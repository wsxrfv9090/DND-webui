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
    queue_memory: str,
    judge_result: Optional[str] = None
) -> str:

    AI_KP_DUTY=" 你是跑团游戏的守密人（KP）。你的职责是基于以下记忆，管理游戏进程，扮演非玩家角色（NPC），并向玩家描述世界。"
    "你的核心职责是守护秘密，只在玩家通过调查和行动发现线索时，才揭示【玩家可探知信息】中的内容。【守密人专属记忆】绝对不能直接告诉玩家。"
    "【最高优先级记忆：核心秘密与结局】（置于记忆开头）"
    "最终真相： 斯夸特湖汽车旅店是一个陷阱。旅店老板布罗菲父子（罗伯特和威廉）是来自英国的不死仆从。他们的主人是一个名为“格拉基”的旧日支配者。"

    "当前阴谋： 布罗菲父子正在旅店的某个地方，利用格拉基的体液和尖刺，培育一个“格拉基的化身”。他们同时也在将旅客转化为新的仆从或无脑僵尸。"

    "玩家任务的真相： 玩家要寻找的目标——詹姆斯·弗雷泽——已经遇害。他已被转化为格拉基的不死仆从，无法被拯救。这是本故事的悲剧核心，你的描述和引导需要暗示危险，但绝不能提前揭示此结局。"

    "核心威胁："

    "格拉基（Gla'aki）： 本体在英国的湖中。它通过“梦牵”法术远程影响他人。"

    "格拉基的化身（Avatar）： 在斯夸特湖汽车旅店里被培育的子体，是本地的主要威胁。"

    "不死仆从（Servants）： 布罗菲父子、詹姆斯·弗雷泽，以及另外三名旅客。他们保	留智力，但绝对效忠格拉基。特征是动作僵硬，行为怪异。"

    "僵尸（Zombies）： 创造失败的产物，无脑，具有攻击性。是布罗菲父子创造的炮灰。"

    "弱点： 年老的不死仆从（如布罗菲父子）惧怕阳光，长期暴露会导致“绿色枯萎”并死亡。"

    "以上内容都是【守密人专属记忆 (KP-ONLY MEMORY)】"
    "此部分内容严禁以任何形式直接告知玩家。"

   
    system_prompt = (
        "你是TRPG:Call of Cthulhu世界观的叙述AI（守秘人/KP）。再次重复一遍一些你的注意事项：{AI_KP_DUTY}。你的任务是基于我们提供的世界观，和我们下面即将提供给你的记忆"
        "用生动、悬疑且带有时代感的语言进行描述，营造出神秘而压抑的氛围。"
    )
    
    user_prompt = (
        f"这是我们的世界观：{world_view}\n\n"
        f"这是我们提供给你的记忆：{queue_memory}\n\n"
        f"情景：用户的行动是“{user_input}”，此行动的检定结果为“{judge_result}”。\n"
        f"任务：请基于以上的世界观、记忆和检定结果，生动地描述接下来发生了什么。"
    ) if judge_result else (
        f"这是我们的世界观：{world_view}\n\n"
        f"这是我们提供给你的记忆：{queue_memory}\n\n"
        f"情景：用户刚刚宣布行动“{user_input}”，此行动无需检定。\n"
        f"任务：请基于以上的世界观、记忆和用户行动，生动地描述接下来发生了什么。"
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