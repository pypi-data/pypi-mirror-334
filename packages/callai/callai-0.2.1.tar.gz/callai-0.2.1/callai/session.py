"""
callai 会话功能模块 - 提供会话管理功能
"""

import json
import uuid
from typing import Dict, List, Union, Iterator
from datetime import datetime

class Session:
    """聊天会话类，维护会话上下文"""
    
    def __init__(self, client, system_prompt: str = "你是人工智能助手", **kwargs):
        """
        初始化会话
        
        Args:
            client: Client实例
            system_prompt: 系统提示语
            **kwargs: 会话的默认参数，如model, temperature等
        """
        self._client = client
        self._messages = [{"role": "system", "content": system_prompt}]
        self._kwargs = kwargs
        self.session_id = str(uuid.uuid4())
        self.created_at = datetime.now().isoformat()
        
    def _add_message(self, role: str, content: str):
        """添加消息到会话历史"""
        self._messages.append({"role": role, "content": content})
    
    def update(self, **kwargs):
        """
        更新会话参数
        
        Args:
            **kwargs: 要更新的参数，如system_prompt, temperature等
        """
        # 如果更新system_prompt，直接替换第一条消息
        if "system_prompt" in kwargs:
            system_prompt = kwargs.pop("system_prompt")
            if self._messages and self._messages[0]["role"] == "system":
                self._messages[0]["content"] = system_prompt
            else:
                self._messages.insert(0, {"role": "system", "content": system_prompt})
                
        # 更新其他参数
        self._kwargs.update(kwargs)
        
        return self
        
    def ask(self, prompt: str, system_prompt: str = None, **kwargs) -> str:
        """
        向AI发送问题并获取回答
        
        Args:
            prompt: 用户提问内容
            system_prompt: 可选，覆盖会话默认系统提示
            **kwargs: 覆盖会话默认参数
            
        Returns:
            AI的回答文本
        """
        # 如果提供了system_prompt，临时更新
        if system_prompt and self._messages[0]["role"] == "system":
            original_system = self._messages[0]["content"]
            self._messages[0]["content"] = system_prompt
        
        # 添加用户消息
        self._add_message("user", prompt)
        
        # 合并参数
        params = self._kwargs.copy()
        params.update(kwargs)
        
        # 调用API
        response = self._client.ask(messages=self._messages, **params)
        
        # 添加助手回复到历史
        self._add_message("assistant", response)
        
        # 恢复原始system_prompt
        if system_prompt and self._messages[0]["role"] == "system":
            self._messages[0]["content"] = original_system
        
        return response
        
    def stream_ask(self, prompt: str, system_prompt: str = None, **kwargs) -> Iterator[str]:
        """
        流式方式向AI发送问题并获取回答
        
        Args:
            prompt: 用户提问内容
            system_prompt: 可选，覆盖会话默认系统提示
            **kwargs: 覆盖会话默认参数
            
        Returns:
            AI回答文本的迭代器
        """
        # 如果提供了system_prompt，临时更新
        if system_prompt and self._messages[0]["role"] == "system":
            original_system = self._messages[0]["content"]
            self._messages[0]["content"] = system_prompt
        
        # 添加用户消息
        self._add_message("user", prompt)
        
        # 合并参数
        params = self._kwargs.copy()
        params.update(kwargs)
        
        # 收集完整回复
        full_response = ""
        
        # 调用流式API
        for chunk in self._client.stream_ask(messages=self._messages, **params):
            full_response += chunk
            yield chunk
            
        # 添加完整回复到历史
        self._add_message("assistant", full_response)
        
        # 恢复原始system_prompt
        if system_prompt and self._messages[0]["role"] == "system":
            self._messages[0]["content"] = original_system
    
    def think(self, prompt: str, system_prompt: str = None, **kwargs) -> Dict[str, str]:
        """
        让AI思考问题并获取思考过程和回答
        
        此方法使用支持reasoning_content的API接口，获取AI的详细思考过程和最终回答
        
        Args:
            prompt: 用户提问内容
            system_prompt: 可选，覆盖会话默认系统提示
            **kwargs: 覆盖会话默认参数
            
        Returns:
            包含思考过程和回答的字典，如 {"reasoning": "思考过程", "answer": "最终回答"}
        """
        # 如果提供了system_prompt，临时更新
        if system_prompt and self._messages[0]["role"] == "system":
            original_system = self._messages[0]["content"]
            self._messages[0]["content"] = system_prompt
            
        # 添加用户消息
        self._add_message("user", prompt)
        
        # 合并参数
        params = self._kwargs.copy()
        params.update(kwargs)
        
        # 调用think API
        result = self._client.think(messages=self._messages, **params)
        
        # 添加助手回复到历史（只记录最终答案）
        self._add_message("assistant", result["answer"])
        
        # 恢复原始system_prompt
        if system_prompt and self._messages[0]["role"] == "system":
            self._messages[0]["content"] = original_system
        
        return result
        
    def stream_think(self, prompt: str, system_prompt: str = None, **kwargs) -> Iterator[Dict[str, str]]:
        """
        流式方式让AI思考问题并获取思考过程和回答
        
        此方法使用支持reasoning_content的API接口，以流式方式获取AI的详细思考过程和最终回答
        
        Args:
            prompt: 用户提问内容
            system_prompt: 可选，覆盖会话默认系统提示
            **kwargs: 覆盖会话默认参数
            
        Returns:
            包含内容类型和文本的字典迭代器，如 {"type": "reasoning" 或 "answer", "content": "文本片段"}
        """
        # 如果提供了system_prompt，临时更新
        if system_prompt and self._messages[0]["role"] == "system":
            original_system = self._messages[0]["content"]
            self._messages[0]["content"] = system_prompt
        
        # 添加用户消息
        self._add_message("user", prompt)
        
        # 合并参数
        params = self._kwargs.copy()
        params.update(kwargs)
        
        # 收集完整回复
        full_answer = ""
        
        # 调用流式思考API
        for chunk in self._client.stream_think(messages=self._messages, **params):
            # 如果是回答部分，累积回答内容
            if chunk["type"] == "answer":
                full_answer += chunk["content"]
            # 所有内容都传递给调用者
            yield chunk
            
        # 添加完整回答到历史（只记录最终答案，不记录思考过程）
        self._add_message("assistant", full_answer)
        
        # 恢复原始system_prompt
        if system_prompt and self._messages[0]["role"] == "system":
            self._messages[0]["content"] = original_system
        
    def ask_json(self, prompt: str, system_prompt: str = None, **kwargs) -> dict:
        """
        向AI发送问题并获取JSON格式回答
        
        Args:
            prompt: 用户提问内容
            system_prompt: 可选，覆盖会话默认系统提示
            **kwargs: 覆盖会话默认参数
            
        Returns:
            解析后的JSON对象
        """
        # 如果提供了system_prompt，临时更新
        if system_prompt and self._messages[0]["role"] == "system":
            original_system = self._messages[0]["content"]
            self._messages[0]["content"] = system_prompt
            
        # 构建JSON指令提示语
        json_prompt = f"请以有效的JSON格式回答以下问题（不要有多余的文字说明）：\n\n{prompt}"
        self._add_message("user", json_prompt)
        
        # 合并参数
        params = self._kwargs.copy()
        params.update(kwargs)
        
        # 调用API
        response = self._client.ask(messages=self._messages, **params)
        
        # 添加助手回复到历史
        self._add_message("assistant", response)
        
        # 恢复原始system_prompt
        if system_prompt and self._messages[0]["role"] == "system":
            self._messages[0]["content"] = original_system
        
        # 解析JSON
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            # 尝试提取可能被额外文本包围的JSON
            import re
            json_pattern = r'```(?:json)?\s*([\s\S]*?)\s*```|(\{[\s\S]*\})'
            match = re.search(json_pattern, response)
            if match:
                json_str = match.group(1) or match.group(2)
                try:
                    return json.loads(json_str)
                except json.JSONDecodeError:
                    pass
            
            # 如果无法解析，返回原始文本作为字典
            return {"error": "无法解析为JSON", "text": response}
    
    def get_messages(self) -> List[Dict[str, str]]:
        """获取当前会话的所有消息"""
        return self._messages.copy()
    
    def to_dict(self) -> Dict:
        """将会话转换为字典"""
        return {
            "session_id": self.session_id,
            "created_at": self.created_at,
            "messages": self._messages,
            "params": self._kwargs
        } 