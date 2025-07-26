import bin.utility as util
import bin.concurrent_1 as cur_1

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openai import AsyncOpenAI
import json


print("FastAPI 应用启动中，正在初始化 AI 服务...")
try:
    # 创建异步AI客户端实例
    ai_client = AsyncOpenAI(api_key = util.API_KEY, base_url = util.BASE_URL)
    
    # 加载世界观和技能列表
    world_view = util.load_world_view()
    all_skills_list = util.load_skills_list()
    
    # 将技能列表转换为字符串，用于传递给AI prompt
    skills_str = "、".join([skill.get('技能名称', '') for skill in all_skills_list])
    print("AI 服务初始化成功！")
except Exception as e:
    print(f"错误：AI 服务初始化失败 - {e}")
    # 在实际应用中，你可能希望在这里让应用启动失败
    ai_client = None
    world_view = ""
    skills_str = ""
    
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
    processed_result = await cur_1.concurrent_1(input_text, skills_list, world_view, skills_str ,ai_client)

    return {"output": processed_result}

@app.get("/")
async def root_endpoint():
    message = "你好！Python API正在运行中。"
    if not ai_client:
        message += " (警告: AI服务未成功初始化)"
    return {"message": message}
