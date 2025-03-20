import asyncio
import json
import logging
import random
import time
import yaml
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Literal

import httpx
from httpx import AsyncClient, Client

from .account_profile import AccountProfile, WeightedRotator
from .proxy import ProxyConfig, ProxyPool
from .util import get_headers


class AccountGroup:
    def __init__(self, name: str, accounts: List[AccountProfile], proxy_pool: ProxyPool):
        """
        初始化一个账号组，包含账号列表和代理池
        
        Args:
            name: 组名
            accounts: 账号列表
            proxy_pool: 代理池
        """
        self.name = name
        self.accounts = accounts
        self.proxy_pool = proxy_pool
        self.account_rotator = WeightedRotator(accounts)
        self.logger = logging.getLogger(f"AccountGroup.{name}")
    
    @property
    def active_pair(self) -> Tuple[AccountProfile, ProxyConfig]:
        """
        获取活跃的账号和代理对
        
        Returns:
            Tuple[AccountProfile, ProxyConfig]: 账号和代理的元组
        """
        return (
            self.account_rotator.next(),
            self.proxy_pool.get()
        )
    
    def add_account(self, account: AccountProfile):
        """
        添加一个账号到组
        
        Args:
            account: 要添加的账号
        """
        self.accounts.append(account)
    
    def remove_account(self, auth_token: str):
        """
        从组中移除一个账号
        
        Args:
            auth_token: 要移除的账号的auth_token
        """
        self.accounts = [a for a in self.accounts if a.auth_token != auth_token]
    
    def update_account_weight(self, auth_token: str, new_weight: int):
        """
        更新账号权重
        
        Args:
            auth_token: 要更新的账号的auth_token
            new_weight: 新的权重值
        """
        for account in self.accounts:
            if account.auth_token == auth_token:
                account.weight = new_weight
                break
    
    def add_proxy(self, proxy: ProxyConfig):
        """
        添加一个代理
        
        Args:
            proxy: 要添加的代理
        """
        self.proxy_pool.add(proxy)
    
    def remove_proxy(self, proxy_url: str):
        """
        移除一个代理
        
        Args:
            proxy_url: 要移除的代理URL
        """
        for proxy in self.proxy_pool.proxies:
            if proxy.url == proxy_url:
                self.proxy_pool.remove(proxy)
                break
    
    def __len__(self):
        """
        返回组中账号的数量
        
        Returns:
            int: 账号数量
        """
        return len(self.accounts)


