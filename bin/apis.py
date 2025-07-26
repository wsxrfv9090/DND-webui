from bin import utility as util
from openai import AsyncOpenAI
from typing import Tuple, Optional

async def api_1_analyze_action(
    client: AsyncOpenAI, 
    world_view: str, 
    skills_str: str, 
    user_input: str
) -> Tuple[bool, Optional[str], int]:
    """
    异步分析用户输入，判断是否需要技能检定、使用哪个技能以及难度。
    """
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
        model = util.MODEL_NAME,
        messages=[
            {"role": "system", "content": "你是一个严格的TRPG规则裁判AI，只输出结构化判定结果。技能名称必须完全匹配技能列表中的名称。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
    )
    ai_reply = completion.choices[0].message.content.strip()
    print(f"AI分析结果: {ai_reply}")  # 添加调试输出

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

async def api_2_generate_description(
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
        model = util.MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
    )
    return completion.choices[0].message.content.strip()