"""
callai 思考模式示例
"""

import os
from callai import AI

api_key = os.environ.get("OPENAI_API_KEY")

# 初始化客户端
client = AI(
    api_key=api_key,
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    default_model="deepseek-r1-distill-qwen-7b-250120",
)

# ===== 示例1: 简单的think方法 =====
print("\n===== 使用think方法 =====")
question = "9.9和9.11哪个更大？"
print(f"问题: {question}")

# 调用think方法获取思考过程和回答
result = client.think(question)

# 打印结果
print("\n思考过程:")
print(result["reasoning"])
print("\n回答:")
print(result["answer"])


# ===== 示例2: 使用stream_think方法查看实时思考过程 =====
print("\n\n===== 使用stream_think方法 =====")
question = "计算3126乘以567等于多少？"
print(f"问题: {question}")

# 用于收集完整思考过程和回答
full_reasoning = ""
full_answer = ""
mode = "reasoning"  # 当前模式

print("\n实时输出:")
for chunk in client.stream_think(question):
    # 切换模式
    if chunk["type"] == "switch_to_answer":
        mode = "answer"
        print("\n--- 开始回答 ---\n")
        continue
        
    if chunk["type"] == "reasoning":
        full_reasoning += chunk["content"]
        print(chunk["content"], end="", flush=True)
    elif chunk["type"] == "answer":
        full_answer += chunk["content"]
        print(chunk["content"], end="", flush=True)

print("\n\n完整思考过程:")
print(full_reasoning)
print("\n完整回答:")
print(full_answer)


# ===== 示例3: 使用会话进行思考 =====
print("\n\n===== 在会话中使用思考 =====")

# 创建会话
session = client.session("你是一个擅长数学的助手")
print("(已创建会话)")

# 第一个问题
question = "如何计算复利？"
print(f"\n问题1: {question}")

# 使用think方法
result = session.think(question)
print("\n思考过程:")
print(result["reasoning"])
print("\n回答:")
print(result["answer"])

# 第二个问题(会保持上下文)
question = "年利率5%，10年后本金会增加多少？"
print(f"\n问题2: {question}")

# 使用stream_think方法
print("\n实时输出:")
full_answer = ""
for chunk in session.stream_think(question):
    if chunk["type"] == "switch_to_answer" and full_answer == "":
        print("\n--- 开始回答 ---\n")
    
    # 简单输出所有内容
    if "content" in chunk and chunk["content"]:
        print(chunk["content"], end="", flush=True)
        if chunk["type"] == "answer":
            full_answer += chunk["content"]

# 打印完整对话历史
print("\n\n会话历史:")
for i, msg in enumerate(session.get_messages()):
    role = "系统" if msg["role"] == "system" else "用户" if msg["role"] == "user" else "助手"
    print(f"{i+1}. [{role}] {msg['content'][:50]}..." if len(msg["content"]) > 50 else f"{i+1}. [{role}] {msg['content']}") 