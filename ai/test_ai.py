from openai import OpenAI
import json

# 初始化 Moonshot AI 客户端
client = OpenAI(
    api_key="sk-1fPmr7wLVZy1QlPBPfBXB3bSO5Wc3UPBvTi8tSGfL7FYwyMe",
    base_url="https://api.moonshot.cn/v1",
)

# 预设事件列表
event_list = ["锻炼", "学习", "打工"]

# 角色初始属性
character_stats = {
    "智力": 50,
    "生命值": 100,
    "攻击力": 30
}

def match_event(user_input):
    # 构造提示，要求 AI 从事件列表中选择最匹配的事件
    prompt = f"""
    用户输入了一个事件：'{user_input}'。
    请从以下事件列表中选择最匹配的事件：{event_list}。
    只返回匹配的事件名称（例如：锻炼），不要返回其他内容。
    如果没有明确匹配，基于语义选择最接近的事件。
    """
    
    # 调用 Kimi 模型进行事件匹配
    completion = client.chat.completions.create(
        model="kimi-k2-0711-preview",
        messages=[
            {
                "role": "system",
                "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，擅长中文对话。你会为用户提供准确的回答，并从给定列表中选择最匹配的选项。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.6,
    )
    
    # 获取 AI 返回的匹配事件
    matched_event = completion.choices[0].message.content.strip()
    return matched_event

def update_stats(matched_event):
    # 根据匹配的事件更新角色属性
    if matched_event == "锻炼":
        character_stats["生命值"] += 10
        print(f"事件匹配：{matched_event}，生命值 +10！")
    if matched_event == "学习":
        character_stats["智力"] += 10
        print(f"事件匹配：{matched_event}，智力 +10！")
    if  matched_event == "打工":
        character_stats["生命值"] -= 10
        print(f"事件匹配：{matched_event}，生命值 -10！")
    
    # 返回更新后的角色属性
    return character_stats

def main():
    # 获取用户输入
    user_input = input("请输入一个事件（例如：去跑步）：")
    
    # 匹配事件
    matched_event = match_event(user_input)
    
    # 更新角色属性
    updated_stats = update_stats(matched_event)
    
    # 打印角色最新属性
    print("角色当前属性：")
    print(json.dumps(updated_stats, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()