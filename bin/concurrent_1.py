from typing import Dict, List, Any
from bin import utility as util
import random
from bin import apis
from typing import Tuple


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
    # 使用新的技能字符串生成函数
    if not skills_str:
        skills_str = util.get_skills_string()
    
    print(f"技能字符串: {skills_str}")  # 添加调试输出
    
    # [改动 2]: 直接调用异步 AI 分析函数，并传入所需的全局变量
    need_judge, skill_name, difficulty = await apis.api_1_analyze_action(
        client = client,
        world_view = world_view,
        skills_str = skills_str,
        user_input = user_input
    )

    print(f"判定结果: need_judge={need_judge}, skill_name={skill_name}, difficulty={difficulty}")  # 添加调试输出

    result_desc = ""

    if need_judge and skill_name:
        # 从传入的 player_skills 中获取角色在该技能上的成功率
        success_rate = util.get_skill_success_rate(skill_name, player_skills)
        print(f"技能成功率: {success_rate}")  # 添加调试输出
        
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
        world_view = world_view,
        user_input = user_input,
        judge_result = result_desc if result_desc else None
    )
    
    # 组合最终结果
    final_result = world_desc
    
    print(f"后端收到了文本: '{user_input}'")
    print(f"后端即将返回: {final_result}")
    print(f"正在存储至{util.QUEUE_MEMORY_PATH}")
    poped = save_one_io_into_queue(user_input, final_result, util.QUEUE_MEMORY_PATH)
    print(poped)
    return final_result


def save_one_io_into_queue(input_text: str, output_text: str, filename: str, max_turns: int = 5) -> Tuple[str, ...]:
    """
    将一次用户输入和AI输出（可以是多行）保存到文本文件中，并维持一个固定大小的对话队列。
    
    使用一个明确的分隔符来界定每一轮对话，以支持多行输入和输出。
    当文件中的对话轮数超过max_turns时，会删除最旧的一轮对话。

    :param input_text: 用户的输入内容（可多行）。
    :param output_text: AI的输出内容（可多行）。
    :param filename: 用于存储对话的txt文件名。
    :param max_turns: 队列中要保留的最大对话轮数。
    """
    
    # 1. 定义角色前缀和轮次分隔符
    # 分隔符应足够独特，以避免与对话内容本身冲突
    player_prefix = "Player:"
    ai_prefix = "AI:"
    TURN_SEPARATOR = "\n<|END_OF_TURN|>\n" # 使用一个清晰且独特的分隔符

    all_turns = []
    
    # 2. 读取现有文件内容，并按分隔符切分成轮次
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            # 读取整个文件内容，然后用分隔符切分
            content = f.read()
            if content:
                # 切分后，过滤掉可能因文件末尾分隔符产生的空字符串
                all_turns = [turn for turn in content.split(TURN_SEPARATOR) if turn.strip()]
    except FileNotFoundError:
        # 文件不存在，all_turns 保持为空列表
        pass
        
    # 3. 格式化并加入最新的对话轮次
    # 移除了您之前代码中多余的冒号和换行符，让格式更标准
    # Player:
    # ...input...
    # AI:
    # ...output...
    new_turn_string = f"{player_prefix}\n{input_text}\n{ai_prefix}\n{output_text}"
    all_turns.append(new_turn_string)
    
    
    # 4. 检查对话轮数，如果超过限制，则删除最老的记录
    if len(all_turns) > max_turns: 
        # 列表切片依然是实现此功能的最佳方式
        all_turns = all_turns[-max_turns:]
        
    # 5. 将更新后的对话队列（用分隔符连接）一次性写回文件
    with open(filename, 'w', encoding='utf-8') as f:
        # 使用分隔符将所有轮次连接成一个字符串
        output_content = TURN_SEPARATOR.join(all_turns)
        f.write(output_content)
        
    return tuple(all_turns)
