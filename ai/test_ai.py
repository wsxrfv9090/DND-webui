from openai import OpenAI
import json
import random
import math

# 初始化 Moonshot AI 客户端
client = OpenAI(
    api_key="sk-1fPmr7wLVZy1QlPBPfBXB3bSO5Wc3UPBvTi8tSGfL7FYwyMe",
    base_url="https://api.moonshot.cn/v1",
)

def analyze_action(user_input):
    """
    用AI分析用户输入，返回 (need_judge, skill_name, difficulty)
    - need_judge: True/False
    - skill_name: str 或 None
    - difficulty: int (0/1/2) 或 None
    """
    prompt = (
        f"你是一个TRPG规则裁判AI。用户输入一句话，请你判断：\n"
        f"1. 这句话是否需要技能判定？\n"
        f"2. 如果需要，应该用哪个技能？（技能名称必须严格来自技能列表）\n"
        f"3. 难度是普通(0)、困难(1)还是极难(2)？\n"
        f"请严格按照如下格式输出：True-技能名称-难度 或 False--\n"
        f"技能列表：信用评级、说服、侦查、心理学、闪避、格斗、射击、驾驶、图书馆使用、聆听、潜行、妙手、恐吓、法律、医学、急救、攀爬、跳跃、游泳、投掷、取悦、乔装、锁匠、机械维修、计算机使用 Ω、电子学 Ω、科学①、科学②、科学③、外语①、外语②、外语③、母语、历史、考古学、人类学、博物学、导航、神秘学、操作重型机械、爆破、炮术、催眠、读唇、动物驯养、学识、技艺①、技艺②、技艺③\n"
        f"用户输入：'{user_input}'"
    )
    completion = client.chat.completions.create(
        model="kimi-k2-0711-preview",
        messages=[
            {
                "role": "system",
                "content": "你是TRPG规则裁判AI，只输出结构化判定结果。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1,
    )
    ai_reply = completion.choices[0].message.content.strip()
    # 解析AI输出
    if ai_reply.startswith("True-"):
        parts = ai_reply.split("-")
        skill = parts[1] if len(parts) > 1 else None
        try:
            difficulty = int(parts[2]) if len(parts) > 2 else 0
        except Exception:
            difficulty = 0
        return True, skill, difficulty
    else:
        return False, None, None

def generate_description(user_input, judge_result=None):
    """
    用AI生成世界观下的描述。
    - user_input: 用户原话
    - judge_result: 判定结果描述（可选）
    """
    if judge_result:
        prompt = (
            f"你是TRPG世界观的叙述AI。用户刚才说：'{user_input}'，判定结果是：{judge_result}。请用生动的语言描述在这个世界观下发生了什么。"
        )
    else:
        prompt = (
            f"你是TRPG世界观的叙述AI。用户刚才说：'{user_input}'。请用生动的语言描述在这个世界观下发生了什么。"
        )
    completion = client.chat.completions.create(
        model="kimi-k2-0711-preview",
        messages=[
            {
                "role": "system",
                "content": "你是TRPG世界观的叙述AI，只输出故事描述。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
    )
    return completion.choices[0].message.content.strip()

def get_skill_success_rate(skill_name, skills_list):
    for skill in skills_list:
        if skill["技能名称"] == skill_name:
            return skill["成功率"]
    return 0

def judge(roll_result, success_rate, difficulty):
    if difficulty == 0:
        modifier = 1
    elif difficulty == 1:
        modifier = 1/2
    elif difficulty == 2:
        modifier = 1/5
    else:
        modifier = 1
    threshold = int(math.floor(success_rate * modifier))
    return roll_result <= threshold

def describe_action(user_input, skill_name, difficulty, roll_result, success):
    diff_map = {0: "普通", 1: "困难", 2: "极难"}
    outcome = "通过" if success else "不通过"
    return f"你尝试进行[{skill_name}]({diff_map.get(difficulty, '普通')})判定，骰点结果为{roll_result}，{outcome}。"
