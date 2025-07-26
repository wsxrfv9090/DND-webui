from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openai import AsyncOpenAI
from typing import Dict, List, Any
import json

# 假设你的 AIServices01.py 文件包含了之前重构的所有无类函数
# (API_KEY, MODEL_NAME, load_world_view, load_skills_list, analyze_action, etc.)
import ai.AIServices as ai_process 
import random

# ==============================================================================
# 1. 应用启动时的一次性初始化
# ==============================================================================
# 将 AI 客户端、世界观和技能列表等作为全局变量加载，避免每次请求都重复创建/读取。
# 这极大地提高了性能。
print("FastAPI 应用启动中，正在初始化 AI 服务...")
try:
    # 创建异步AI客户端实例
    ai_client = AsyncOpenAI(api_key=ai_process.API_KEY, base_url=ai_process.BASE_URL)
    
    # 加载世界观和技能列表
    world_view = ai_process.load_world_view()
    all_skills_list = ai_process.load_skills_list()
    
    # 将技能列表转换为字符串，用于传递给AI prompt
    skills_str = "、".join([skill.get('name', '') for skill in all_skills_list])
    
    print("AI 服务初始化成功！")
except Exception as e:
    print(f"错误：AI 服务初始化失败 - {e}")
    # 在实际应用中，你可能希望在这里让应用启动失败
    ai_client = None
    world_view = ""
    skills_str = ""


# ==============================================================================
# 2. 核心处理逻辑
# ==============================================================================
# [改动 1]: 核心函数现在接收“玩家技能表”作为参数
async def core_python_processing(user_input: str, player_skills: List[Dict[str, Any]]) -> str:
    """
    处理用户输入的完整异步流程。
    """
    # [改动 2]: 直接调用异步 AI 分析函数，并传入所需的全局变量
    need_judge, skill_name, difficulty = await ai_process.analyze_action(
        client=ai_client,
        world_view=world_view,
        skills_str=skills_str,
        user_input=user_input
    )

    result_desc = ""

    if need_judge and skill_name:
        # 从传入的 player_skills 中获取角色在该技能上的成功率
        success_rate = ai_process.get_skill_success_rate(skill_name, player_skills)
        
        # 纯计算和随机操作，无需异步
        roll_result = random.randint(1, 100)
        is_success = ai_process.perform_check(roll_result, success_rate, difficulty)
        
        # 生成格式化的检定结果描述
        judge_desc = ai_process.format_check_result_string(skill_name, difficulty, roll_result, is_success)
        result_desc = judge_desc # 将检定结果作为叙述的一部分
        print(judge_desc)
    else:
        print("无需判定。")

    # [改动 3]: 调用异步 AI 描述生成函数，并传入所需参数
    world_desc = await ai_process.generate_description(
        client=ai_client,
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


# ==============================================================================
# 3. FastAPI 应用实例与端点
# ==============================================================================
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/process-text")
async def process_text_endpoint(request_data: dict):
    # 检查AI客户端是否成功初始化
    if not ai_client:
        return {"error": "服务器AI服务未就绪，请检查服务器日志。"}

    input_text = request_data.get("user_input")
    if not input_text:
        return {"error": "没有收到名为 user_input 的数据"}


    json_filename = 'cache/skills.json'
    with open(json_filename, 'r', encoding='utf-8') as f:
        skills_list = json.load(f)
    # 调用核心逻辑，并传入玩家技能表
    processed_result = await core_python_processing(input_text, skills_list)

    return {"output": processed_result}

@app.get("/")
async def root_endpoint():
    message = "你好！Python API正在运行中。"
    if not ai_client:
        message += " (警告: AI服务未成功初始化)"
    return {"message": message}
