"""
示例：使用callai的Function Calling功能

这个示例展示了如何设置和使用callai的工具调用功能。
"""

import os
import json
import requests
import traceback
import sys
import time
from datetime import datetime
from callai import AI
from callai.function_calling import register_tool

# 设置API密钥
api_key = os.environ.get("OPENAI_API_KEY", "your-api-key")

# 创建AI客户端
ai = AI(
    api_key=api_key,
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    default_model="doubao-1-5-lite-32k-250115",
)

# 定义工具函数

@register_tool
def get_current_weather(location: str = "", unit: str = "celsius"):
    """
    获取指定位置的当前天气
    
    Args:
        location: 城市名称
        unit: 温度单位，可以是celsius（摄氏度）或fahrenheit（华氏度）
    
    Returns:
        包含天气信息的字典
    """
    # 这是一个模拟的天气API调用
    # 在实际应用中，您可能需要调用真实的天气API
    print(f"获取{location or '未指定位置'}的天气信息，单位：{unit}")
    
    # 如果未提供位置，返回默认值
    if not location:
        location = "默认城市"
    
    # 模拟的响应
    return {
        "location": location,
        "temperature": 22 if unit == "celsius" else 72,
        "unit": unit,
        "forecast": ["晴天", "多云"],
        "humidity": 70,
        "wind_speed": 10
    }

@register_tool
def get_current_time(timezone: str = "UTC"):
    """
    获取当前时间
    
    Args:
        timezone: 时区，例如UTC、Asia/Shanghai等
    
    Returns:
        当前时间字符串
    """
    # 在实际应用中，您可能需要处理不同的时区
    now = datetime.now()
    return f"当前时间是：{now.strftime('%Y-%m-%d %H:%M:%S')}，时区：{timezone}"

@register_tool(name="search_database", description="搜索数据库中的信息")
def search_db(query: str = "", limit: int = 5):
    """
    搜索数据库
    
    Args:
        query: 搜索关键词
        limit: 返回结果数量限制
    
    Returns:
        搜索结果列表
    """
    print(f"搜索数据库：{query or '未指定关键词'}，限制：{limit}条结果")
    
    # 如果未提供查询关键词，使用默认值
    if not query:
        query = "通用查询"
    
    # 模拟的搜索结果
    results = [
        {"id": 1, "title": "人工智能简介", "content": f"AI是模拟人类智能的技术... 关键词:{query}"},
        {"id": 2, "title": "机器学习基础", "content": f"机器学习是AI的一个子领域... 关键词:{query}"},
        {"id": 3, "title": "深度学习应用", "content": f"深度学习在图像识别领域取得了突破... 关键词:{query}"}
    ]
    
    return results[:min(limit, len(results))]

def print_safe_json(obj):
    """安全打印JSON对象，处理序列化错误"""
    try:
        return json.dumps(obj, indent=2, ensure_ascii=False)
    except:
        if isinstance(obj, dict):
            return "{" + ", ".join(f'"{k}": (无法序列化的对象)' for k in obj.keys()) + "}"
        elif isinstance(obj, list):
            return f"[{len(obj)}个项目]"
        else:
            return str(obj)

# 示例1：基本工具调用
print("\n=== 示例1：基本工具调用 ===")
try:
    response = ai.call_with_tools(
        prompt="上海现在天气怎么样？今天几点了？",
    )

    print("AI回答:", response["content"])
    
    # 安全打印工具调用和结果
    if response["tool_calls"]:
        print("工具调用:")
        for tool_call in response["tool_calls"]:
            print(f"  - {print_safe_json(tool_call)}")
    else:
        print("没有工具调用")
        
    if response["function_results"]:
        print("函数结果:")
        for result in response["function_results"]:
            print(f"  - ID: {result.get('id', 'unknown')}")
            print(f"    结果: {print_safe_json(result.get('result', ''))}")
    else:
        print("没有函数结果")
except Exception as e:
    print(f"错误: {str(e)}")
    print(traceback.format_exc())

