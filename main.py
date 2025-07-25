USER_INPUT = 'HI'
import ai.test_ai as ai_process
import json

user_input = USER_INPUT

# 返回布尔值，是否需要判定
# need_determination = ai_process.determine(user_input)

# 如果需要判定，即need_determination为真
# 则判断需要过哪一个判定，返回一个对应skills.json里面技能名字的字符串
# 如果返回值不是skills.json里面的字符串，就循环再来，直到返回值match skills.json其中的一个名字



# if need_determination:
#     skill = ai_process.choose_skill(user_input)
    
    # 当返回值对应的成功率小于10时，print("")