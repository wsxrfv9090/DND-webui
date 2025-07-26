from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
USER_INPUT = 'HI'
import ai.test_ai as ai_process
import json
import math
import random
import os


def core_python_processing(user_text: str) -> str:
    """
    这里面放你所有的复杂Python代码。
    它可以是数据分析、机器学习模型调用、复杂的计算等等。
    为了演示，我们只做一个简单的文本反转。
    """
    # 读取技能数据
    json_filename = 'skills.json'
    with open(json_filename, 'r', encoding='utf-8') as f:
        skills_list = json.load(f)

    # 获取用户输入
    user_input =user_text

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
    else:
        print("无需判定。")
        # 直接生成世界观下的AI描述
        world_desc = ai_process.generate_description(user_input)
    # 实现长期记忆 function(txt位置， 上次的输出)

    result = world_desc
    print(f"后端收到了文本: '{user_input}'")
    print(f"后端即将返回result'")
    print(result)
    return result


app = FastAPI()

# 3. 【至关重要】配置“跨域许可” (CORS)
# 解释：默认情况下，出于安全考虑，浏览器不允许一个域名（比如 a.com）的网页
# 去请求另一个域名（比如 b.com）的API。我们的Next.js开发服务器在3000端口，
# Python服务器在8000端口，浏览器会认为它们是不同的“域”，所以会阻止请求。
# 这段代码就是告诉浏览器：“别担心，我允许来自3000端口的请求，放行吧！”
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 只允许这个来源的请求
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有请求方法 (GET, POST等)
    allow_headers=["*"],  # 允许所有请求头
)


# 4. 创建一个“API端点”(Endpoint)，也就是一个具体的“客服分机”
# @app.post("/process-text") 这句话的意思是：
#   - @app：嘿，FastAPI应用！
#   - .post：我要创建一个只接受 POST 类型请求的分机。（POST通常用于发送数据给服务器）
#   - ("/process-text")：这个分机的“号码”是 /process-text
#
# 这个函数 `process_text_endpoint` 会在有人“拨打”这个分机时自动运行
@app.post("/process-text")
def process_text_endpoint(request_data: dict):
    # FastAPI会自动把前端发来的JSON数据转成一个Python字典 `request_data`
    # 我们期望前端发送的数据格式是 {"user_input": "一些文本"}
    input_text = request_data.get("user_input")

    if input_text is None:
        return {"error": "没有收到名为 user_input 的数据"}

    # 调用你真正的核心逻辑函数
    processed_result = core_python_processing(input_text)

    # 以JSON格式返回结果。FastAPI会自动转换。
    # 前端将会收到一个格式为 {"output": "处理后的结果"} 的数据
    return {"output": processed_result}


# 5. 我们再创建一个“总机”，用来测试服务器是否正常运行
@app.get("/")
def root_endpoint():
    return {"message": "你好！Python API正在运行中。"}