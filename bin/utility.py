import os
import json
from typing import Optional, Dict, List, Any
import math



def main_init() -> tuple[str, str, str, str, str]:
    """
    Initialize configuration constants for Moonshot API and ensure cache directory exists.

    Returns:
        tuple: A tuple containing API_KEY, BASE_URL, MODEL_NAME,
               WORLD_VIEW_PATH, and SKILLS_PATH.
    """
    # API configuration
    CWD = os.getcwd()

    API_KEY: str = "sk-1fPmr7wLVZy1QlPBPfBXB3bSO5Wc3UPBvTi8tSGfL7FYwyMe"
    BASE_URL: str = "https://api.moonshot.cn/v1"
    MODEL_NAME: str = "moonshot-v1-8k"

    # Data file paths
    CACHE_DIR: str = os.path.join(CWD, 'cache')
    os.makedirs(CACHE_DIR, exist_ok = True)
    WORLD_VIEW_PATH: str = os.path.join(CACHE_DIR, 'world_view.txt')
    SKILLS_PATH: str = os.path.join(CACHE_DIR, 'skills.json')
    
    MEMORY_SESSION_PATH = os.path.join(CACHE_DIR, 'session_memory')
    os.makedirs(MEMORY_SESSION_PATH, exist_ok = True)
    
    QUEUE_MEMORY_PATH = os.path.join(MEMORY_SESSION_PATH, 'queue_memory.txt')
    initial_story_text = """1924年，马萨诸塞州，阿卡姆市。

窗外，连绵的秋雨不知疲倦地敲打着玻璃，将街道的煤气灯光晕染成一片模糊的昏黄。你正身处自己位于“德尔伍德古物研究会”三楼的办公室里。空气中弥漫着旧书、皮革与淡淡烟草混合的熟悉气味，唯一的声响来自角落里那座老式落地钟沉稳而规律的滴答声。

你的桌上摊着几份关于新英格兰地区乡野传说的手稿，其中一篇关于“蹲占者之湖”（Squatter Lake）的记述尤其让你在意——文中提到了怪异的乌鸦群和某些无法被点燃的木材。你正沉浸在这些尘封的记述中，试图将零散的线索拼凑成一个完整的图案。

就在这时——

笃，笃，笃。

三声清晰而有力的敲门声，穿透了雨声和钟摆声，打破了书房的宁静。这声音听起来既不匆忙，也不犹豫，带着一种不容拒绝的决断。

你的思绪被打断了。你会怎么做？"""
    with open(QUEUE_MEMORY_PATH, 'w', encoding='utf-8') as f:
        f.write(initial_story_text)
    PROLONGED_MEMORY_PATH = os.path.join(MEMORY_SESSION_PATH, 'prolonged_memory.json')

    return API_KEY, BASE_URL, MODEL_NAME, CACHE_DIR, WORLD_VIEW_PATH, SKILLS_PATH, MEMORY_SESSION_PATH, QUEUE_MEMORY_PATH, PROLONGED_MEMORY_PATH

API_KEY, BASE_URL, MODEL_NAME, CACHE_DIR, WORLD_VIEW_PATH, SKILLS_PATH, MEMORY_SESSION_PATH, QUEUE_MEMORY_PATH, PROLONGED_MEMORY_PATH = main_init()

def ensure_cache_dir_exists():
    """确保缓存目录存在"""
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
        
