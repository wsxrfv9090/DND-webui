from openai import OpenAI
import json
import random
import math

# 初始化 Moonshot AI 客户端
client = OpenAI(
    api_key="sk-1fPmr7wLVZy1QlPBPfBXB3bSO5Wc3UPBvTi8tSGfL7FYwyMe",
    base_url="https://api.moonshot.cn/v1",
)

def load_world_view():
    """
    加载世界观设定
    """
    with open('cache/world_view.txt', 'r', encoding='utf-8') as f:
         return f.read().strip()
  
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
        f"技能列表：会计、人类学、估价、考古学、技艺、取悦、攀爬、计算机使用 Ω、信用评级、乔装、闪避、汽车驾驶、电气维修、电子学 Ω、话术、格斗、射击、急救、历史、恐吓、跳跃、外语、母语、法律、图书馆使用、聆听、锁匠、机械维修、医学、博物学、导航、神秘学、操作重型机械、说服、驾驶、精神分析、心理学、骑术、科学、妙手、侦查、潜行、生存、游泳、投掷、追踪、动物驯养、潜水、爆破、读唇、催眠、炮术、学识\n"
        f"用户输入：'{user_input}'"
    )
    completion = client.chat.completions.create(
        model="kimi-k2-0711-preview",
        messages=[
            {
                "role": "system",
                "content": "你是TRPG规则裁判AI，只输出结构化判定结果。技能名称必须完全匹配技能列表中的名称。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1,
    )
    ai_reply = completion.choices[0].message.content.strip()
    print(f"AI分析结果: {ai_reply}")  # 添加调试输出
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

def generate_description(user_input, judge_result = None):
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

# ===== 新增接口：支持记忆系统集成 =====

def analyze_action_with_memory(user_input, complete_memory):
    """
    用AI分析用户输入，返回 (need_judge, skill_name, difficulty)
    支持传入完整记忆
    - user_input: 用户输入
    - complete_memory: 完整的记忆文本（世界观+动态状态）
    - 返回: (need_judge, skill_name, difficulty)
    """
    prompt = (
        f"这是当前的记忆：{complete_memory}\n\n"
        f"你是一个TRPG:Call of Cthulhu的规则裁判AI，基于上述世界观设定和当前游戏状态进行判定。用户输入一句话，请你判断：\n"
        f"1. 这句话是否需要技能判定？\n"
        f"2. 如果需要，应该用哪个技能？（技能名称必须严格来自技能列表）\n"
        f"3. 难度是普通(0)、困难(1)还是极难(2)？\n"
        f"请严格按照如下格式输出：True-技能名称-难度 或 False--\n"
        f"技能列表：会计、人类学、估价、考古学、技艺、取悦、攀爬、计算机使用 Ω、信用评级、乔装、闪避、汽车驾驶、电气维修、电子学 Ω、话术、格斗、射击、急救、历史、恐吓、跳跃、外语、母语、法律、图书馆使用、聆听、锁匠、机械维修、医学、博物学、导航、神秘学、操作重型机械、说服、驾驶、精神分析、心理学、骑术、科学、妙手、侦查、潜行、生存、游泳、投掷、追踪、动物驯养、潜水、爆破、读唇、催眠、炮术、学识\n"
        f"用户输入：'{user_input}'"
    )
    completion = client.chat.completions.create(
        model="kimi-k2-0711-preview",
        messages=[
            {
                "role": "system",
                "content": "你是TRPG:Call of Cthulhu的规则裁判AI，基于1920年代阿卡姆世界观和当前游戏状态进行判定，只输出结构化判定结果。"
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

def generate_description_with_memory(user_input, judge_result=None, complete_memory=None):
    """
    用AI生成世界观下的描述。
    传入完整记忆
    - user_input: 用户原话
    - judge_result: 判定结果描述（可选）
    - complete_memory: 完整的记忆文本（世界观+动态状态）
    """
    if complete_memory:
        # 使用完整记忆
        if judge_result:
            prompt = (
                f"这是当前的记忆：{complete_memory}\n\n"
                f"你是TRPG:Call of Cthulhu世界观的叙述AI。基于上述世界观设定和当前游戏状态，用户刚才说：'{user_input}'，判定结果是：{judge_result}。\n"
                f"请用生动的语言描述在1920年代阿卡姆小镇发生了什么，营造神秘而压抑的氛围，保持时代特色。注意根据当前游戏状态调整描述内容。"
            )
        else:
            prompt = (
                f"这是当前的记忆：{complete_memory}\n\n"
                f"你是TRPG:Call of Cthulhu世界观的叙述AI。基于上述世界观设定和当前游戏状态，用户刚才说：'{user_input}'。\n"
                f"请用生动的语言描述在1920年代阿卡姆小镇发生了什么，营造神秘而压抑的氛围，保持时代特色。注意根据当前游戏状态调整描述内容。"
            )
   
    completion = client.chat.completions.create(
        model="kimi-k2-0711-preview",
        messages=[
            {
                "role": "system",
                "content": "你是TRPG:Call of Cthulhu世界观的叙述AI，基于1920年代阿卡姆世界观进行描述，营造神秘而压抑的氛围。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
    )
    return completion.choices[0].message.content.strip()

def analyze_interaction_for_memory(user_input, ai_response):
    """
    分析玩家与AI的交互，提取需要更新到记忆系统的信息
    新增接口：用于长期记忆分析
    - user_input: 玩家输入
    - ai_response: AI的回应
    - 返回: 需要更新的状态字典
    """
    prompt = (
        f"你是长期记忆分析AI。请分析以下玩家与AI的交互，判断是否需要更新游戏状态：\n\n"
        f"玩家输入：{user_input}\n"
        f"AI回应：{ai_response}\n\n"
        f"请分析这次交互是否涉及以下状态变化：\n"
        f"1. 剧情关键点（如玩家是否发现了重要线索）\n"
        f"2. NPC状态变化（如是否与某个NPC见面）\n"
        f"3. 地点状态变化（如是否解锁了某个房间）\n"
        f"4. 玩家知识更新（如是否获得了新线索）\n\n"
        f"请以JSON格式返回需要更新的状态，格式如下：\n"
        f'{{"plot_flags.key": value, "npc_states.npc_name.key": value, "location_states.location.key": value, "player_knowledge.key": value}}\n'
        f"如果没有需要更新的状态，返回空对象 {{}}"
    )
    
    completion = client.chat.completions.create(
        model="kimi-k2-0711-preview",
        messages=[
            {
                "role": "system",
                "content": "你是长期记忆分析AI，负责分析游戏交互并提取状态更新信息。只返回JSON格式的结果。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1,
    )
    
    try:
        ai_reply = completion.choices[0].message.content.strip()
        # 尝试解析JSON
        import json
        return json.loads(ai_reply)
    except Exception as e:
        print(f"解析记忆分析结果失败: {e}")
        return {}

def get_current_game_context(complete_memory):
    """
    从完整记忆中提取当前游戏上下文信息
    新增接口：用于获取当前游戏状态摘要
    - complete_memory: 完整的记忆文本
    - 返回: 游戏上下文摘要
    """
    prompt = (
        f"基于以下游戏记忆，请提取当前游戏的关键上下文信息：\n\n"
        f"{complete_memory}\n\n"
        f"请总结：\n"
        f"1. 玩家当前的位置和状态\n"
        f"2. 已知的重要线索\n"
        f"3. 已接触的NPC\n"
        f"4. 当前的主要任务或目标\n"
        f"5. 需要注意的危险或限制\n\n"
        f"请用简洁的语言总结，不超过200字。"
    )
    
    completion = client.chat.completions.create(
        model="kimi-k2-0711-preview",
        messages=[
            {
                "role": "system",
                "content": "你是游戏上下文分析AI，负责提取当前游戏状态的关键信息。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
    )
    
    return completion.choices[0].message.content.strip()
