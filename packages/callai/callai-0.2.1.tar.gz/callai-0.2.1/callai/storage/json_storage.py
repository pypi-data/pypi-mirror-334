"""
callai JSON存储模块 - 提供JSON文件会话存储功能
"""

import json
from typing import Dict, List

# 动态导入，避免循环引用
def get_session_class():
    from ..session import Session
    return Session

class SessionJSON:
    """会话JSON文件管理类"""
    
    def __init__(self, client, json_path: str, session_id: str = None):
        """
        初始化会话JSON文件
        
        Args:
            client: Client实例
            json_path: JSON文件路径
            session_id: 会话ID（可选）
        """
        self._client = client
        self._json_path = json_path
        self._session_id = session_id
        self._load_or_init_data()
        
    def _load_or_init_data(self):
        """加载或初始化数据"""
        try:
            with open(self._json_path, "r", encoding="utf-8") as f:
                self._data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self._data = {"sessions": {}}
            self._save_data()
            
    def _save_data(self):
        """保存数据到文件"""
        with open(self._json_path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, ensure_ascii=False, indent=2)
            
    def save_session(self, session):
        """保存会话到JSON文件"""
        session_data = session.to_dict()
        self._data["sessions"][session_data["session_id"]] = session_data
        self._save_data()
        
    def view_sessions(self) -> List[Dict]:
        """查看所有会话"""
        return [
            {"session_id": session_id, "created_at": data["created_at"]} 
            for session_id, data in self._data["sessions"].items()
        ]
        
    def view_session_id(self, session_id: str = None) -> Dict:
        """
        查看特定会话ID的详情
        
        Args:
            session_id: 会话ID，如果为None则使用初始化时指定的ID
        """
        # 使用提供的会话ID或初始化时设置的ID
        sid = session_id or self._session_id
        if not sid:
            raise ValueError("必须提供会话ID")
            
        return self._data["sessions"].get(sid)
        
    def load_session(self, session_id: str = None, update: bool = False):
        """
        加载会话
        
        Args:
            session_id: 会话ID，如果为None则使用初始化时指定的ID
            update: 是否创建新的会话ID
            
        Returns:
            Session实例
        """
        # 使用提供的会话ID或初始化时设置的ID
        sid = session_id or self._session_id
        if not sid:
            raise ValueError("必须提供会话ID")
            
        session_data = self.view_session_id(sid)
        
        if not session_data:
            raise ValueError(f"会话ID不存在: {sid}")
        
        # 获取Session类
        Session = get_session_class()
            
        # 创建新会话
        session = Session(self._client)
        
        # 设置会话数据
        session._messages = session_data["messages"]
        session._kwargs = session_data["params"]
        
        if not update:
            # 保持原会话ID
            session.session_id = sid
            session.created_at = session_data["created_at"]
        
        return session 