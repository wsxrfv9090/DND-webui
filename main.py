from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import ai.test_ai as ai_process
import json
import math
import random
import os
import Memory
import uuid
from datetime import datetime



def core_python_processing(user_text: str) -> str:
    """
    核心处理函数：集成AI判定、记忆系统和状态管理
    """
   
        # 1. 初始化记忆系统
    Memory.initialize_memory()
        
        # 2. 获取完整记忆（世界观+动态状态）
    complete_memory = Memory.prepare_kp_memory()
        
        # 3. 读取技能数据
    json_filename = 'skills.json'
    with open(json_filename, 'r', encoding='utf-8') as f:
            skills_list = json.load(f)

        # 4. 分析用户输入（暂不传入记忆）
    need_judge, skill_name, difficulty = ai_process.analyze_action(user_text)  

        # 5. 处理判定逻辑
    if need_judge:
            # 获取技能成功率
            success_rate = ai_process.get_skill_success_rate(skill_name, skills_list)
            # 投骰
            roll_result = random.randint(1, 100)
            print(f"你投出了：{roll_result}")
            # 判定
            success = ai_process.judge(roll_result, success_rate, difficulty)
            # 生成判定描述
            judge_desc = ai_process.describe_action(user_text, skill_name, difficulty, roll_result, success)
            print(judge_desc)
            #生成世界描述（传入完整记忆）
            world_desc = ai_process.generate_description_with_memory(user_text, judge_desc, complete_memory)
            # 组合结果：判定结果 + 世界观描述
            result = f"{judge_desc}\n\n{world_desc}"
    else:
            print("无需判定。")
            # 直接生成世界描述（传入完整记忆）
            world_desc = ai_process.generate_description_with_memory(user_text, None, complete_memory)
            result = world_desc

    # 6. 生成记忆更新
    memory_updates = ai_process.analyze_interaction_for_memory(user_text, result)
    
    # 7. 如果有需要更新的状态，则更新记忆
    if memory_updates:
        Memory.update_dynamic_state(memory_updates)
        print(f"记忆状态已更新: {memory_updates}")
    else:
        print("无需更新记忆状态")
        
    print(f"后端收到了文本: '{user_text}'")
    print(f"后端即将返回: {result}")
    return result
        
   

# FastAPI应用设置
app = FastAPI(title="DND WebUI - 集成版", version="2.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 只允许这个来源的请求
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有请求方法 (GET, POST等)
    allow_headers=["*"],  # 允许所有请求头
)

# 原有接口：处理文本
@app.post("/process-text")
def process_text_endpoint(request_data: dict):
    input_text = request_data.get("user_input")
    if input_text is None:
        return {"error": "没有收到名为 user_input 的数据"}
    
    processed_result = core_python_processing(input_text)
    return {"output": processed_result}

# 新增接口：获取游戏状态
@app.get("/game-status")
def game_status_endpoint():
    return get_game_status()

# 新增接口：重置游戏
@app.post("/reset-game")
def reset_game_endpoint():
    return reset_game()

# 新增接口：获取游戏上下文
@app.get("/game-context")
def game_context_endpoint():
    return get_game_context()

# 新增接口：获取交互历史
@app.get("/interaction-history")
def interaction_history_endpoint():
    return {
        "session_id": session_id,
        "history": interaction_history,
        "count": len(interaction_history)
    }

# 测试服务器是否正常运行
@app.get("/")
def root_endpoint():
    return {
        "message": "你好！DND WebUI 集成版API正在运行中。",
        "version": "2.0.0",
        "session_id": session_id,
        "features": [
            "AI判定系统",
            "记忆管理系统", 
            "游戏状态跟踪",
            "会话历史记录"
        ]
    }

# 健康检查接口
@app.get("/health")
def health_check():
    try:
        Memory.initialize_memory()
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id,
            "memory_system": "initialized"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        } 