# 示例2：流式工具调用 - 实时输出模式
print("\n=== 示例2：流式工具调用 (实时输出) ===")
try:
    # 记录状态
    ai_first_response = ""
    ai_final_response = ""
    in_second_round = False
    tool_results = []
    current_event = None
    
    # 使用彩色输出
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    PURPLE = "\033[95m"  # 新增紫色用于原始事件调试
    CYAN = "\033[96m"    # 青色用于突出显示
    RESET = "\033[0m"
    BOLD = "\033[1m"
    
    print(f"{BOLD}AI 第一轮回复:{RESET} ", end="", flush=True)
    
    # 使用更长的上下文查询来测试Qwen的长上下文能力
    prompt = """北京和上海的天气分别是什么？请同时查询一下数据库中关于人工智能的信息。
    另外，请提供一下当前的时间。请详细描述各城市的温度、湿度和天气状况，以及未来三天的天气预报。
    对于数据库查询，请重点关注最新的人工智能发展趋势和应用领域。"""
    
    for event in ai.stream_call_with_tools(
        prompt=prompt,
        temperature=0.7
    ):
        # 保存当前事件用于调试
        current_event = event
        
        # 安全获取事件类型，默认为空字符串
        event_type = event.get("type", "")
        
        # 调试模式：可以启用以查看完整事件内容
        debug_mode = False  # 设置为True以显示事件详情
        if debug_mode:
            print(f"\n{PURPLE}[DEBUG] Event: {print_safe_json(event)}{RESET}", file=sys.stderr)
        
        # 处理不同类型的事件
        if event_type == "content":
            # 实时输出AI初始回复内容，不中断，保持连续性
            content = event.get("content", "")
            if content:  # 确保内容不为空
                ai_first_response += content
                print(f"{GREEN}{content}{RESET}", end="", flush=True)
            
        elif event_type == "tool_calls_ready":
            # 工具调用准备就绪，美化分隔
            count = event.get("count", 0)
            print(f"\n\n{BOLD}{YELLOW}{'═' * 40}{RESET}")
            print(f"{BOLD}{YELLOW}✓ 收集到 {count} 个工具调用，准备执行{RESET}")
            print(f"{BOLD}{YELLOW}{'═' * 40}{RESET}\n")
            
        elif event_type == "tool_call_executing":
            # 执行工具调用
            index = event.get("index", 0)
            total = event.get("total", 1)
            name = event.get("name", "unknown")
            arguments = event.get("arguments", "{}")
            
            print(f"{BOLD}{BLUE}⚙ 执行工具 [{index+1}/{total}]: {name}{RESET}")
            # 显示参数，美化输出
            if arguments:
                try:
                    args = json.loads(arguments)
                    if args:
                        print(f"{BLUE}  参数:{RESET}")
                        for key, value in args.items():
                            print(f"{BLUE}   • {key}: {RESET}{value}")
                    else:
                        print(f"{BLUE}  无参数{RESET}")
                except json.JSONDecodeError:
                    print(f"{BLUE}  原始参数: {RESET}{arguments}")
                
        elif event_type == "tool_result":
            # 工具执行结果
            index = event.get("index", 0)
            name = event.get("name", "unknown")
            result = event.get("result", "")
            
            tool_results.append((name, result))
            print(f"{BOLD}{BLUE}✓ 工具 {name} 返回结果:{RESET}")
            
            # 格式化输出结果
            if isinstance(result, str):
                print(f"{BLUE}  {result}{RESET}")
            else:
                try:
                    formatted_result = json.dumps(result, indent=2, ensure_ascii=False)
                    for line in formatted_result.split("\n"):
                        print(f"{BLUE}  {line}{RESET}")
                except:
                    print(f"{BLUE}  {print_safe_json(result)}{RESET}")
            print()  # 添加空行增加可读性
            
        elif event_type == "tool_error":
            # 工具执行错误
            index = event.get("index", 0)
            name = event.get("name", "unknown")
            error = event.get("error", "")
            print(f"{BOLD}{RED}✗ 工具 {name} 执行错误: {RESET}")
            print(f"{RED}  {error}{RESET}\n")
            
        elif event_type == "second_round_start":
            # 开始第二轮对话
            in_second_round = True
            message = event.get("message", "正在生成最终回复...")
            print(f"\n{BOLD}{YELLOW}{'═' * 40}{RESET}")
            print(f"{BOLD}{YELLOW}➤ {message}{RESET}")
            print(f"{BOLD}{YELLOW}{'═' * 40}{RESET}\n")
            print(f"{BOLD}AI 最终回复:{RESET} ", end="", flush=True)
            
        elif event_type == "final_content":
            # 最终回复内容
            content = event.get("content", "")
            if content:  # 确保内容不为空
                ai_final_response += content
                print(f"{GREEN}{content}{RESET}", end="", flush=True)
            
        elif event_type == "error":
            # 错误信息
            message = event.get("message", "发生错误")
            print(f"\n\n{BOLD}{RED}[错误]: {message}{RESET}")
            
        elif event_type == "warning":
            # 警告信息
            message = event.get("message", "警告")
            print(f"\n\n{BOLD}{YELLOW}[警告]: {message}{RESET}")
            
        elif event_type == "no_tool_calls":
            # 没有工具调用
            message = event.get("message", "没有工具调用")
            print(f"\n\n{BOLD}{YELLOW}[信息]: {message}{RESET}")
        
        # 如果事件类型不在上述任何一种情况中，但不是空事件
        elif event:
            # 只在调试模式下输出未知事件类型，避免干扰正常输出
            print(f"\n{YELLOW}[未知事件类型: {event_type}]{RESET}")
            if debug_mode:
                print(f"{YELLOW}事件内容: {print_safe_json(event)}{RESET}")
        
        # 空事件或None
        elif event is None:
            # 只在调试模式下输出
            if debug_mode:
                print(f"\n{YELLOW}[空事件]{RESET}")
            
    print(f"\n\n{BOLD}{GREEN}✓ 完成{RESET}")
    
    # 显示结果摘要
    print(f"\n{BOLD}{YELLOW}{'═' * 40}{RESET}")
    print(f"{BOLD}{YELLOW}📋 结果摘要{RESET}")
    print(f"{BOLD}{YELLOW}{'═' * 40}{RESET}")
    
    if ai_first_response:
        print(f"\n{BOLD}第一轮AI回复:{RESET}")
        print(f"  {ai_first_response}")
        
    if ai_final_response:
        print(f"\n{BOLD}最终AI回复:{RESET}")
        print(f"  {ai_final_response}")
    
    if tool_results:
        print(f"\n{BOLD}工具调用结果:{RESET}")
        for i, (name, result) in enumerate(tool_results):
            print(f"{BOLD}{i+1}. {name}:{RESET}")
            if isinstance(result, str):
                print(f"   {result}")
            else:
                print(f"   {type(result).__name__} 对象: {print_safe_json(result)}")
    
    # 如果出现了异常事件或未预期的输出，显示调试信息
    if not (ai_first_response or ai_final_response) and not tool_results:
        print(f"\n{BOLD}{RED}警告: 未获得有效输出{RESET}")
        if current_event:
            print(f"{RED}最后一个事件: {print_safe_json(current_event)}{RESET}")
    
    print()  # 空行
    
except Exception as e:
    print(f"\n\n{RED}错误: {str(e)}{RESET}")
    print(f"{RED}{traceback.format_exc()}{RESET}")

# 示例3：使用系统提示语
print("\n=== 示例3：使用系统提示语 ===")
try:
    system_prompt = """你是一个天气助手，负责回答用户关于天气的问题。
尽可能使用get_current_weather工具获取天气信息。
数据返回后，以友好的方式向用户解释天气情况。"""

    response = ai.call_with_tools(
        prompt="深圳今天天气如何？",
        system_prompt=system_prompt,
    )

    print("AI回答:", response["content"])
    
    # 安全打印工具调用和结果
    if response["tool_calls"]:
        print("工具调用:")
        for tool_call in response["tool_calls"]:
            print(f"  - {print_safe_json(tool_call)}")
    else:
        print("没有工具调用")
        
    if response["function_results"]:
        print("函数结果:")
        for result in response["function_results"]:
            print(f"  - ID: {result.get('id', 'unknown')}")
            print(f"    结果: {print_safe_json(result.get('result', ''))}")
    else:
        print("没有函数结果")
except Exception as e:
    print(f"错误: {str(e)}")
    print(traceback.format_exc()) 