import random
import math


# Test data
STR = 10
DEX = 17
CON = 7
INT = 12
WIS = 13
CHA = 9



def roll_d20(
    ) -> int:
    """
    模拟掷一个20面骰子 (d20)，返回1到20之间的整数。
    """
    return random.randint(1, 20)

def ability_modifier(
    ability_value: int,
    
) -> int:
    return (value - 10) // 2
# def determine(
#     attribute_name: str,
#     attribute_value:
    
# ) -> bool:
    