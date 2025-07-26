from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
USER_INPUT = 'HI'
import ai.test_ai as ai_process
import json
import math
import random
import os


def core_python_processing(user_text: str) -> str:
   
    # 读取技能数据
    json_filename = 'skills.json'
    with open(json_filename, 'r', encoding='utf-8') as f:
        skills_list = json.load(f)

    # 获取用户输入
    user_input = user_text

    # 用AI分析用户输入，获得判定需求、技能、难度
    need_judge, skill_name, difficulty = ai_process.analyze_action(user_input)

    if need_judge:
        # 获取技能成功率
        success_rate = ai_process.get_skill_success_rate(skill_name, skills_list)
        # 投骰
        roll_result = random.randint(1, 100)
        print(f"你投出了：{roll_result}")
        # 判定
        success = ai_process.judge(roll_result, success_rate, difficulty)
        # 生成判定描述
        judge_desc = ai_process.describe_action(user_input, skill_name, difficulty, roll_result, success)
        print(judge_desc)
        # 生成世界观下的AI描述
        world_desc = ai_process.generate_description(user_input, judge_desc)
        # 组合结果：判定结果 + 世界观描述
        result = f"{judge_desc}\n\n{world_desc}"
    else:
        print("无需判定。")
        # 直接生成世界观下的AI描述
        world_desc = ai_process.generate_description(user_input)
        result = world_desc

    print(f"后端收到了文本: '{user_input}'")
    print(f"后端即将返回: {result}")
    return result


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 只允许这个来源的请求
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有请求方法 (GET, POST等)
    allow_headers=["*"],  # 允许所有请求头
)


@app.post("/process-text")
def process_text_endpoint(request_data: dict):
    # FastAPI会自动把前端发来的JSON数据转成一个Python字典 `request_data`
    # 我们前端发送的数据格式是 {"user_input": "一些文本"}
    input_text = request_data.get("user_input")

    if input_text is None:
        return {"error": "没有收到名为 user_input 的数据"}

    # 调用核心逻辑函数
    processed_result = core_python_processing(input_text)

    # 以JSON格式返回结果。FastAPI会自动转换。
    # 前端将会收到一个格式为 {"output": "处理后的结果"} 的数据
    return {"output": processed_result}


#测试服务器是否正常运行
@app.get("/")
def root_endpoint():
    return {"message": "你好！Python API正在运行中。"}