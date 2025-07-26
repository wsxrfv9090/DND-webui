# -*- coding: utf-8 -*-
import asyncio
import json
import math
import os
import random
from openai import AsyncOpenAI
from typing import Tuple, Optional, Dict, List, Any

# ==============================================================================
# 1. 统一配置常量 (Global Configuration Constants)
# ==============================================================================
# 请将这里的 API Key 替换为您自己的 Moonshot AI Key
API_KEY: str = "sk-1fPmr7wLVZy1QlPBPfBXB3bSO5Wc3UPBvTi8tSGfL7FYwyMe"
BASE_URL: str = "https://api.moonshot.cn/v1"
MODEL_NAME: str = "moonshot-v1-8k"

# 数据文件路径
CACHE_DIR: str = 'cache'
WORLD_VIEW_PATH: str = os.path.join(CACHE_DIR, 'world_view.txt')
SKILLS_PATH: str = os.path.join(CACHE_DIR, 'skills.json')


# ==============================================================================
# 2. 数据加载与工具函数 (Data Loading & Utility Functions)
# ==============================================================================

def ensure_cache_dir_exists():
    """确保缓存目录存在"""
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

def load_text_file(path: str, default_content: str) -> str:
    """加载文本文件，若不存在则创建并写入默认内容"""
    ensure_cache_dir_exists()
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(default_content)
        return default_content

def load_json_file(path: str, default_content: List[Dict]) -> List[Dict]:
    """加载JSON文件，若不存在或无效则创建并写入默认内容"""
    ensure_cache_dir_exists()
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(default_content, f, ensure_ascii=False, indent=4)
        return default_content

def get_skill_success_rate(skill_name: Optional[str], skills_list: List[Dict[str, Any]]) -> int:
    """从角色技能列表中查找技能的成功率"""
    if not skill_name:
        return 0
    for skill in skills_list:
        if skill["技能名称"] == skill_name:
            return skill["成功率"]
    return 0

def perform_check(roll_result: int, success_rate: int, difficulty: int) -> bool:
    """根据CoC规则进行技能检定判定"""
    modifiers = {0: 1, 1: 0.5, 2: 0.2}
    modifier = modifiers.get(difficulty, 1)
    threshold = math.floor(success_rate * modifier)
    return roll_result <= threshold

def format_check_result_string(skill_name: str, difficulty: int, roll_result: int, success: bool) -> str:
    """生成格式化的检定结果描述文本"""
    diff_map = {0: "普通", 1: "困难", 2: "极难"}
    outcome = "成功" if success else "失败"
    return f"你进行了一次[{skill_name}]({diff_map.get(difficulty, '普通')})检定，骰点结果为 {roll_result}，判定 {outcome}。"

# --- 从原Class中拆分出的数据加载函数 ---
def load_world_view() -> str:
    """加载世界观设定"""
    default_world_view = (
        "【世界观设定：1920年代的阿卡姆】\n\n"
        "时代背景：1920年代的美国，禁酒令时期，社会变革与神秘主义并存。"
        "阿卡姆是一座虚构的新英格兰小镇，位于马萨诸塞州，以其古老的建筑、"
        "神秘的传说和密斯卡托尼克大学而闻名。"
    )
    return load_text_file(WORLD_VIEW_PATH, default_world_view)

def load_skills_list() -> List[Dict[str, Any]]:
    """加载技能列表"""
    default_skills = [
        {"name": skill} for skill in [
            "信用评级", "说服", "侦查", "心理学", "闪避", "格斗", "射击", "驾驶",
            "图书馆使用", "聆听", "潜行", "妙手", "恐吓", "法律", "医学", "急救",
            "攀爬", "跳跃", "游泳", "投掷", "取悦", "乔装", "锁匠", "机械维修",
            "计算机使用 Ω", "电子学 Ω", "科学", "外语", "母语", "历史", "考古学",
            "人类学", "博物学", "导航", "神秘学", "操作重型机械", "爆破",
            "炮术", "催眠", "读唇", "动物驯养", "学识", "技艺"
        ]
    ]
    return load_json_file(SKILLS_PATH, default_skills)


# ==============================================================================
# 3. 核心AI函数 (Core AI Functions)
# ==============================================================================

