"""
推特账号代理管理模块
支持HTTP和SOCKS5代理
"""

import json
from pathlib import Path
from typing import Dict, Optional, Union, List

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
    
    def set_proxy(self, username: str, proxy_url: str, proxy_type: str = 'http') -> bool:
        """
        为特定用户设置代理
        
        参数:
            username: Twitter用户名
            proxy_url: 代理URL (例如: "127.0.0.1:8080")
            proxy_type: 代理类型 (http, https, socks5)
            
        返回:
            设置是否成功
        """
        if proxy_type not in PROXY_TYPES:
            print(f"不支持的代理类型: {proxy_type}, 支持的类型: {', '.join(PROXY_TYPES.keys())}")
            return False
        
        # 构建代理URL
        formatted_proxy = f"{PROXY_TYPES[proxy_type]}://{proxy_url}"
        
        # 保存代理配置
        self.proxy_configs[username] = {
            "url": formatted_proxy,
            "type": proxy_type
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
    
    def list_proxies(self) -> Dict:
        """列出所有配置的代理"""
        return self.proxy_configs 