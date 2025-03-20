import unittest
import tempfile
import os
from pathlib import Path
import yaml
import json

from twitter.manager import GroupManager
from twitter.account_profile import AccountProfile
from twitter.proxy import ProxyConfig, ProxyProtocol, ProxyAuth


class TestGroupManager(unittest.TestCase):
    def setUp(self):
        # 创建测试数据
        self.accounts_data = {
            "groups": {
                "test_group": {
                    "accounts": [
                        {
                            "auth_token": "test_token_1",
                            "ct0": "test_ct0_1",
                            "username": "test_user_1",
                            "weight": 1
                        },
                        {
                            "auth_token": "test_token_2",
                            "ct0": "test_ct0_2",
                            "username": "test_user_2",
                            "weight": 2
                        }
                    ]
                }
            }
        }
        
        self.proxies_data = {
            "groups": {
                "test_group": {
                    "proxies": [
                        {
                            "url": "http://test-proxy-1.com:8080",
                            "protocol": "http",
                            "weight": 1
                        },
                        {
                            "url": "socks5://test-proxy-2.com:1080",
                            "protocol": "socks5",
                            "auth": {
                                "username": "test_user",
                                "password": "test_pass"
                            },
                            "weight": 2
                        }
                    ]
                }
            }
        }
        
        # 创建临时文件
        self.temp_dir = tempfile.TemporaryDirectory()
        self.accounts_path = os.path.join(self.temp_dir.name, "accounts.yaml")
        self.proxies_path = os.path.join(self.temp_dir.name, "proxies.yaml")
        
        # 写入测试数据
        with open(self.accounts_path, "w") as f:
            yaml.dump(self.accounts_data, f)
        
        with open(self.proxies_path, "w") as f:
            yaml.dump(self.proxies_data, f)
        
        # 创建管理器
        self.manager = GroupManager.load(self.accounts_path, self.proxies_path)
    
    def tearDown(self):
        # 清理临时文件
        self.temp_dir.cleanup()
    
    def test_load_manager(self):
        # 测试加载配置
        self.assertIn("test_group", self.manager.groups)
        group = self.manager.groups["test_group"]
        self.assertEqual(len(group.accounts), 2)
        self.assertEqual(len(group.proxy_pool.proxies), 2)
        
        # 检查账号
        self.assertEqual(group.accounts[0].auth_token, "test_token_1")
        self.assertEqual(group.accounts[1].auth_token, "test_token_2")
        
        # 检查代理
        self.assertEqual(group.proxy_pool.proxies[0].url, "http://test-proxy-1.com:8080")
        self.assertEqual(group.proxy_pool.proxies[1].url, "socks5://test-proxy-2.com:1080")
        self.assertEqual(group.proxy_pool.proxies[1].auth.username, "test_user")
    
    def test_add_account(self):
        # 测试添加账号
        new_account = AccountProfile(
            auth_token="new_token",
            ct0="new_ct0",
            username="new_user"
        )
        self.manager.add_account("test_group", new_account)
        
        group = self.manager.groups["test_group"]
        self.assertEqual(len(group.accounts), 3)
        self.assertEqual(group.accounts[2].auth_token, "new_token")
    
    def test_remove_account(self):
        # 测试移除账号
        self.manager.remove_account("test_group", "test_token_1")
        
        group = self.manager.groups["test_group"]
        self.assertEqual(len(group.accounts), 1)
        self.assertEqual(group.accounts[0].auth_token, "test_token_2")
    
    def test_add_proxy(self):
        # 测试添加代理
        new_proxy = ProxyConfig(
            url="http://new-proxy.com:8080",
            protocol=ProxyProtocol.HTTP
        )
        self.manager.add_proxy("test_group", new_proxy)
        
        group = self.manager.groups["test_group"]
        self.assertEqual(len(group.proxy_pool.proxies), 3)
        self.assertEqual(group.proxy_pool.proxies[2].url, "http://new-proxy.com:8080")
    
    def test_remove_proxy(self):
        # 测试移除代理
        self.manager.remove_proxy("test_group", "http://test-proxy-1.com:8080")
        
        group = self.manager.groups["test_group"]
        self.assertEqual(len(group.proxy_pool.proxies), 1)
        self.assertEqual(group.proxy_pool.proxies[0].url, "socks5://test-proxy-2.com:1080")
    
    def test_update_account_weight(self):
        # 测试更新账号权重
        self.manager.update_account_weight("test_group", "test_token_1", 5)
        
        group = self.manager.groups["test_group"]
        for account in group.accounts:
            if account.auth_token == "test_token_1":
                self.assertEqual(account.weight, 5)
    
    def test_set_proxy_strategy(self):
        # 测试设置代理策略
        self.manager.set_proxy_strategy("test_group", "latency")
        
        group = self.manager.groups["test_group"]
        self.assertEqual(group.proxy_pool.strategy, "latency")
    
    def test_save_config(self):
        # 测试保存配置
        new_accounts_path = os.path.join(self.temp_dir.name, "accounts_updated.yaml")
        new_proxies_path = os.path.join(self.temp_dir.name, "proxies_updated.yaml")
        
        self.manager.save(new_accounts_path, new_proxies_path)
        
        # 测试加载新保存的配置
        new_manager = GroupManager.load(new_accounts_path, new_proxies_path)
        self.assertIn("test_group", new_manager.groups)
        self.assertEqual(len(new_manager.groups["test_group"].accounts), 2)
        self.assertEqual(len(new_manager.groups["test_group"].proxy_pool.proxies), 2)
    
    def test_add_group(self):
        # 测试添加组
        accounts = [
            AccountProfile(
                auth_token="group2_token_1",
                ct0="group2_ct0_1"
            )
        ]
        
        proxies = [
            ProxyConfig(
                url="http://group2-proxy.com:8080",
                protocol=ProxyProtocol.HTTP
            )
        ]
        
        self.manager.add_group("test_group_2", accounts, proxies)
        
        self.assertIn("test_group_2", self.manager.groups)
        self.assertEqual(len(self.manager.groups["test_group_2"].accounts), 1)
        self.assertEqual(len(self.manager.groups["test_group_2"].proxy_pool.proxies), 1)


if __name__ == "__main__":
    unittest.main() 