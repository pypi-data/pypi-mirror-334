"""
callai库使用示例
"""

import os
from callai import AI, OpenAI, Client, Session

print("===== 初始化客户端 =====")
# 获取API密钥
api_key = os.environ.get("OPENAI_API_KEY")

# 初始化客户端方式1: 使用AI类
client = AI(
    api_key=api_key,
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    default_model="doubao-1-5-lite-32k-250115",
)

# 方式2: 使用OpenAI类
# client = OpenAI(
#     api_key=api_key,
#     base_url="https://ark.cn-beijing.volces.com/api/v3",
#     default_model="doubao-pro-32k-241215"
# )

# 方式3: 使用Client类
# client = Client(
#     api_key=api_key,
#     base_url="https://ark.cn-beijing.volces.com/api/v3",
#     default_model="doubao-pro-32k-241215"
# )

print("\n===== 简单接口示例 =====")
print("----- 标准请求示例 -----")
# 直接提问
response = client.ask("常见的十字花科植物有哪些？")
print(response)

print("\n----- 流式请求示例 -----")
# 流式提问
for chunk in client.stream_ask("列举5种常见的编程语言及其特点？"):
    print(chunk, end="")
print()

print("\n----- 思考模式示例 -----")
# 思考模式
response = client.think("如何判断一个算法的时间复杂度？")
print("思考过程:")
print(response["reasoning"])
print("\n最终回答:")
print(response["answer"])

print("\n----- JSON格式返回示例 -----")
# 请求JSON格式
json_response = client.ask_json("请提供5种编程语言及其发明年份")
print(json_response)

print("\n===== 会话接口示例 =====")
# 创建一个会话
session = client.session(
    system_prompt="你是一位Python编程专家",
    temperature=0.7  # 可以设置会话级别的默认参数
)

# 会话提问
print("----- 会话提问1 -----")
response = session.ask("如何在Python中处理JSON数据？")
print(response)

print("\n----- 会话提问2 (自动保持上下文) -----")
response = session.ask("有没有更高效的方法？")
print(response)

print("\n----- 会话流式提问 -----")
for chunk in session.stream_ask("用代码示例说明如何解析嵌套的JSON？"):
    print(chunk, end="")
print()

print("\n===== 会话管理示例 =====")
print("----- 使用SQLite保存会话 -----")
# 使用数据库保存会话
db = client.load_db("sessions.db")
# 保存当前会话
db.save_session(session)
print(f"会话已保存，会话ID: {session.session_id}")

# 查看所有会话
print("\n所有会话:")
sessions = db.view_sessions()
for s in sessions:
    print(f"会话ID: {s['session_id']}, 创建时间: {s['created_at']}")
    
# 加载会话
if sessions:
    print(f"\n加载会话: {sessions[0]['session_id']}")
    loaded_session = db.load_session(sessions[0]['session_id'])
    response = loaded_session.ask("总结一下我们的对话")
    print(response)

print("\n----- 使用JSON保存会话 -----")
# 使用JSON保存会话
js = client.load_json("sessions.json")
# 保存会话
js.save_session(session)
print(f"会话已保存到JSON，会话ID: {session.session_id}")

# 兼容OpenAI原生接口
print("\n===== 兼容OpenAI原生接口 =====")
completion = client.chat.completions.create(
    messages=[
        {"role": "system", "content": "你是人工智能助手"},
        {"role": "user", "content": "请用一句话介绍自己"},
    ],
) 