from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any


@dataclass
class AccountProfile:
    auth_token: str
    ct0: str
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    weight: int = 1
    health: int = 5  # 健康度评分(0-5)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def cookies(self) -> Dict[str, str]:
        """返回账号的cookies"""
        cookies = {
            'auth_token': self.auth_token,
            'ct0': self.ct0,
        }
        if self.username:
            cookies['username'] = self.username
        if self.email:
            cookies['email'] = self.email
        if self.password:
            cookies['password'] = self.password
        return cookies


class WeightedRotator:
    def __init__(self, items: List[Any], weight_attr: str = 'weight', health_attr: str = 'health'):
        self.items = items
        self.weight_attr = weight_attr
        self.health_attr = health_attr
        self.current_index = 0
    
    def next(self) -> Any:
        """获取下一个项目，使用加权轮询算法"""
        if not self.items:
            raise ValueError("No items available")
        
        # 过滤掉健康度为0的项目
        healthy_items = [item for item in self.items if getattr(item, self.health_attr, 0) > 0]
        if not healthy_items:
            # 如果没有健康的项目，重置所有项目健康度并返回第一个
            for item in self.items:
                setattr(item, self.health_attr, 1)
            return self.items[0]
        
        # 计算总权重
        total_weight = sum(
            getattr(item, self.weight_attr, 1) * getattr(item, self.health_attr, 5)
            for item in healthy_items
        )
        
        # 选择一个项目
        r = 0
        for item in healthy_items:
            weight = getattr(item, self.weight_attr, 1) * getattr(item, self.health_attr, 5)
            r += weight / total_weight
            if r >= 1.0:
                return item
        
        # 如果没有选中任何项目，返回第一个
        return healthy_items[0] 