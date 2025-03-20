"""
推特账号代理管理模块
支持HTTP和SOCKS5代理
"""

import json
from pathlib import Path
from typing import Dict, Optional, Union, List
import re
from urllib.parse import urlparse

from .constants import PROXY_TYPES, DEFAULT_PROXY


class ProxyManager:
    """代理管理器，管理不同账号的代理配置"""

    def __init__(self, config_path: Optional[str] = None):
        """
        初始化代理管理器
        
        参数:
            config_path: 代理配置文件路径，不提供时使用默认路径
        """
        self.config_path = config_path or str(Path.home() / ".twitter_proxies.json")
        self.proxy_configs = self._load_config()
    
    def _load_config(self) -> Dict:
        """加载代理配置"""
        try:
            if Path(self.config_path).exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"加载代理配置失败: {e}")
            return {}
    
    def _save_config(self) -> None:
        """保存代理配置"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.proxy_configs, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"保存代理配置失败: {e}")
    
    def set_proxy(self, username: str, proxy_url: str, proxy_type: str = 'http', 
                 proxy_username: Optional[str] = None, proxy_password: Optional[str] = None) -> bool:
        """
        为特定用户设置代理
        
        参数:
            username: Twitter用户名
            proxy_url: 代理URL (例如: "127.0.0.1:8080")
            proxy_type: 代理类型 (http, https, socks5)
            proxy_username: 代理认证用户名
            proxy_password: 代理认证密码
            
        返回:
            设置是否成功
        """
        if proxy_type not in PROXY_TYPES:
            print(f"不支持的代理类型: {proxy_type}, 支持的类型: {', '.join(PROXY_TYPES.keys())}")
            return False
        
        # 确保proxy_url不包含协议前缀和认证信息
        if '://' in proxy_url:
            parsed = urlparse(proxy_url)
            # 如果URL已包含认证信息，提取它
            if parsed.username and not proxy_username:
                proxy_username = parsed.username
            if parsed.password and not proxy_password:
                proxy_password = parsed.password
            
            # 只使用主机和端口部分
            proxy_url = f"{parsed.hostname}:{parsed.port}" if parsed.port else parsed.hostname
        
        # 构建代理URL
        if proxy_username and proxy_password:
            # 带认证的代理格式
            formatted_proxy = f"{PROXY_TYPES[proxy_type]}://{proxy_username}:{proxy_password}@{proxy_url}"
        else:
            # 无认证的代理格式
            formatted_proxy = f"{PROXY_TYPES[proxy_type]}://{proxy_url}"
        
        # 保存代理配置
        self.proxy_configs[username] = {
            "url": formatted_proxy,
            "type": proxy_type,
            "has_auth": bool(proxy_username and proxy_password)
        }
        self._save_config()
        return True
    
    def remove_proxy(self, username: str) -> bool:
        """
        移除用户的代理设置
        
        参数:
            username: Twitter用户名
            
        返回:
            移除是否成功
        """
        if username in self.proxy_configs:
            del self.proxy_configs[username]
            self._save_config()
            return True
        return False
    
    def get_proxy(self, username: str) -> Optional[str]:
        """
        获取指定用户的代理URL
        
        参数:
            username: Twitter用户名
            
        返回:
            代理URL或None（如果未设置）
        """
        if username in self.proxy_configs:
            return self.proxy_configs[username]["url"]
        return DEFAULT_PROXY
    
    def get_proxy_dict(self, username: str) -> Optional[Dict[str, str]]:
        """
        获取指定用户的代理配置字典，可用于httpx客户端
        
        参数:
            username: Twitter用户名
            
        返回:
            代理配置字典，格式为：{"http://": "...", "https://": "..."}
        """
        proxy_url = self.get_proxy(username)
        if not proxy_url:
            return None
            
        # 解析代理URL
        parsed = urlparse(proxy_url)
        protocol = parsed.scheme
        
        # 处理SOCKS5代理
        if protocol == "socks5":
            return {"http://": proxy_url, "https://": proxy_url}
        else:
            # 处理HTTP/HTTPS代理
            return {
                "http://": proxy_url,
                "https://": proxy_url.replace("http://", "https://") if proxy_url.startswith("http://") else proxy_url
            }
    
    def list_proxies(self) -> Dict:
        """列出所有配置的代理"""
        return self.proxy_configs 