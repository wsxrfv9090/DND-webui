USER_INPUT = 'HI'
import ai.test_ai as ai_process
import json
import math
import random

user_input = USER_INPUT

def roll() -> int:
    result = random.randint(1, 100)
    print(f"1d100: 您摇到的结果是：{result}\n")
    return result

# 返回布尔值，是否需要判定
# need_determination = ai_process.determine(user_input)

# 如果需要判定，即need_determination为真
# 则判断需要过哪一个判定，返回一个对应skills.json里面技能名字的字符串
# 如果返回值不是skills.json里面的字符串，就循环再来，直到返回值match skills.json其中的一个名字



# if need_determination:
#     skill = ai_process.choose_skill(user_input)
    
    # 当返回值对应的成功率小于10时，print("")

# ------------------------------------------------------------
# 上述逻辑返回的值，供下面test临时使用
# 第一返回值：是否需要判定，需要为真，不需要为否
return_value_1 = True
# 第二返回值：需要判定的技能名字，为字符串，不需要判定为None
return_value_2 = '会计'
# 第三返回值：判定的难度，分为0，1，2(int)，分别代表普通，困难，极难，不需要判定为None
return_value_3 = 0

# 判断逻辑
json_filename = 'skills.json'
with open(json_filename, 'r', encoding='utf-8') as f:
    # 使用 json.load() 从文件对象中读取并解析JSON
    skills_list = json.load(f)
    
skills_dict = {item['技能名称']: item['成功率'] for item in skills_list}

determination_result = None
if return_value_1:
    modifier = None
    if return_value_3 == 0:
        modifier = 1
    elif return_value_3 == 1:
        modifier = 1/2
    elif return_value_3 == 2:
        modifier = 1/5
    else:
        raise ValueError("Difficulty of this determination is invalid.")
    print(modifier)
    print(skills_dict[return_value_2])
    if roll() <= int(math.floor(skills_dict[return_value_2])):
        print("通过")
    else:
        print("不通过")
    