"""
callai客户端实现，提供与OpenAI兼容的接口和简化使用的便捷方法
"""

import os
import json
import re
import httpx
from typing import Dict, List, Optional, Union, Any, Iterator, Tuple, Callable

import warnings

try:
    from openai import OpenAI as OriginalOpenAI
except ImportError:
    raise ImportError(
        "请安装openai包: pip install openai>=1.0.0"
    )

from .api import Chat
from .session import Session
from .storage.db import SessionDB
from .storage.json_storage import SessionJSON
from .function_calling import Tool, registry


class Client:
    """callai客户端，提供兼容OpenAI的API接口和简化的调用方法"""
    
    def __init__(
        self, 
        api_key: str = None,
        base_url: str = None,
        default_model: str = None,
        proxies: Dict[str, str] = None,
        **kwargs
    ):
        """
        初始化callai客户端
        
        Args:
            api_key: API密钥，如果为None则从环境变量中读取
            base_url: API基础URL，可选
            default_model: 默认使用的模型
            proxies: 代理设置，如 {"http": "http://localhost:8080", "https": "http://localhost:8080"}
            **kwargs: 传递给OpenAI客户端的其他参数
        """
        # 从环境变量获取API密钥（如果未提供）
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            warnings.warn("未提供API密钥，请通过参数或环境变量OPENAI_API_KEY设置")
            
        # 保存默认模型
        self.default_model = default_model
        
        # 处理代理设置
        if proxies is not None:
            # 在新版openai库中，需要通过http_client参数设置代理
            http_client = httpx.Client(proxies=proxies)
            kwargs["http_client"] = http_client
        
        # 从kwargs中移除proxies参数，防止传递给OpenAI客户端
        if "proxies" in kwargs:
            kwargs.pop("proxies")
        
        # 初始化OpenAI客户端
        self._openai_client = OriginalOpenAI(
            api_key=self.api_key,
            base_url=base_url,
            **kwargs
        )
        
        # 初始化API命名空间
        self.chat = Chat(self)
        
    def __repr__(self):
        return f"callai.Client(base_url='{self._openai_client.base_url}')"
        
    def _create_messages(self, prompt=None, system_prompt=None, messages=None):
        """
        创建消息列表
        
        Args:
            prompt: 用户提问内容
            system_prompt: 系统提示语
            messages: 完整的消息列表
            
        Returns:
            消息列表
        """
        if messages:
            # 如果提供了消息列表，使用它
            msg_list = messages
        else:
            # 创建新的消息列表
            msg_list = []
            
            # 添加系统提示（如果有）
            if system_prompt:
                msg_list.append({"role": "system", "content": system_prompt})
                
            # 添加用户问题
            if prompt:
                msg_list.append({"role": "user", "content": prompt})
            else:
                raise ValueError("必须提供prompt或messages参数")
                
        return msg_list
        
    def ask(self, prompt=None, system_prompt=None, messages=None, **kwargs) -> str:
        """
        向AI发送问题并获取回答
        
        Args:
            prompt: 用户提问内容（与messages二选一）
            system_prompt: 系统提示语（可选）
            messages: 完整的消息列表（与prompt二选一）
            **kwargs: 其他参数，如model, temperature等
            
        Returns:
            AI的回答文本
        """
        msg_list = self._create_messages(prompt, system_prompt, messages)
        
        # 调用API
        response = self.chat.completions.create(
            messages=msg_list,
            **kwargs
        )
        
        return response.choices[0].message.content
        
    def stream_ask(self, prompt=None, system_prompt=None, messages=None, **kwargs) -> Iterator[str]:
        """
        流式方式向AI发送问题并获取回答
        
        Args:
            prompt: 用户提问内容（与messages二选一）
            system_prompt: 系统提示语（可选）
            messages: 完整的消息列表（与prompt二选一）
            **kwargs: 其他参数，如model, temperature等
            
        Returns:
            AI回答文本的迭代器
        """
        msg_list = self._create_messages(prompt, system_prompt, messages)
        
        # 调用流式API
        stream = self.chat.completions.create(
            messages=msg_list,
            stream=True,
            **kwargs
        )
        
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
                
    def think(self, prompt=None, system_prompt=None, messages=None, **kwargs) -> Dict[str, str]:
        """
        让AI思考问题并获取思考过程和回答
        
        此方法使用支持reasoning_content的API接口，获取AI的详细思考过程和最终回答
        
        Args:
            prompt: 用户提问内容（与messages二选一）
            system_prompt: 系统提示语（可选）
            messages: 完整的消息列表（与prompt二选一）
            **kwargs: 其他参数，如model, temperature等
            
        Returns:
            包含思考过程和回答的字典，如 {"reasoning": "思考过程", "answer": "最终回答"}
        """
        # 创建消息列表
        msg_list = self._create_messages(prompt, system_prompt, messages)
        
        # 确保stream=True，因为我们需要获取reasoning_content
        kwargs['stream'] = True
        
        # 调用流式API
        stream = self.chat.completions.create(
            messages=msg_list,
            **kwargs
        )
        
        reasoning_content = ""
        answer_content = ""
        is_answering = False
        
        for chunk in stream:
            if not chunk.choices:
                # 这可能是最后一个包含usage的chunk
                continue
                
            delta = chunk.choices[0].delta
            # 获取思考过程
            if hasattr(delta, 'reasoning_content') and delta.reasoning_content is not None:
                reasoning_content += delta.reasoning_content
            # 获取回答内容
            elif hasattr(delta, 'content') and delta.content is not None:
                answer_content += delta.content
                is_answering = True
        
        # 如果API不支持reasoning_content，则使用传统方法
        if not reasoning_content and answer_content:
            return {
                "reasoning": "API不支持获取思考过程",
                "answer": answer_content
            }
            
        # 如果没有获取到回答，则整个内容作为回答
        if not answer_content:
            answer_content = reasoning_content
            reasoning_content = ""
            
        return {
            "reasoning": reasoning_content,
            "answer": answer_content
        }
    
    def stream_think(self, prompt=None, system_prompt=None, messages=None, **kwargs) -> Iterator[Dict[str, str]]:
        """
        流式方式让AI思考问题并获取思考过程和回答
        
        此方法使用支持reasoning_content的API接口，以流式方式获取AI的详细思考过程和最终回答
        
        Args:
            prompt: 用户提问内容（与messages二选一）
            system_prompt: 系统提示语（可选）
            messages: 完整的消息列表（与prompt二选一）
            **kwargs: 其他参数，如model, temperature等
            
        Returns:
            包含内容类型和文本的字典迭代器，如 {"type": "reasoning" 或 "answer", "content": "文本片段"}
        """
        # 创建消息列表
        msg_list = self._create_messages(prompt, system_prompt, messages)
        
        # 确保stream=True，因为我们需要进行流式处理
        kwargs['stream'] = True
        
        # 调用流式API
        stream = self.chat.completions.create(
            messages=msg_list,
            **kwargs
        )
        
        is_answering = False
        
        for chunk in stream:
            if not chunk.choices:
                # 这可能是最后一个包含usage的chunk
                continue
                
            delta = chunk.choices[0].delta
            
            # 获取思考过程
            if hasattr(delta, 'reasoning_content') and delta.reasoning_content is not None and delta.reasoning_content != "":
                yield {"type": "reasoning", "content": delta.reasoning_content}
            
            # 获取回答内容
            elif hasattr(delta, 'content') and delta.content is not None and delta.content != "":
                if not is_answering:
                    # 第一次遇到content，表示开始回答
                    is_answering = True
                    # 可以选择性地发送一个标记事件，表示从思考转为回答
                    yield {"type": "switch_to_answer", "content": ""}
                
                yield {"type": "answer", "content": delta.content}
            
    def ask_json(self, prompt=None, system_prompt=None, messages=None, **kwargs) -> dict:
        """
        向AI发送问题并获取JSON格式回答
        
        Args:
            prompt: 用户提问内容（与messages二选一）
            system_prompt: 系统提示语（可选）
            messages: 完整的消息列表（与prompt二选一）
            **kwargs: 其他参数，如model, temperature等
            
        Returns:
            解析后的JSON对象
        """
        # 添加JSON格式指令
        if prompt:
            json_prompt = f"请以有效的JSON格式回答以下问题（不要有多余的文字说明）：\n\n{prompt}"
            response = self.ask(prompt=json_prompt, system_prompt=system_prompt, **kwargs)
        elif messages:
            # 如果是消息列表，在最后一条用户消息前添加JSON指令
            msg_list = messages.copy()
            for i in range(len(msg_list) - 1, -1, -1):
                if msg_list[i]["role"] == "user":
                    content = msg_list[i]["content"]
                    msg_list[i]["content"] = f"请以有效的JSON格式回答以下问题（不要有多余的文字说明）：\n\n{content}"
                    break
            response = self.ask(messages=msg_list, **kwargs)
        else:
            raise ValueError("必须提供prompt或messages参数")
            
        # 解析JSON
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            # 尝试提取可能被额外文本包围的JSON
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
    
    def call_with_tools(self, prompt=None, system_prompt=None, messages=None, tools=None, **kwargs) -> Dict:
        """
        使用工具调用功能向AI发送问题
        
        Args:
            prompt: 用户提问内容（与messages二选一）
            system_prompt: 系统提示语（可选）
            messages: 完整的消息列表（与prompt二选一）
            tools: 工具列表，如果为None则使用全局注册的所有工具
            **kwargs: 其他参数，如model, temperature等
            
        Returns:
            包含AI回答和工具调用信息的字典：
            {
                "content": "AI回答文本",
                "tool_calls": [工具调用信息],
                "function_results": [工具执行结果]
            }
        """
        # 创建初始消息列表
        msg_list = self._create_messages(prompt, system_prompt, messages)
        
        # 如果未提供工具，使用全局注册的所有工具
        if tools is None:
            tools = registry.list_tools()
        elif isinstance(tools, list) and all(isinstance(t, (Tool, Callable)) for t in tools):
            # 如果是Tool或函数对象列表，转换为OpenAI格式的工具列表
            tools = [t.to_dict() if isinstance(t, Tool) else Tool(t).to_dict() for t in tools]
            
        # 确保tool_choice设置为auto
        kwargs["tool_choice"] = kwargs.get("tool_choice", "auto")
        
        # 第一次调用API
        response = self.chat.completions.create(
            messages=msg_list,
            tools=tools,
            **kwargs
        )
        
        message = response.choices[0].message
        content = message.content or ""
        
        # 如果没有工具调用，直接返回结果
        if not hasattr(message, 'tool_calls') or not message.tool_calls:
            return {"content": content, "tool_calls": [], "function_results": []}
        
        # 收集工具调用信息
        tool_calls = message.tool_calls
        function_results = []
        
        # 执行每个工具调用
        tools_executed = []
        for tool_call in tool_calls:
            try:
                # 获取ID，同时处理字典或对象形式
                tool_call_id = tool_call.id if hasattr(tool_call, 'id') else tool_call.get("id", "unknown")
                
                # 跳过没有ID的工具调用
                if not tool_call_id or tool_call_id == "unknown":
                    continue
                    
                # 执行工具调用
                result = registry.execute_tool_call(tool_call)
                
                # 将结果添加到列表中
                function_result = {
                    "id": tool_call_id,
                    "result": result
                }
                function_results.append(function_result)
                
                # 添加工具执行结果到消息列表
                tools_executed.append({
                    "tool_call_id": tool_call_id,
                    "role": "tool",
                    "content": str(result) if not isinstance(result, str) else result
                })
                
            except Exception as e:
                # 获取ID，同时处理字典或对象形式
                tool_call_id = tool_call.id if hasattr(tool_call, 'id') else tool_call.get("id", "unknown")
                if tool_call_id and tool_call_id != "unknown":
                    function_results.append({
                        "id": tool_call_id,
                        "error": str(e)
                    })
                    # 添加错误信息到消息列表
                    tools_executed.append({
                        "tool_call_id": tool_call_id,
                        "role": "tool",
                        "content": f"Error: {str(e)}"
                    })
        
        # 如果有工具执行结果，添加到消息列表并再次调用模型
        if tools_executed:
            # 添加上一次模型的回复
            msg_list.append({
                "role": "assistant",
                "content": content,
                "tool_calls": [
                    {
                        "id": tc.id if hasattr(tc, 'id') else tc.get("id"),
                        "type": "function",
                        "function": {
                            "name": tc.function.name if hasattr(tc.function, 'name') else tc.get("function", {}).get("name"),
                            "arguments": tc.function.arguments if hasattr(tc.function, 'arguments') else tc.get("function", {}).get("arguments", "{}")
                        }
                    } for tc in tool_calls if hasattr(tc, 'id') or tc.get("id")
                ]
            })
            
            # 添加工具执行结果
            for tool_result in tools_executed:
                msg_list.append(tool_result)
            
            # 再次调用模型获取最终回复
            kwargs.pop("tools", None)  # 第二次调用不需要工具
            kwargs.pop("tool_choice", None)  # 第二次调用不需要工具选择
            
            final_response = self.chat.completions.create(
                messages=msg_list,
                **kwargs
            )
            
            final_content = final_response.choices[0].message.content or ""
            
            # 更新content为最终回复
            content = final_content
        
        # 为了保持API一致性，将tool_calls转换为可序列化的字典
        serializable_tool_calls = []
        for tc in tool_calls:
            if hasattr(tc, 'model_dump'):
                # 如果对象有model_dump方法（最新的Pydantic对象）
                serializable_tool_calls.append(tc.model_dump())
            elif hasattr(tc, 'to_dict'):
                # 如果对象有to_dict方法
                serializable_tool_calls.append(tc.to_dict())
            elif hasattr(tc, '__dict__'):
                # 尝试通过__dict__获取
                serializable_tool_calls.append(tc.__dict__)
            else:
                # 如果已经是字典或其他可序列化对象
                serializable_tool_calls.append(tc)
        
        return {
            "content": content,
            "tool_calls": serializable_tool_calls,
            "function_results": function_results
        }
    
    def stream_call_with_tools(self, prompt=None, system_prompt=None, messages=None, tools=None, **kwargs) -> Iterator[Dict]:
        """
        流式方式使用工具调用功能向AI发送问题
        
        Args:
            prompt: 用户提问内容（与messages二选一）
            system_prompt: 系统提示语（可选）
            messages: 完整的消息列表（与prompt二选一）
            tools: 工具列表，如果为None则使用全局注册的所有工具
            **kwargs: 其他参数，如model, temperature等
            
        Returns:
            包含事件类型和内容的字典迭代器，事件类型可能是：
            - "content": 常规内容 (第一轮)
            - "tool_calls_ready": 工具调用准备就绪
            - "tool_call_executing": 正在执行工具
            - "tool_result": 工具执行结果
            - "final_content": 最终回复内容 (第二轮)
        """
        # 创建初始消息列表
        msg_list = self._create_messages(prompt, system_prompt, messages)
        
        # 如果未提供工具，使用全局注册的所有工具
        if tools is None:
            tools = registry.list_tools()
        elif isinstance(tools, list) and all(isinstance(t, (Tool, Callable)) for t in tools):
            # 如果是Tool或函数对象列表，转换为OpenAI格式的工具列表
            tools = [t.to_dict() if isinstance(t, Tool) else Tool(t).to_dict() for t in tools]
            
        # 确保tool_choice设置为auto
        stream_param = kwargs.pop("stream", True)  # 移除stream参数，避免重复
        tool_choice = kwargs.pop("tool_choice", "auto")  # 移除tool_choice参数，后面会设置
        
        # 第一轮：调用流式API，仅收集模型输出
        round_one_kwargs = kwargs.copy()
        round_one_kwargs["stream"] = True
        round_one_kwargs["tool_choice"] = tool_choice
        
        # 第一轮：流式获取模型输出和工具调用意图
        try:
            first_stream = self.chat.completions.create(
                messages=msg_list,
                tools=tools,
                **round_one_kwargs
            )
        except Exception as e:
            yield {"type": "error", "message": f"调用API失败: {str(e)}"}
            return
        
        # 收集第一轮的完整回复
        first_response_text = ""
        collected_tool_calls = []
        current_tool_call = None
        
        # 流式输出第一轮结果
        try:
            for chunk in first_stream:
                if not chunk.choices:
                    continue
                    
                delta = chunk.choices[0].delta
                
                # 处理内容增量
                if hasattr(delta, 'content') and delta.content is not None:
                    content = delta.content
                    first_response_text += content
                    yield {"type": "content", "content": content}
                
                # 收集工具调用，但不立即执行
                if hasattr(delta, 'tool_calls') and delta.tool_calls:
                    for tool_call_delta in delta.tool_calls:
                        # 处理工具调用的ID
                        if hasattr(tool_call_delta, 'id') and tool_call_delta.id:
                            tool_call_id = tool_call_delta.id
                            index = getattr(tool_call_delta, 'index', 0)
                            
                            # 如果是新工具调用，创建一个新对象
                            if current_tool_call is None or current_tool_call.get('id') != tool_call_id:
                                current_tool_call = {
                                    "id": tool_call_id,
                                    "index": index,
                                    "type": "function",
                                    "function": {"name": "", "arguments": ""}
                                }
                                collected_tool_calls.append(current_tool_call)
                        
                        # 收集函数名称和参数
                        if hasattr(tool_call_delta, 'function'):
                            function_delta = tool_call_delta.function
                            if hasattr(function_delta, 'name') and function_delta.name:
                                current_tool_call["function"]["name"] = function_delta.name
                                
                            if hasattr(function_delta, 'arguments') and function_delta.arguments is not None:
                                current_tool_call["function"]["arguments"] += function_delta.arguments
        except Exception as e:
            yield {"type": "error", "message": f"处理流式响应时出错: {str(e)}"}
            return
        
        # 没有收集到任何内容，可能是API错误
        if not first_response_text and not collected_tool_calls:
            yield {"type": "error", "message": "未能从API获取有效响应"}
            return
            
        # 第一轮结束，通知用户工具调用准备就绪
        if collected_tool_calls:
            yield {"type": "tool_calls_ready", "count": len(collected_tool_calls)}
        
        # 第一轮的完整模型回复
        assistant_message = {
            "role": "assistant",
            "content": first_response_text,
            "tool_calls": []
        }
        
        # 检查和执行所有收集到的工具调用
        tools_executed = []
        
        for i, tool_call in enumerate(collected_tool_calls):
            tool_call_id = tool_call.get("id", "")
            function_name = tool_call.get("function", {}).get("name", "")
            arguments = tool_call.get("function", {}).get("arguments", "")
            
            yield {
                "type": "tool_call_executing", 
                "index": i,
                "total": len(collected_tool_calls),
                "name": function_name,
                "arguments": arguments
            }
            
            # 准备添加到assistant消息的工具调用
            assistant_tool_call = {
                "id": tool_call_id,
                "type": "function",
                "function": {
                    "name": function_name,
                    "arguments": arguments
                }
            }
            assistant_message["tool_calls"].append(assistant_tool_call)
            
            # 执行工具调用
            try:
                result = registry.execute_tool_call(tool_call)
                yield {
                    "type": "tool_result", 
                    "index": i,
                    "name": function_name,
                    "result": result
                }
                
                # 添加工具结果到tools_executed
                tools_executed.append({
                    "tool_call_id": tool_call_id,
                    "role": "tool",
                    "content": str(result) if not isinstance(result, str) else result
                })
                
            except Exception as e:
                error_message = str(e)
                yield {
                    "type": "tool_error", 
                    "index": i,
                    "name": function_name,
                    "error": error_message
                }
                
                # 添加错误结果
                tools_executed.append({
                    "tool_call_id": tool_call_id,
                    "role": "tool",
                    "content": f"Error: {error_message}"
                })
        
        # 如果有工具执行结果，进行第二轮对话
        if tools_executed:
            # 添加第一轮助手消息（包含工具调用）
            msg_list.append(assistant_message)
            
            # 添加工具执行结果
            for tool_result in tools_executed:
                msg_list.append(tool_result)
            
            # 准备第二轮调用参数
            round_two_kwargs = kwargs.copy()
            round_two_kwargs["stream"] = True  # 确保流式输出
            
            yield {"type": "second_round_start", "message": "正在生成最终回复..."}
            
            # 第二轮：流式获取最终回复
            try:
                final_stream = self.chat.completions.create(
                    messages=msg_list,
                    **round_two_kwargs
                )
                
                for chunk in final_stream:
                    if not chunk.choices:
                        continue
                        
                    delta = chunk.choices[0].delta
                    
                    # 处理内容增量
                    if hasattr(delta, 'content') and delta.content is not None:
                        yield {"type": "final_content", "content": delta.content}
            except Exception as e:
                yield {"type": "error", "message": f"第二轮对话失败: {str(e)}"}
        else:
            if collected_tool_calls:
                # 有工具调用但执行失败
                yield {"type": "warning", "message": "有工具调用，但执行失败或没有返回结果"}
            else:
                # 没有工具调用，使用第一轮的回复作为最终回复
                yield {"type": "no_tool_calls", "message": "没有工具调用，使用第一轮回复作为最终结果。"}
    
    def session(self, system_prompt: str = "你是人工智能助手", **kwargs) -> Session:
        """
        创建新的会话
        
        Args:
            system_prompt: 系统提示语
            **kwargs: 会话的默认参数，如model, temperature等
            
        Returns:
            Session实例
        """
        return Session(self, system_prompt, **kwargs)
        
    def load_db(self, db_path: str, table_name: str = "ai_messages", session_id: str = None) -> SessionDB:
        """
        加载数据库会话管理器
        
        Args:
            db_path: 数据库文件路径
            table_name: 表名
            session_id: 会话ID（可选）
            
        Returns:
            SessionDB实例
        """
        return SessionDB(self, db_path, table_name, session_id)
        
    def load_json(self, json_path: str, session_id: str = None) -> SessionJSON:
        """
        加载JSON文件会话管理器
        
        Args:
            json_path: JSON文件路径
            session_id: 会话ID（可选）
            
        Returns:
            SessionJSON实例
        """
        return SessionJSON(self, json_path, session_id)


# 为了兼容性，提供与OpenAI相同的类名
class AI(Client):
    """主要的AI客户端类，等同于Client"""
    pass
    
# 为了兼容性，提供与OpenAI相同的类名
class OpenAI(Client):
    """兼容OpenAI类名的客户端"""
    pass 