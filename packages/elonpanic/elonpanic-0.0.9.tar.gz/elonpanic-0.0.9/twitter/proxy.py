import asyncio
import random
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Literal, Optional, Union
from urllib.parse import urlparse

import httpx


class ProxyProtocol(str, Enum):
    HTTP = "http"
    HTTPS = "https"
    SOCKS5 = "socks5"


@dataclass
class ProxyAuth:
    username: str
    password: str


@dataclass
class ProxyMetrics:
    success_count: int = 0
    error_count: int = 0
    total_latency: float = 0
    last_check: float = 0
    last_error: Optional[str] = None
    
    @property
    def success_rate(self) -> float:
        total = self.success_count + self.error_count
        return self.success_count / total if total > 0 else 0
    
    @property
    def avg_latency(self) -> float:
        return self.total_latency / self.success_count if self.success_count > 0 else float('inf')
    
    def update(self, latency: float, success: bool):
        if success:
            self.success_count += 1
            self.total_latency += latency
        else:
            self.error_count += 1
        self.last_check = time.time()
    
    def report_error(self, error: Exception):
        self.error_count += 1
        self.last_error = str(error)
        self.last_check = time.time()


@dataclass
class ProxyConfig:
    url: str
    protocol: ProxyProtocol = ProxyProtocol.HTTP
    auth: Optional[ProxyAuth] = None
    max_connections: int = 100
    timeout: float = 10.0
    verify: bool = True
    weight: int = 1
    health: int = 5  # 健康度评分(0-5)
    max_retries: int = 3  # 最大重试次数
    retry_codes: List[int] = field(default_factory=lambda: [429, 500, 502, 503, 504])  # 需要重试的状态码
    retry_delay: float = 1.0  # 重试延迟基数（秒）
    
    def __post_init__(self):
        # 如果URL中包含认证信息但auth未设置，则从URL提取
        if not self.auth and '@' in self.url:
            parsed = urlparse(self.url)
            if parsed.username and parsed.password:
                self.auth = ProxyAuth(
                    username=parsed.username,
                    password=parsed.password
                )
        
        # 确保协议正确
        if not self.url.startswith(f"{self.protocol}://"):
            self.url = f"{self.protocol}://{self.url}"
        
        # 确保retry_codes是列表类型
        if not isinstance(self.retry_codes, list):
            self.retry_codes = list(self.retry_codes)
    
    @property
    def formatted_url(self) -> str:
        """返回格式化的代理URL，适用于httpx"""
        parsed = urlparse(self.url)
        if self.auth and not (parsed.username and parsed.password):
            # 如果URL中没有认证信息但auth已设置，则添加到URL
            netloc = f"{self.auth.username}:{self.auth.password}@{parsed.netloc}"
            parts = list(parsed)
            parts[1] = netloc
            return urlparse.urlunparse(parts)
        return self.url
    
    @property
    def httpx_proxy_config(self) -> Dict[str, str]:
        """返回适用于httpx的代理配置"""
        return {
            "http://": self.formatted_url,
            "https://": self.formatted_url
        }
        
    def should_retry(self, status_code: int) -> bool:
        """判断是否应该重试"""
        return status_code in self.retry_codes
        
    def get_retry_delay(self, attempt: int) -> float:
        """获取重试延迟时间（指数退避）"""
        return self.retry_delay * (2 ** attempt) + random.random()


