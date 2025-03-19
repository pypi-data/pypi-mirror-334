# CallAI

一个简单的OpenAI API兼容封装库，提供简洁的接口对外暴露，完全兼容原生openai包的调用方式。

## 特点

- 完全兼容OpenAI客户端API
- 提供简单易用的封装接口（ask、stream_ask、think、ask_json）
- 支持会话管理（自动跟踪上下文）
- 支持会话持久化（SQLite和JSON格式）
- 支持思考模式（获取模型的推理过程和最终答案）
- 支持代理配置（适用于网络受限环境）
- 支持Function Calling功能（允许AI调用工具函数）
- 自动处理API认证和配置
- 支持标准和流式响应

## 安装

```bash
pip install -e .
```

或者

```bash
python setup.py install
```

## 快速开始

### 初始化客户端

```python
import os
from callai import AI, Client, OpenAI

# 方法1：使用AI类（推荐）
client = AI(
    api_key=os.environ.get("API_KEY"),
    base_url="https://api.example.com/v1",
    default_model="model-name",
    # 可选：设置代理
    proxies={
        "http": "http://127.0.0.1:7890",
        "https": "http://127.0.0.1:7890"
    }
)

# 方法2：使用Client类
client = Client(
    api_key=os.environ.get("API_KEY"),
    base_url="https://api.example.com/v1",
    default_model="model-name"
)

# 方法3：使用与OpenAI库兼容的类名
client = OpenAI(
    api_key=os.environ.get("API_KEY"),
    base_url="https://api.example.com/v1",
    default_model="model-name"
)
```

### 代理设置

如果你需要使用代理服务器，可以在初始化客户端时指定代理：

```python
from callai import AI

client = AI(
    api_key="your-api-key",
    base_url="https://api.example.com/v1",
    # 设置HTTP和HTTPS代理
    proxies={
        "http": "http://127.0.0.1:7890",
        "https": "http://127.0.0.1:7890"
    }
    # 或者使用SOCKS代理
    # proxies={
    #     "http": "socks5://127.0.0.1:1080",
    #     "https": "socks5://127.0.0.1:1080"
    # }
)
```

注意：使用SOCKS代理需要安装额外的依赖：`pip install httpx[socks]`

### 简单接口

最简单的方式是使用封装好的方法：

```python
# 简单提问
response = client.ask("请介绍一下自己")
print(response)

# 流式响应
for chunk in client.stream_ask("请列举5种编程语言"):
    print(chunk, end="")

# 获取JSON格式回答
json_data = client.ask_json("提供五种编程语言及其特点")
print(json_data)  # 这是一个Python字典
```

### 思考模式

思考模式可以获取模型的推理过程和最终答案：

```python
# 标准思考模式（返回思考过程和答案）
result = client.think("9.9和9.11哪个更大？")
print("思考过程:", result["reasoning"])
print("答案:", result["answer"])

# 流式思考模式（实时获取思考过程和答案）
for chunk in client.stream_think("计算1234 * 5678"):
    if chunk["type"] == "reasoning":
        print("思考中:", chunk["content"], end="")
    elif chunk["type"] == "answer":
        print("回答:", chunk["content"], end="")
```

### Function Calling（工具调用）

Function Calling功能允许AI调用用户定义的工具函数：

```python
from callai import AI
from callai.function_calling import register_tool

# 注册工具函数
@register_tool
def get_weather(location: str, unit: str = "celsius"):
    """获取指定位置的天气
    
    Args:
        location: 城市名称
        unit: 温度单位，可以是celsius或fahrenheit
    """
    # 这里模拟天气API调用
    return {
        "location": location,
        "temperature": 22 if unit == "celsius" else 72,
        "unit": unit,
        "condition": "晴天"
    }

# 创建客户端
client = AI(api_key="your-api-key")

# 使用工具调用
response = client.call_with_tools(
    prompt="北京今天天气怎么样？",
    model="gpt-3.5-turbo"  # 确保使用支持函数调用的模型
)

print("AI回答:", response["content"])
print("工具调用:", response["tool_calls"])
print("函数结果:", response["function_results"])

# 流式工具调用
for event in client.stream_call_with_tools(
    prompt="上海和北京的天气分别是什么？",
    model="gpt-3.5-turbo"
):
    if event["type"] == "content":
        print("AI:", event["content"])
    elif event["type"] == "tool_call_start":
        print(f"开始调用工具: {event.get('tool_call_id')}")
    elif event["type"] == "tool_result":
        print(f"工具结果: {event.get('result')}")
```

更多详细用法请参考[example_tools.py](./examples/example_tools.py)示例文件。

### 会话接口

会话接口可以自动维护对话上下文：

```python
# 创建会话
session = client.session(
    system_prompt="你是一位Python编程专家",
    temperature=0.7  # 会话级别的默认参数
)

# 第一个问题
response = session.ask("如何在Python中处理JSON数据？")
print(response)

# 后续问题（自动保持上下文）
response = session.ask("有没有更高效的方法？")
print(response)

# 流式会话问答
for chunk in session.stream_ask("能给个代码示例吗？"):
    print(chunk, end="")

# 会话中使用思考模式
result = session.think("这种方法有什么潜在问题？")
print("思考过程:", result["reasoning"])
print("答案:", result["answer"])

# 会话中流式思考
for chunk in session.stream_think("如何优化这段代码？"):
    if chunk["type"] == "reasoning":
        print("思考:", chunk["content"], end="")
    elif chunk["type"] == "answer":
        print("回答:", chunk["content"], end="")

# 会话中请求JSON格式回答
json_data = session.ask_json("列出5个常用的JSON处理库")
print(json_data)
```

### 会话管理

可以持久化保存会话状态：

```python
# 使用SQLite数据库管理会话
db = client.load_db("sessions.db")

# 保存当前会话
db.save_session(session)

# 查看所有会话
sessions = db.view_sessions()
for s in sessions:
    print(f"会话ID: {s['session_id']}, 创建时间: {s['created_at']}")

# 查看特定会话详情
session_details = db.view_session_id(session.session_id)

# 加载已有会话
loaded_session = db.load_session(session.session_id)

# 使用JSON文件管理会话
js = client.load_json("sessions.json")
js.save_session(session)
```

### 兼容OpenAI原生接口

```python
# 使用与原生OpenAI库相同的调用方式
completion = client.chat.completions.create(
    model="another-model",  # 覆盖默认模型
    messages=[
        {"role": "system", "content": "你是人工智能助手"},
        {"role": "user", "content": "你好，请介绍一下自己"},
    ],
)
print(completion.choices[0].message.content)
```

## 示例

- [example.py](./example.py) - 基本使用示例
- [example_think.py](./example_think.py) - 思考模式示例
- [examples/example_tools.py](./examples/example_tools.py) - Function Calling示例

## 依赖

- Python 3.6+
- openai >= 1.0.0
- httpx >= 0.23.0
- sqlite3 (Python标准库)

## 可选依赖

- httpx[socks] - 如果你需要使用SOCKS代理 