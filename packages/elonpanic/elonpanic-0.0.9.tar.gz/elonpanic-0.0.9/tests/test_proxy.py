import unittest
import asyncio
from unittest.mock import patch, MagicMock

from twitter.proxy import ProxyConfig, ProxyAuth, ProxyHealthChecker, ProxyPool, ProxyProtocol, ProxyMetrics


class TestProxyConfig(unittest.TestCase):
    def test_init_with_url_only(self):
        """测试仅使用URL初始化ProxyConfig"""
        proxy = ProxyConfig(url="http://example.com:8080")
        self.assertEqual(proxy.url, "http://example.com:8080")
        self.assertEqual(proxy.protocol, ProxyProtocol.HTTP)
        self.assertIsNone(proxy.auth)
        self.assertEqual(proxy.max_connections, 100)
        self.assertEqual(proxy.timeout, 10.0)
        self.assertTrue(proxy.verify)
        self.assertEqual(proxy.weight, 1)
        self.assertEqual(proxy.health, 5)
    
    def test_init_with_auth_in_url(self):
        """测试URL中包含认证信息时初始化ProxyConfig"""
        proxy = ProxyConfig(url="http://user:pass@example.com:8080")
        self.assertEqual(proxy.url, "http://user:pass@example.com:8080")
        self.assertIsNotNone(proxy.auth)
        self.assertEqual(proxy.auth.username, "user")
        self.assertEqual(proxy.auth.password, "pass")
    
    def test_init_with_auth_object(self):
        """测试使用ProxyAuth对象初始化ProxyConfig"""
        auth = ProxyAuth(username="user", password="pass")
        proxy = ProxyConfig(url="http://example.com:8080", auth=auth)
        self.assertEqual(proxy.url, "http://example.com:8080")
        self.assertEqual(proxy.auth, auth)
    
    def test_init_protocol_correction(self):
        """测试URL协议自动修正"""
        proxy = ProxyConfig(url="example.com:8080", protocol=ProxyProtocol.SOCKS5)
        self.assertEqual(proxy.url, "socks5://example.com:8080")
    
    def test_formatted_url(self):
        """测试获取格式化的URL"""
        auth = ProxyAuth(username="user", password="pass")
        proxy = ProxyConfig(url="http://example.com:8080", auth=auth)
        self.assertEqual(proxy.formatted_url, "http://user:pass@example.com:8080")
    
    def test_httpx_proxy_config(self):
        """测试获取httpx代理配置"""
        proxy = ProxyConfig(url="http://example.com:8080")
        config = proxy.httpx_proxy_config
        self.assertEqual(config["http://"], "http://example.com:8080")
        self.assertEqual(config["https://"], "http://example.com:8080")
    
    def test_should_retry(self):
        """测试should_retry方法"""
        proxy = ProxyConfig(url="http://example.com:8080")
        self.assertTrue(proxy.should_retry(429))
        self.assertTrue(proxy.should_retry(500))
        self.assertFalse(proxy.should_retry(404))
    
    def test_get_retry_delay(self):
        """测试get_retry_delay方法"""
        proxy = ProxyConfig(url="http://example.com:8080", retry_delay=1.0)
        # 重试延迟应该随着尝试次数增加而增加（指数退避）
        self.assertTrue(1.0 <= proxy.get_retry_delay(0) < 2.0)  # 1.0 + random(0-1)
        self.assertTrue(2.0 <= proxy.get_retry_delay(1) < 3.0)  # 2.0 + random(0-1)
        self.assertTrue(4.0 <= proxy.get_retry_delay(2) < 5.0)  # 4.0 + random(0-1)


