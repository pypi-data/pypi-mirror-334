"""
callai - 一个简单的OpenAI API兼容封装库
"""

from .client import Client, OpenAI, AI
from .session import Session
from .storage.db import SessionDB
from .storage.json_storage import SessionJSON

__all__ = [
    "Client", "OpenAI", "AI", 
    "Session", "SessionDB", "SessionJSON"
]

__version__ = "0.2.0" 