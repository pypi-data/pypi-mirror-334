"""
callai API模块 - 提供底层API接口封装
"""

from typing import Dict, List, Optional, Union, Any, Iterator

try:
    from openai.types.chat import ChatCompletion, ChatCompletionChunk
except ImportError:
    raise ImportError("请安装openai包: pip install openai>=1.0.0")


class ChatCompletions:
    """封装聊天补全API"""
    
    def __init__(self, client):
        self._client = client
        self._openai_client = client._openai_client
        
    def create(self, 
               model: str = None,
               messages: List[Dict[str, str]] = None,
               temperature: float = None,
               top_p: float = None,
               n: int = None,
               stream: bool = None,
               max_tokens: int = None,
               presence_penalty: float = None,
               frequency_penalty: float = None,
               logit_bias: Dict[str, float] = None,
               user: str = None,
               **kwargs) -> Union[ChatCompletion, Iterator[ChatCompletionChunk]]:
        """
        创建聊天补全，兼容OpenAI的接口
        
        Args:
            model: 模型名称，如果未提供则使用客户端默认值
            messages: 消息列表
            temperature: 温度参数
            top_p: 核采样参数
            n: 生成的回复数量
            stream: 是否流式返回
            max_tokens: 最大生成token数
            presence_penalty: 存在惩罚
            frequency_penalty: 频率惩罚
            logit_bias: 词元偏置
            user: 用户标识
            **kwargs: 其他参数
            
        Returns:
            ChatCompletion或ChatCompletionChunk的迭代器
        """
        # 使用客户端默认值替换None参数
        if model is None:
            model = self._client.default_model
            
        # 调用OpenAI客户端
        return self._openai_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            top_p=top_p,
            n=n,
            stream=stream,
            max_tokens=max_tokens,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            logit_bias=logit_bias,
            user=user,
            **kwargs
        )


class Chat:
    """封装聊天API"""
    
    def __init__(self, client):
        self._client = client
        self.completions = ChatCompletions(client) 