async def analyze_action(
    client: AsyncOpenAI, 
    world_view: str, 
    skills_str: str, 
    user_input: str
) -> Tuple[bool, Optional[str], int]:
    """异步分析用户输入，判断是否需要技能检定、使用哪个技能以及难度。"""
    prompt = (
        f"{world_view}\n\n"
        f"你是一个TRPG:Call of Cthulhu的规则裁判AI。请基于上述世界观判定用户行为。\n"
        f"1. 该行为是否需要技能检定？\n"
        f"2. 若需要，应使用哪个技能？（技能名必须严格来自技能列表）\n"
        f"3. 难度是普通(0)、困难(1)还是极难(2)？\n"
        f"严格按以下格式之一输出：\n- `True-技能名称-难度`\n- `False--`\n\n"
        f"技能列表: {skills_str}\n"
        f"用户输入: '{user_input}'"
    )
    
    completion = await client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "你是一个严格的TRPG规则裁判AI，只输出结构化判定结果。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
    )
    ai_reply = completion.choices[0].message.content.strip()

    if ai_reply.startswith("True-"):
        parts = ai_reply.split("-")
        skill = parts[1] if len(parts) > 1 and parts[1] else None
        try:
            difficulty = int(parts[2]) if len(parts) > 2 and parts[2] else 0
        except (ValueError, IndexError):
            difficulty = 0
        return True, skill, difficulty
    else:
        return False, None, 0

async def generate_description(
    client: AsyncOpenAI, 
    world_view: str, 
    user_input: str, 
    judge_result: Optional[str] = None
) -> str:
    """异步生成场景描述，营造克苏鲁氛围"""
    system_prompt = (
        "你是TRPG:Call of Cthulhu世界观的叙述AI（守秘人/KP）。你的任务是基于1920年代阿卡姆世界观，"
        "用生动、悬疑且带有时代感的语言进行描述，营造出神秘而压抑的氛围。"
    )
    
    user_prompt = (
        f"{world_view}\n\n"
        f"情景：用户的行动是“{user_input}”，此行动的检定结果为“{judge_result}”。\n"
        f"任务：请基于此结果，生动地描述接下来发生了什么。"
    ) if judge_result else (
        f"{world_view}\n\n"
        f"情景：用户刚刚宣布行动“{user_input}”，此行动无需检定。\n"
        f"任务：请直接描述这个行动在阿卡姆这个地方发生时的情景和氛围。"
    )
        
    completion = await client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
    )
    return completion.choices[0].message.content.strip()


# ==============================================================================
# 4. 主程序入口 (Main Execution Block)
# ==============================================================================

async def main():
    """主函数，运行一个完整的游戏回合"""
    print("\n--- 欢迎来到克苏鲁的呼唤 AI 守秘人 ---")
    
    # --- 游戏设置与初始化 ---
    player_character_skills = [
        {"name": "侦查", "rate": 75}, {"name": "图书馆使用", "rate": 60},
        {"name": "说服", "rate": 50}, {"name": "闪避", "rate": 40},
        {"name": "神秘学", "rate": 5},
    ]

    # 初始化AI客户端和游戏数据
    client = AsyncOpenAI(api_key=API_KEY, base_url=BASE_URL)
    world_view = load_world_view()
    all_skills_list = load_skills_list()
    skills_str = "、".join([skill['name'] for skill in all_skills_list])
    print("AI服务及游戏数据已加载。")

    # --- 游戏循环 (简化为单回合) ---
    user_input = input("\n你的角色想要做什么？> ")

    # 1. AI 分析行动 (传入 client, world_view, skills_str)
    print("\n[AI裁判正在分析你的行动...]")
    need_check, skill, difficulty = await analyze_action(client, world_view, skills_str, user_input)
    judge_result_str = None

    # 2. 如果需要，执行技能检定
    if need_check and skill:
        player_skill_rate = get_skill_success_rate(skill, player_character_skills)
        print(f"[判定需求：技能={skill}, 难度={['普通', '困难', '极难'][difficulty]}, 你的成功率={player_skill_rate}%]")
        
        roll = random.randint(1, 100)
        print(f"[你掷出了 D100 = {roll}]")

        is_success = perform_check(roll, player_skill_rate, difficulty)
        judge_result_str = format_check_result_string(skill, difficulty, roll, is_success)
        print(f"[{judge_result_str}]")
    else:
        print("[AI裁判认为这只是普通行动，无需检定]")

    # 3. AI 生成叙述 (传入 client, world_view)
    print("\n[AI守秘人正在生成场景描述...]")
    narrative = await generate_description(client, world_view, user_input, judge_result_str)

    print("\n" + "="*20 + " 场景描述 " + "="*20)
    print(narrative)
    print("="*52 + "\n")

if __name__ == "__main__":
    if not API_KEY or "sk-..." in API_KEY:
        print("错误：请在脚本顶部的全局常量中设置您的有效 Moonshot API_KEY。")
    else:
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            print("\n游戏已退出。")
        except Exception as e:
            print(f"\n[严重错误] 程序运行失败: {e}")