class ProxyHealthChecker:
    def __init__(self, proxies: List[ProxyConfig]):
        self.proxies = proxies
        self.metrics: Dict[ProxyConfig, ProxyMetrics] = {
            proxy: ProxyMetrics() for proxy in proxies
        }
        self._running = False
        self._task = None
    
    def start(self):
        """启动健康检查任务"""
        if not self._running:
            self._running = True
            self._task = asyncio.create_task(self._continuous_check())
    
    def stop(self):
        """停止健康检查任务"""
        if self._running and self._task:
            self._task.cancel()
            self._running = False
    
    async def _continuous_check(self):
        """持续检查代理健康状态"""
        while self._running:
            await asyncio.gather(*[
                self._check_proxy(proxy) for proxy in self.proxies
            ])
            await asyncio.sleep(300)  # 5分钟检查一次
    
    async def _check_proxy(self, proxy: ProxyConfig):
        """检查单个代理的健康状态，包含重试逻辑"""
        for attempt in range(proxy.max_retries):
            try:
                async with httpx.AsyncClient(
                    proxies=proxy.httpx_proxy_config,
                    timeout=proxy.timeout,
                    verify=proxy.verify
                ) as client:
                    start = time.time()
                    r = await client.get('https://api.twitter.com/1.1/guest/activate.json')
                    latency = time.time() - start
                    
                    if r.status_code >= 400 and proxy.should_retry(r.status_code):
                        if attempt < proxy.max_retries - 1:
                            delay = proxy.get_retry_delay(attempt)
                            await asyncio.sleep(delay)
                            continue
                    
                    success = r.status_code < 400
                    self.metrics[proxy].update(latency=latency, success=success)
                    
                    # 动态调整健康度
                    if success:
                        proxy.health = min(5, proxy.health + 1)
                    else:
                        proxy.health = max(0, proxy.health - 1)
                    
                    return
            except Exception as e:
                self.metrics[proxy].report_error(e)
                if attempt < proxy.max_retries - 1:
                    delay = proxy.get_retry_delay(attempt)
                    await asyncio.sleep(delay)
                else:
                    proxy.health = max(0, proxy.health - 2)  # 出错降低2点健康度
    
    def best_proxy(self, strategy: Literal['latency', 'success_rate', 'random', 'weighted'] = 'weighted') -> ProxyConfig:
        """
        根据策略选择最佳代理
        
        Args:
            strategy: 代理选择策略
                - 'latency': 选择延迟最低的代理
                - 'success_rate': 选择成功率最高的代理
                - 'random': 随机选择一个健康的代理
                - 'weighted': 根据代理权重和健康度进行加权选择（默认）
        
        Returns:
            ProxyConfig: 选择的代理
        
        Note:
            'weighted' 策略考虑代理的健康度和配置的权重，适合大多数场景
            'latency' 策略适合对响应时间敏感的场景
            'success_rate' 策略适合需要高可靠性的场景
            'random' 策略在多个代理性能相近时提供负载均衡
        """
        # 过滤掉健康度为0的代理
        healthy_proxies = [p for p in self.proxies if p.health > 0]
        if not healthy_proxies:
            # 如果没有健康的代理，重置所有代理健康度并返回随机一个
            for p in self.proxies:
                p.health = 1
            return random.choice(self.proxies)
        
        if strategy == 'latency':
            return min(healthy_proxies, key=lambda p: self.metrics[p].avg_latency)
        elif strategy == 'success_rate':
            return max(healthy_proxies, key=lambda p: self.metrics[p].success_rate)
        elif strategy == 'random':
            return random.choice(healthy_proxies)
        elif strategy == 'weighted':
            # 根据健康度和权重计算总权重
            weights = [p.health * p.weight for p in healthy_proxies]
            return random.choices(healthy_proxies, weights=weights, k=1)[0]
        else:
            raise ValueError(f"Unknown strategy: {strategy}")


class ProxyPool:
    def __init__(self, proxies: List[ProxyConfig]):
        self.proxies = proxies
        self.health_checker = ProxyHealthChecker(proxies)
        self.strategy = 'weighted'
        
        # 启动健康检查
        self.health_checker.start()
    
    def set_strategy(self, strategy: str):
        """
        设置代理选择策略
        
        Args:
            strategy: 代理选择策略，可选值:
                - 'latency': 选择延迟最低的代理
                - 'success_rate': 选择成功率最高的代理
                - 'random': 随机选择一个健康的代理
                - 'weighted': 根据代理权重和健康度进行加权选择（默认）
                
        Raises:
            ValueError: 如果策略无效
        """
        valid_strategies = ['latency', 'success_rate', 'random', 'weighted']
        if strategy not in valid_strategies:
            raise ValueError(f"Invalid strategy: {strategy}. Valid strategies are: {', '.join(valid_strategies)}")
        self.strategy = strategy

    def get(self, strategy: Optional[str] = None) -> ProxyConfig:
        """
        获取一个代理
        
        Args:
            strategy: 代理选择策略，可选值:
                - 'latency': 选择延迟最低的代理
                - 'success_rate': 选择成功率最高的代理
                - 'random': 随机选择一个健康的代理
                - 'weighted': 根据代理权重和健康度进行加权选择（默认）
                
                如果为None，则使用当前设置的策略
                
        Returns:
            ProxyConfig: 选择的代理
            
        Raises:
            ValueError: 如果策略无效或没有可用代理
        """
        return self.health_checker.best_proxy(strategy or self.strategy)
    
    def add(self, proxy: ProxyConfig):
        """添加一个代理"""
        self.proxies.append(proxy)
        self.health_checker.metrics[proxy] = ProxyMetrics()
    
    def remove(self, proxy: ProxyConfig):
        """移除一个代理"""
        if proxy in self.proxies:
            self.proxies.remove(proxy)
            self.health_checker.metrics.pop(proxy, None)
    
    def __len__(self):
        return len(self.proxies) 