class GroupManager:
    def __init__(self):
        """
        初始化GroupManager实例，用于管理账号组和代理组
        """
        self.groups: Dict[str, AccountGroup] = {}
        self.logger = logging.getLogger("GroupManager")
    
    def add_group(self, name: str, accounts: List[AccountProfile], proxies: List[ProxyConfig]):
        """
        添加一个账号代理组
        
        Args:
            name: 组名
            accounts: 账号列表
            proxies: 代理列表
        """
        proxy_pool = ProxyPool(proxies)
        self.groups[name] = AccountGroup(name, accounts, proxy_pool)
        self.logger.info(f"Added group {name} with {len(accounts)} accounts and {len(proxies)} proxies")
    
    def remove_group(self, name: str):
        """
        移除一个组
        
        Args:
            name: 要移除的组名
        """
        if name in self.groups:
            del self.groups[name]
            self.logger.info(f"Removed group {name}")
    
    def get_group(self, name: str) -> AccountGroup:
        """
        获取一个组
        
        Args:
            name: 组名
            
        Returns:
            AccountGroup: 账号组对象
            
        Raises:
            ValueError: 如果组不存在
        """
        if name not in self.groups:
            raise ValueError(f"Group {name} not found")
        return self.groups[name]
    
    def get_client(self, group_name: str) -> Client:
        """
        获取一个配置了账号和代理的httpx Client实例
        
        Args:
            group_name: 组名
            
        Returns:
            Client: 配置了账号和代理的httpx客户端
            
        Raises:
            ValueError: 如果组不存在
        """
        group = self.get_group(group_name)
        account, proxy = group.active_pair
        
        client = Client(
            cookies=account.cookies,
            proxies=proxy.httpx_proxy_config,
            follow_redirects=True,
            timeout=proxy.timeout,
            verify=proxy.verify
        )
        client.headers.update(get_headers(client))
        return client
    
    async def get_async_client(self, group_name: str) -> AsyncClient:
        """
        获取一个配置了账号和代理的httpx AsyncClient实例
        
        Args:
            group_name: 组名
            
        Returns:
            AsyncClient: 配置了账号和代理的异步httpx客户端
            
        Raises:
            ValueError: 如果组不存在
        """
        group = self.get_group(group_name)
        account, proxy = group.active_pair
        
        client = AsyncClient(
            cookies=account.cookies,
            proxies=proxy.httpx_proxy_config,
            follow_redirects=True,
            timeout=proxy.timeout,
            verify=proxy.verify
        )
        client.headers.update(get_headers(client))
        return client
    
    def add_account(self, group_name: str, account: AccountProfile):
        """
        添加一个账号到组
        
        Args:
            group_name: 组名
            account: 要添加的账号
            
        Raises:
            ValueError: 如果组不存在
        """
        self.get_group(group_name).add_account(account)
    
    def remove_account(self, group_name: str, auth_token: str):
        """
        从组中移除一个账号
        
        Args:
            group_name: 组名
            auth_token: 要移除的账号的auth_token
            
        Raises:
            ValueError: 如果组不存在
        """
        self.get_group(group_name).remove_account(auth_token)
    
    def update_account_weight(self, group_name: str, auth_token: str, new_weight: int):
        """
        更新组中账号的权重
        
        Args:
            group_name: 组名
            auth_token: 要更新的账号的auth_token
            new_weight: 新的权重值
            
        Raises:
            ValueError: 如果组不存在
        """
        self.get_group(group_name).update_account_weight(auth_token, new_weight)
    
    def add_proxy(self, group_name: str, proxy: ProxyConfig):
        """
        添加一个代理到组
        
        Args:
            group_name: 组名
            proxy: 要添加的代理
            
        Raises:
            ValueError: 如果组不存在
        """
        self.get_group(group_name).add_proxy(proxy)
    
    def remove_proxy(self, group_name: str, proxy_url: str):
        """
        从组中移除一个代理
        
        Args:
            group_name: 组名
            proxy_url: 要移除的代理URL
            
        Raises:
            ValueError: 如果组不存在
        """
        self.get_group(group_name).remove_proxy(proxy_url)
    
    def set_proxy_strategy(self, group_name: str, strategy: str):
        """
        设置组的代理选择策略
        
        Args:
            group_name: 组名
            strategy: 代理选择策略，可选值:
                - 'latency': 选择延迟最低的代理
                - 'success_rate': 选择成功率最高的代理
                - 'random': 随机选择一个代理
                - 'weighted': 根据代理权重和健康度进行加权选择（默认）
                
        Raises:
            ValueError: 如果组不存在或策略无效
        """
        self.get_group(group_name).proxy_pool.set_strategy(strategy)
    
    def generate_report(self, start_date: str = None, end_date: str = None, metrics: List[str] = None) -> Dict:
        """
        生成流量分析报告
        
        Args:
            start_date: 开始日期（可选），格式为 'YYYY-MM-DD'
            end_date: 结束日期（可选），格式为 'YYYY-MM-DD'
            metrics: 要包含的指标列表（可选），默认包含所有指标
            
        Returns:
            Dict: 包含各组代理使用情况的报告字典
        """
        report = {}
        for name, group in self.groups.items():
            group_report = {
                "accounts": len(group.accounts),
                "proxies": len(group.proxy_pool.proxies),
                "proxy_metrics": {}
            }
            
            for proxy in group.proxy_pool.proxies:
                metrics_obj = group.proxy_pool.health_checker.metrics[proxy]
                group_report["proxy_metrics"][proxy.url] = {
                    "success_rate": metrics_obj.success_rate,
                    "avg_latency": metrics_obj.avg_latency,
                    "success_count": metrics_obj.success_count,
                    "error_count": metrics_obj.error_count,
                    "health": proxy.health
                }
            
            report[name] = group_report
        
        return report
    
    @classmethod
    def load(cls, accounts_path: str, proxies_path: str) -> 'GroupManager':
        """
        从配置文件加载GroupManager
        
        Args:
            accounts_path: 账号配置文件路径（yaml或json）
            proxies_path: 代理配置文件路径（yaml或json）
            
        Returns:
            GroupManager: 配置好的GroupManager实例
            
        Raises:
            FileNotFoundError: 如果配置文件不存在
            ValueError: 如果配置文件格式无效
        """
        manager = cls()
        
        # 加载账号配置
        with open(accounts_path, 'r') as f:
            if accounts_path.endswith('.yaml') or accounts_path.endswith('.yml'):
                accounts_config = yaml.safe_load(f)
            else:
                accounts_config = json.load(f)
        
        # 加载代理配置
        with open(proxies_path, 'r') as f:
            if proxies_path.endswith('.yaml') or proxies_path.endswith('.yml'):
                proxies_config = yaml.safe_load(f)
            else:
                proxies_config = json.load(f)
        
        # 创建组
        for group_name, group_data in accounts_config.get('groups', {}).items():
            accounts = []
            for account_data in group_data.get('accounts', []):
                accounts.append(AccountProfile(**account_data))
            
            proxies = []
            if group_name in proxies_config.get('groups', {}):
                for proxy_data in proxies_config['groups'][group_name].get('proxies', []):
                    # 处理auth字段
                    if 'auth' in proxy_data and isinstance(proxy_data['auth'], dict):
                        from .proxy import ProxyAuth
                        proxy_data['auth'] = ProxyAuth(**proxy_data['auth'])
                    proxies.append(ProxyConfig(**proxy_data))
            
            manager.add_group(group_name, accounts, proxies)
        
        return manager
    
    def save(self, accounts_path: str, proxies_path: str):
        """
        保存配置到文件
        
        Args:
            accounts_path: 账号配置保存路径（yaml或json）
            proxies_path: 代理配置保存路径（yaml或json）
            
        Raises:
            IOError: 如果写入文件失败
        """
        accounts_config = {"groups": {}}
        proxies_config = {"groups": {}}
        
        for name, group in self.groups.items():
            # 保存账号配置
            accounts_config["groups"][name] = {
                "accounts": [
                    {
                        "auth_token": a.auth_token,
                        "ct0": a.ct0,
                        "username": a.username,
                        "email": a.email,
                        "password": a.password,
                        "weight": a.weight,
                        "health": a.health,
                        "metadata": a.metadata
                    }
                    for a in group.accounts
                ]
            }
            
            # 保存代理配置
            proxies_config["groups"][name] = {
                "proxies": [
                    {
                        "url": p.url,
                        "protocol": p.protocol,
                        "auth": {
                            "username": p.auth.username,
                            "password": p.auth.password
                        } if p.auth else None,
                        "max_connections": p.max_connections,
                        "timeout": p.timeout,
                        "verify": p.verify,
                        "weight": p.weight,
                        "health": p.health
                    }
                    for p in group.proxy_pool.proxies
                ]
            }
        
        # 写入文件
        with open(accounts_path, 'w') as f:
            if accounts_path.endswith('.yaml') or accounts_path.endswith('.yml'):
                yaml.dump(accounts_config, f)
            else:
                json.dump(accounts_config, f, indent=2)
        
        with open(proxies_path, 'w') as f:
            if proxies_path.endswith('.yaml') or proxies_path.endswith('.yml'):
                yaml.dump(proxies_config, f)
            else:
                json.dump(proxies_config, f, indent=2) 