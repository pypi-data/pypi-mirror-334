"""
callai 数据库存储模块 - 提供SQLite会话存储功能
"""

import json
import sqlite3
from typing import Dict, List

# 动态导入，避免循环引用
def get_session_class():
    from ..session import Session
    return Session

class SessionDB:
    """会话数据库管理类（SQLite版本）"""
    
    def __init__(self, client, db_path: str, table_name: str = "ai_messages", session_id: str = None):
        """
        初始化会话数据库
        
        Args:
            client: Client实例
            db_path: 数据库文件路径
            table_name: 表名
            session_id: 会话ID（可选）
        """
        self._client = client
        self._db_path = db_path
        self._table_name = table_name
        self._session_id = session_id
        self._init_db()
        
    def _init_db(self):
        """初始化数据库"""
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        
        # 创建会话表
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {self._table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            created_at TEXT NOT NULL,
            messages TEXT NOT NULL,
            params TEXT NOT NULL
        )
        ''')
        
        conn.commit()
        conn.close()
        
    def save_session(self, session):
        """保存会话到数据库"""
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        
        # 将会话数据序列化为JSON
        session_data = session.to_dict()
        
        # 检查会话是否已存在
        cursor.execute(
            f"SELECT id FROM {self._table_name} WHERE session_id = ?", 
            (session_data["session_id"],)
        )
        result = cursor.fetchone()
        
        if result:
            # 更新现有会话
            cursor.execute(
                f"UPDATE {self._table_name} SET messages = ?, params = ? WHERE session_id = ?",
                (
                    json.dumps(session_data["messages"]), 
                    json.dumps(session_data["params"]),
                    session_data["session_id"]
                )
            )
        else:
            # 添加新会话
            cursor.execute(
                f"INSERT INTO {self._table_name} (session_id, created_at, messages, params) VALUES (?, ?, ?, ?)",
                (
                    session_data["session_id"],
                    session_data["created_at"],
                    json.dumps(session_data["messages"]),
                    json.dumps(session_data["params"])
                )
            )
        
        conn.commit()
        conn.close()
        
    def view_sessions(self) -> List[Dict]:
        """查看所有会话"""
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            f"SELECT session_id, created_at FROM {self._table_name} ORDER BY created_at DESC"
        )
        
        sessions = [{"session_id": row[0], "created_at": row[1]} for row in cursor.fetchall()]
        
        conn.close()
        return sessions
        
    def view_session_id(self, session_id: str = None) -> Dict:
        """
        查看特定会话ID的详情
        
        Args:
            session_id: 会话ID，如果为None则使用初始化时指定的ID
        """
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        
        # 使用提供的会话ID或初始化时设置的ID
        sid = session_id or self._session_id
        if not sid:
            conn.close()
            raise ValueError("必须提供会话ID")
        
        cursor.execute(
            f"SELECT session_id, created_at, messages, params FROM {self._table_name} WHERE session_id = ?",
            (sid,)
        )
        
        result = cursor.fetchone()
        
        conn.close()
        
        if not result:
            return None
            
        return {
            "session_id": result[0],
            "created_at": result[1],
            "messages": json.loads(result[2]),
            "params": json.loads(result[3])
        }
        
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