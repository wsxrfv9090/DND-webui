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
    if os.path.exists(QUEUE_MEMORY_PATH):
        os.remove(QUEUE_MEMORY_PATH)
        open(QUEUE_MEMORY_PATH, 'w').close()
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

def format_check_result_string(skill_name: str, difficulty: int, roll_result: int, success: bool) -> str:
    """
    生成格式化的检定结果描述文本
    """
    diff_map = {0: "普通", 1: "困难", 2: "极难"}
    outcome = "成功" if success else "失败"
    return f"你进行了一次[{skill_name}]({diff_map.get(difficulty, '普通')})检定，骰点结果为 {roll_result}，判定 {outcome}。"

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