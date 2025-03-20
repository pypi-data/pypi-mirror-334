"""
callai Function Calling模块 - 提供工具调用功能
"""

import inspect
import json
from typing import Dict, List, Any, Callable, Union, Optional

class Tool:
    """
    工具类，用于定义可被AI调用的函数
    """
    
    def __init__(self, 
                 func: Callable, 
                 name: str = None, 
                 description: str = None,
                 parameters: Dict = None):
        """
        初始化工具
        
        Args:
            func: 工具函数
            name: 工具名称(默认使用函数名)
            description: 工具描述(默认使用函数文档)
            parameters: 工具参数定义(默认从函数签名生成)
        """
        self.func = func
        self.name = name or func.__name__
        self.description = description or (func.__doc__ or "").strip()
        
        # 如果没有提供参数定义，尝试从函数签名生成
        if parameters is None:
            parameters = self._generate_parameters_from_signature()
        self.parameters = parameters
    
    def _generate_parameters_from_signature(self) -> Dict:
        """从函数签名生成参数定义"""
        sig = inspect.signature(self.func)
        parameters = {
            "type": "object",
            "properties": {},
            "required": []
        }
        
        for name, param in sig.parameters.items():
            # 忽略self参数
            if name == "self":
                continue
                
            # 检查是否有注解
            annotation = param.annotation
            param_type = "string"  # 默认类型
            
            # 检查参数类型
            if annotation != inspect.Parameter.empty:
                if annotation == str:
                    param_type = "string"
                elif annotation == int:
                    param_type = "integer"
                elif annotation == float:
                    param_type = "number"
                elif annotation == bool:
                    param_type = "boolean"
                elif annotation == list or annotation == List:
                    param_type = "array"
                elif annotation == dict or annotation == Dict:
                    param_type = "object"
            
            # 添加参数属性
            parameters["properties"][name] = {
                "type": param_type,
                "description": f"参数 {name}"
            }
            
            # 如果参数没有默认值，则为必需参数
            if param.default == inspect.Parameter.empty:
                parameters["required"].append(name)
        
        return parameters
    
    def to_dict(self) -> Dict:
        """转换为OpenAI格式的工具定义"""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters
            }
        }
    
    def __call__(self, *args, **kwargs):
        """调用工具函数"""
        return self.func(*args, **kwargs)


class ToolRegistry:
    """
    工具注册表，管理所有可用的工具
    """
    
    def __init__(self):
        """初始化工具注册表"""
        self.tools = {}
    
    def register(self, tool: Union[Tool, Callable], **kwargs) -> Tool:
        """
        注册工具
        
        Args:
            tool: 工具对象或工具函数
            **kwargs: 如果工具是函数，这些参数会传递给Tool构造函数
            
        Returns:
            注册的工具对象
        """
        if not isinstance(tool, Tool):
            tool = Tool(tool, **kwargs)
        
        self.tools[tool.name] = tool
        return tool
    
    def get(self, name: str) -> Optional[Tool]:
        """获取工具"""
        return self.tools.get(name)
    
    def list_tools(self) -> List[Dict]:
        """获取OpenAI格式的工具列表"""
        return [tool.to_dict() for tool in self.tools.values()]
    
    def execute_tool_call(self, tool_call: Any) -> Any:
        """
        执行工具调用
        
        Args:
            tool_call: 工具调用信息，可能是字典或ChatCompletionMessageToolCall对象
                
        Returns:
            工具执行结果
        """
        # 处理ChatCompletionMessageToolCall对象或字典
        try:
            # 如果是字典形式
            if isinstance(tool_call, dict):
                function_name = tool_call["function"]["name"]
                arguments_str = tool_call["function"]["arguments"]
            else:
                # 如果是ChatCompletionMessageToolCall对象
                function_name = tool_call.function.name
                arguments_str = tool_call.function.arguments
        except (KeyError, AttributeError) as e:
            raise ValueError(f"无效的工具调用格式: {e}")
        
        # 获取工具
        tool = self.get(function_name)
        if not tool:
            raise ValueError(f"未找到工具: {function_name}")
        
        # 处理空参数情况
        if not arguments_str or arguments_str.strip() == "":
            # 对于无参数的函数，使用空字典
            return tool()
        
        # 解析参数
        try:
            arguments = json.loads(arguments_str)
        except json.JSONDecodeError:
            # 如果JSON解析失败，尝试修复常见问题
            # 1. 尝试添加缺失的花括号
            if not arguments_str.strip().startswith("{"):
                arguments_str = "{" + arguments_str
            if not arguments_str.strip().endswith("}"):
                arguments_str = arguments_str + "}"
                
            try:
                arguments = json.loads(arguments_str)
            except json.JSONDecodeError as e:
                raise ValueError(f"无法解析工具参数: {e}\n参数内容: {arguments_str}")
        
        # 执行工具
        return tool(**arguments)


# 全局工具注册表
registry = ToolRegistry()

def register_tool(func=None, **kwargs):
    """
    注册工具的装饰器
    
    Args:
        func: 要注册的函数
        **kwargs: 传递给Tool构造函数的参数
        
    Returns:
        装饰后的函数或装饰器
    """
    def decorator(f):
        registry.register(f, **kwargs)
        return f
    
    if func is None:
        return decorator
    return decorator(func) 