class TestProxyMetrics(unittest.TestCase):
    def test_init(self):
        """测试初始化ProxyMetrics"""
        metrics = ProxyMetrics()
        self.assertEqual(metrics.success_count, 0)
        self.assertEqual(metrics.error_count, 0)
        self.assertEqual(metrics.total_latency, 0)
        self.assertEqual(metrics.last_check, 0)
        self.assertIsNone(metrics.last_error)
    
    def test_success_rate(self):
        """测试成功率计算"""
        metrics = ProxyMetrics()
        # 初始状态应该是0
        self.assertEqual(metrics.success_rate, 0)
        
        # 添加成功和失败
        metrics.update(latency=0.1, success=True)
        metrics.update(latency=0.2, success=True)
        metrics.update(latency=0.3, success=False)
        
        # 成功率应该是2/3
        self.assertAlmostEqual(metrics.success_rate, 2/3, places=2)
    
    def test_avg_latency(self):
        """测试平均延迟计算"""
        metrics = ProxyMetrics()
        # 初始状态应该是无穷大
        self.assertEqual(metrics.avg_latency, float('inf'))
        
        # 添加成功请求
        metrics.update(latency=0.1, success=True)
        metrics.update(latency=0.3, success=True)
        
        # 平均延迟应该是0.2
        self.assertEqual(metrics.avg_latency, 0.2)
        
        # 失败请求不应该影响平均延迟
        metrics.update(latency=0.5, success=False)
        self.assertEqual(metrics.avg_latency, 0.2)
    
    def test_report_error(self):
        """测试报告错误"""
        metrics = ProxyMetrics()
        error = Exception("Test error")
        metrics.report_error(error)
        
        self.assertEqual(metrics.error_count, 1)
        self.assertEqual(metrics.last_error, "Test error")
        self.assertGreater(metrics.last_check, 0)


class TestProxyHealthChecker(unittest.TestCase):
    def setUp(self):
        self.proxies = [
            ProxyConfig(url="http://example1.com:8080", weight=1, health=5),
            ProxyConfig(url="http://example2.com:8080", weight=2, health=3),
            ProxyConfig(url="http://example3.com:8080", weight=1, health=0),  # 不健康的代理
        ]
        self.checker = ProxyHealthChecker(self.proxies)
        
        # 初始化指标
        for proxy in self.proxies:
            self.checker.metrics[proxy] = ProxyMetrics()
            
        # 添加一些测试数据
        self.checker.metrics[self.proxies[0]].update(latency=0.1, success=True)
        self.checker.metrics[self.proxies[0]].update(latency=0.3, success=True)
        
        self.checker.metrics[self.proxies[1]].update(latency=0.5, success=True)
        self.checker.metrics[self.proxies[1]].update(latency=0.7, success=False)
    
    def test_best_proxy_latency_strategy(self):
        """测试延迟策略"""
        best_proxy = self.checker.best_proxy(strategy="latency")
        # 应该选择延迟最低的代理（第一个）
        self.assertEqual(best_proxy, self.proxies[0])
    
    def test_best_proxy_success_rate_strategy(self):
        """测试成功率策略"""
        best_proxy = self.checker.best_proxy(strategy="success_rate")
        # 第一个代理成功率100%，第二个代理成功率50%
        self.assertEqual(best_proxy, self.proxies[0])
        
        # 如果所有代理成功率为0，应该选择第一个健康的代理
        for proxy in self.proxies:
            self.checker.metrics[proxy] = ProxyMetrics()
        best_proxy = self.checker.best_proxy(strategy="success_rate")
        self.assertIn(best_proxy, [self.proxies[0], self.proxies[1]])
    
    def test_best_proxy_random_strategy(self):
        """测试随机策略"""
        # 多次尝试，应该有不同的结果
        results = set()
        for _ in range(10):
            best_proxy = self.checker.best_proxy(strategy="random")
            # 健康度为0的代理不应该被选中
            self.assertNotEqual(best_proxy, self.proxies[2])
            results.add(best_proxy)
        
        # 由于随机性，可能不会选择所有健康的代理，但应该至少有一个
        self.assertGreaterEqual(len(results), 1)
    
    def test_best_proxy_weighted_strategy(self):
        """测试加权策略"""
        # 多次尝试，应该根据权重选择
        counts = {self.proxies[0]: 0, self.proxies[1]: 0}
        for _ in range(100):
            best_proxy = self.checker.best_proxy(strategy="weighted")
            # 健康度为0的代理不应该被选中
            self.assertNotEqual(best_proxy, self.proxies[2])
            if best_proxy in counts:
                counts[best_proxy] += 1
        
        # 由于权重和健康度，第二个代理的选择频率应该大致为(2*3)/(1*5+2*3)=6/11≈0.55
        # 考虑到随机性，允许一定的误差
        total = counts[self.proxies[0]] + counts[self.proxies[1]]
        ratio = counts[self.proxies[1]] / total if total > 0 else 0
        self.assertGreaterEqual(ratio, 0.35)  # 允许一定的误差
        self.assertLessEqual(ratio, 0.75)
    
    @patch("httpx.AsyncClient")
    async def test_check_proxy(self, mock_client):
        """测试代理健康检查"""
        # 模拟成功的健康检查
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_context = MagicMock()
        mock_context.__aenter__.return_value = mock_client
        mock_client.get.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        
        proxy = self.proxies[0]
        await self.checker._check_proxy(proxy)
        
        # 代理健康度应该增加到上限
        self.assertEqual(proxy.health, 5)
        
        # 模拟失败的健康检查
        mock_response.status_code = 500
        await self.checker._check_proxy(proxy)
        
        # 代理健康度应该减少
        self.assertEqual(proxy.health, 4)
        
        # 模拟异常
        mock_client.get.side_effect = Exception("Test error")
        await self.checker._check_proxy(proxy)
        
        # 代理健康度应该减少2点
        self.assertEqual(proxy.health, 2)


