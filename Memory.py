import os
import json

# --- 1. 初始化设置 ---
CWD = os.getcwd()
MEMORY_PATH = os.path.join(CWD, 'Cache')
SESSION_PATH = os.path.join(MEMORY_PATH, 'session_memory')

# 定义文件路径
WORLDVIEW_BASE_PATH = os.path.join(MEMORY_PATH, 'worldview_base.txt')
DYNAMIC_STATE_PATH = os.path.join(MEMORY_PATH, 'dynamic_state.json')

def initialize_memory():
    """在游戏开始时调用，创建必要的目录和初始状态文件。"""
    print("Initializing memory directories and files...")
    os.makedirs(SESSION_PATH, exist_ok=True)

    # 如果世界观基底文件不存在，创建一个空的
    if not os.path.exists(WORLDVIEW_BASE_PATH):
        with open(WORLDVIEW_BASE_PATH, 'w', encoding='utf-8') as f:
            f.write("\n")
        print(f"Created empty worldview file at: {WORLDVIEW_BASE_PATH}")

    # 如果动态状态文件不存在，创建初始状态
    if not os.path.exists(DYNAMIC_STATE_PATH):
        initial_state = {
            "plot_flags": {
                "james_fate_known": False,
                "brophy_identity_suspected": False,
                "glaaki_avatar_discovered": False
            },
            "npc_states": {
                "emily_livingstone": {"status": "alive", "met_players": False},
                "travis_bryce": {"status": "alive", "met_players": False},
                "robert_brophy": {"status": "active_servant", "cover_blown": False}
            },
            "location_states": {
                "squatters_lake_motel": {"room_3_door": "locked"},
                "library_miskatonic": {"squatter_lake_history_researched": False}
            },
            "player_knowledge": {
                "known_clues": [],
                "known_facts_atomic": []
            }
        }
        with open(DYNAMIC_STATE_PATH, 'w', encoding='utf-8') as f:
            json.dump(initial_state, f, indent=4, ensure_ascii=False)
        print(f"Created initial dynamic state file at: {DYNAMIC_STATE_PATH}")

# --- 2. 核心记忆处理函数 ---

def prepare_kp_memory() -> str:
    """
    【关键函数】在每一轮交互前，编织最终的记忆文本给KP Agent。
    它整合了静态世界观和最新的动态状态。
    """
    # 读取静态世界观
    with open(WORLDVIEW_BASE_PATH, 'r', encoding='utf-8') as f:
        base_memory = f.read()

    # 读取动态状态
    with open(DYNAMIC_STATE_PATH, 'r', encoding='utf-8') as f:
        dynamic_state = json.load(f)

    # 将动态状态格式化为人类可读的文本，放在开头作为高优先级提醒
    # f-string的强大之处在于可以方便地嵌入变量
    state_summary = f"""
--- 最高优先级：当前游戏状态提醒 ---
剧情关键点:
- 玩家是否知道詹姆斯的命运: {dynamic_state['plot_flags']['james_fate_known']}
- 玩家是否怀疑布罗菲父子: {dynamic_state['plot_flags']['brophy_identity_suspected']}

NPC状态:
- 艾米丽是否已与玩家见面: {dynamic_state['npc_states']['emily_livingstone']['met_players']}
- 特拉维斯是否已与玩家见面: {dynamic_state['npc_states']['travis_bryce']['met_players']}

玩家已确认的线索和事实:
{chr(10).join('- ' + fact for fact in dynamic_state['player_knowledge']['known_facts_atomic']) if dynamic_state['player_knowledge']['known_facts_atomic'] else '- 暂无'}
------------------------------------
"""
    # 组合成最终的记忆文本
    # 最终发送给KP Agent的是这个组合后的字符串
    final_memory_prompt = state_summary + "\n" + base_memory
    
    # 可以在这里加入短期和长期记忆的文本
    # For example:
    # final_memory_prompt += get_short_term_memory()
    # final_memory_prompt += get_long_term_memory()

    return final_memory_prompt

def update_dynamic_state(updates: dict):
    """
    【关键函数】根据长期记忆Agent的分析结果，更新dynamic_state.json文件。
    updates: 一个包含要更新的键和值的字典。
    例如: {"plot_flags.james_fate_known": True, "player_knowledge.known_clues": "HANDOUT_1"}
    """
    try:
        # 读取当前状态
        with open(DYNAMIC_STATE_PATH, 'r', encoding='utf-8') as f:
            current_state = json.load(f)

        # 应用更新
        for key_path, value in updates.items():
            keys = key_path.split('.')
            element = current_state
            for key in keys[:-1]:
                element = element[key]
            
            # 处理简单值更新和列表追加
            final_key = keys[-1]
            if isinstance(element[final_key], list):
                if value not in element[final_key]:
                    element[final_key].append(value)
            else:
                element[final_key] = value

        # 写回更新后的状态
        with open(DYNAMIC_STATE_PATH, 'w', encoding='utf-8') as f:
            json.dump(current_state, f, indent=4, ensure_ascii=False)
        print(f"Dynamic state updated successfully: {updates}")

    except FileNotFoundError:
        print(f"Error: Dynamic state file not found at {DYNAMIC_STATE_PATH}. Please initialize first.")
    except Exception as e:
        print(f"An error occurred during state update: {e}")

# --- 3. 游戏主循环（示例） ---

def main_game_loop():
    # 游戏开始时初始化
    initialize_memory()

    # --- 模拟一轮游戏 ---
    # 1. 准备给KP的记忆
    kp_prompt = prepare_kp_memory()
    print("\n--- Preparing memory for KP Agent ---")
    # print(kp_prompt) # 你可以打印出来看看效果

    # 2. KP Agent处理输入，生成回应 (这里是伪代码)
    # kp_response = call_kp_agent(kp_prompt, player_input)
    # print(f"KP: {kp_response}")
    # interaction_log = f"Player: {player_input}\nKP: {kp_response}"

    # 3. 长期记忆Agent分析交互 (这里是伪代码)
    # summary = call_long_term_agent(interaction_log)
    # 假设分析结果是玩家成功在图书馆找到了线索
    print("\n--- Long-term memory agent analyzed the turn ---")
    analysis_result = {
        "location_states.library_miskatonic.squatter_lake_history_researched": True,
        "player_knowledge.known_clues": "HANDOUT_1",
        "player_knowledge.known_facts_atomic": "斯夸特湖区域有不祥的历史记录"
    }
    
    # 4. 更新动态状态
    update_dynamic_state(analysis_result)

    # 5. 再次准备记忆，可以看到状态已经更新
    print("\n--- Preparing memory for the NEXT turn ---")
    next_kp_prompt = prepare_kp_memory()
    print(next_kp_prompt.split('---')[1]) # 只打印状态部分看变化

if __name__ == '__main__':
    main_game_loop()

