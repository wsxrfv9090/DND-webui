from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def core_python_processing(user_text: str) -> str:
    """
    这里面放你所有的复杂Python代码。
    它可以是数据分析、机器学习模型调用、复杂的计算等等。
    为了演示，我们只做一个简单的文本反转。
    """
    print(f"后端收到了文本: '{user_text}'")
    result = f"Python后端处理完成！这是反转后的文本： {user_text[::-1]}"
    print(f"后端即将返回: '{result}'")
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
    input_text = request_data.get("user_input")

    if input_text is None:
        return {"error": "没有收到名为 user_input 的数据"}

    processed_result = core_python_processing(input_text)

    return {"output": processed_result}

@app.get("/")
def root_endpoint():
    return {"message": "你好！Python API正在运行中。"}

