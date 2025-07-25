#main，py 先识别用户输入是不是不确定，需不需要判定
USER_INPUT = 'HI'
import ai.test_ai as ai_process
import json
import math
import random
def main():
    # 读取技能数据
    json_filename = 'skills.json'
    with open(json_filename, 'r', encoding='utf-8') as f:
        skills_list = json.load(f)

    # 获取用户输入
    user_input = input("请输入你的行动：")

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
        print(world_desc)
    else:
        print("无需判定。")
        # 直接生成世界观下的AI描述
        world_desc = ai_process.generate_description(user_input)
        print(world_desc)

if __name__ == "__main__":
    main()