class TestProxyPool(unittest.TestCase):
    def setUp(self):
        self.proxies = [
            ProxyConfig(url="http://example1.com:8080", weight=1, health=5),
            ProxyConfig(url="http://example2.com:8080", weight=2, health=3),
        ]
        self.pool = ProxyPool(self.proxies)
    
    def test_get_default_strategy(self):
        """测试默认策略获取代理"""
        proxy = self.pool.get()
        self.assertIn(proxy, self.proxies)
    
    def test_get_with_strategy(self):
        """测试指定策略获取代理"""
        # 测试不同的策略
        proxy_latency = self.pool.get(strategy="latency")
        self.assertIn(proxy_latency, self.proxies)
        
        proxy_success = self.pool.get(strategy="success_rate")
        self.assertIn(proxy_success, self.proxies)
        
        proxy_random = self.pool.get(strategy="random")
        self.assertIn(proxy_random, self.proxies)
        
        proxy_weighted = self.pool.get(strategy="weighted")
        self.assertIn(proxy_weighted, self.proxies)
    
    def test_add_proxy(self):
        """测试添加代理"""
        new_proxy = ProxyConfig(url="http://example3.com:8080")
        self.pool.add(new_proxy)
        
        # 代理池中应该有3个代理
        self.assertEqual(len(self.pool.proxies), 3)
        self.assertIn(new_proxy, self.pool.proxies)
    
    def test_remove_proxy(self):
        """测试移除代理"""
        proxy = self.proxies[0]
        self.pool.remove(proxy)
        
        # 代理池中应该只有1个代理
        self.assertEqual(len(self.pool.proxies), 1)
        self.assertNotIn(proxy, self.pool.proxies)
    
    def test_set_strategy(self):
        """测试设置策略"""
        # 默认策略应该是weighted
        self.assertEqual(self.pool.strategy, "weighted")
        
        # 设置为latency
        self.pool.set_strategy("latency")
        self.assertEqual(self.pool.strategy, "latency")
        
        # 设置为无效策略应该抛出异常
        with self.assertRaises(ValueError):
            self.pool.set_strategy("invalid")
    
    def test_len(self):
        """测试获取代理池大小"""
        self.assertEqual(len(self.pool), 2)


if __name__ == "__main__":
    unittest.main() 