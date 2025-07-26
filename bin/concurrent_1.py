from typing import Dict, List, Any
from bin import utility as util
import random
from bin import apis


async def concurrent_1(
    user_input: str, 
    player_skills: List[Dict[str, Any]],
    world_view: str,
    skills_str: str,
    client,
    ) -> str:
    """
    第一并发过程
    """
    # [改动 2]: 直接调用异步 AI 分析函数，并传入所需的全局变量
    need_judge, skill_name, difficulty = await apis.api_1_analyze_action(
        client = client,
        world_view = world_view,
        skills_str = skills_str,
        user_input = user_input
    )

    result_desc = ""

    if need_judge and skill_name:
        # 从传入的 player_skills 中获取角色在该技能上的成功率
        success_rate = util.get_skill_success_rate(skill_name, player_skills)
        
        # 纯计算和随机操作，无需异步
        roll_result = random.randint(1, 100)
        is_success = util.perform_check_coc(roll_result, success_rate, difficulty)
        
        # 生成格式化的检定结果描述
        judge_desc = util.format_check_result_string(skill_name, difficulty, roll_result, is_success)
        result_desc = judge_desc # 将检定结果作为叙述的一部分
        print(judge_desc)
    else:
        print("无需判定。")

    # [改动 3]: 调用异步 AI 描述生成函数，并传入所需参数
    world_desc = await apis.api_2_generate_description(
        client = client,
        world_view=world_view,
        user_input=user_input,
        judge_result=result_desc if result_desc else None
    )
    
    # 组合最终结果
    final_result = f"{result_desc}\n\n{world_desc}".strip()
    final_result = world_desc

    print(f"后端收到了文本: '{user_input}'")
    print(f"后端即将返回: {final_result}")
    return final_result