def load_text_file(path: str, default_content: str) -> str:
    """加载文本文件，若不存在则创建文件并写入默认内容参数中的内容"""
    ensure_cache_dir_exists()
    try:
        with open(path, 'r', encoding = 'utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        with open(path, 'w', encoding = 'utf-8') as f:
            f.write(default_content)
        return default_content
    
def load_json_file(path: str, default_content: List[Dict]) -> List[Dict]:
    """加载JSON文件(cache/skills.json)，若不存在或无效则创建并写入默认内容"""
    ensure_cache_dir_exists()
    try:
        with open(path, 'r', encoding = 'utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        with open(path, 'w', encoding = 'utf-8') as f:
            json.dump(default_content, f, ensure_ascii = False, indent = 4)
        return default_content
    
def get_skill_success_rate(skill_name: Optional[str], skills_list: List[Dict[str, Any]]) -> int:
    """
    从角色技能列表中查找技能的成功率
    """
    if not skill_name:
        print(f"未找到技能: {skill_name}, 默认成功率为0")
        return 0
    for skill in skills_list:
        if skill["技能名称"] == skill_name:
            return skill["成功率"]
    return 0

def perform_check_coc(roll_result: int, success_rate: int, difficulty: int) -> bool:
    """
    根据CoC规则进行技能检定判定
    骰子
    成功率 * 100
    难度评级：0,1,2
    """
    modifiers = {0: 1, 1: 0.5, 2: 0.2}
    modifier = modifiers.get(difficulty, 1)
    threshold = math.floor(success_rate * modifier)
    return roll_result <= threshold

def format_check_result_string(skill_name: str, difficulty: int, roll_result: int, success: bool, success_rate: int) -> str:
    """
    生成格式化的检定结果描述文本
    """
    diff_map = {0: "普通", 1: "困难", 2: "极难"}
    outcome = "成功" if success else "失败"
    
    # 计算判定成功需要的点数
    modifiers = {0: 1, 1: 0.5, 2: 0.2}
    modifier = modifiers.get(difficulty, 1)
    threshold = math.floor(success_rate * modifier)
    
    return f"您的判定技能是{skill_name}（难度：{diff_map.get(difficulty, '普通')}），骰子点数是{roll_result}，判定成功需要{threshold}点数，所以您{outcome}了。"

def load_world_view() -> str:
    """加载世界观设定"""
    default_world_view = (
        
        "在克苏鲁神话背景下，本剧本的世界观是一个20世纪20年代的美国，表面上宁静却潜藏着不可名状的恐怖。\n"
        "旧日支配者的影响悄然渗透进人类世界，通过梦境与异教信徒操控现实。神秘、疯狂与未知的力量潜藏在被遗忘的角落，常人难以察觉。\n"
        "玩家扮演的调查员将在超自然与理性之间挣扎.在斯夸特湖汽车旅店，面对在隐藏于日常之下的诡秘真相，逐步揭开一场围绕神祇信仰与人类堕落的恐怖阴谋。\n"
        "理智有限，危险常在，结局往往令人绝望。"
    )
    return load_text_file(WORLD_VIEW_PATH, default_world_view)

def load_skills_list() -> List[Dict[str, Any]]:
    """加载技能列表"""
    default_skills = [
        {"技能名称": skill} for skill in [
            "信用评级", "说服", "侦查", "心理学", "闪避", "格斗", "射击", "驾驶",
            "图书馆使用", "聆听", "潜行", "妙手", "恐吓", "法律", "医学", "急救",
            "攀爬", "跳跃", "游泳", "投掷", "取悦", "乔装", "锁匠", "机械维修",
            "计算机使用 Ω", "电子学 Ω", "科学", "外语", "母语", "历史", "考古学",
            "人类学", "博物学", "导航", "神秘学", "操作重型机械", "爆破",
            "炮术", "催眠", "读唇", "动物驯养", "学识", "技艺"
        ]
    ]
    return load_json_file(SKILLS_PATH, default_skills)

def get_skills_string() -> str:
    """获取格式化的技能字符串，用于AI prompt"""
    skills_list = load_skills_list()
    # 清理技能名称，移除冒号等特殊字符
    cleaned_skills = []
    for skill in skills_list:
        skill_name = skill.get("技能名称", "")
        # 移除冒号等特殊字符
        cleaned_name = skill_name.replace("：", "").replace(":", "").strip()
        if cleaned_name:
            cleaned_skills.append(cleaned_name)
    
    return "、".join(cleaned_skills)