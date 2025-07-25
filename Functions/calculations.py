import random


# Test data
STR = 10
DEX = 17
CON = 7
INT = 12
WIS = 13
CHA = 9
SAN = 38



def roll_d100(
    ) -> int:
    """
    模拟掷一个100面骰子 (d100)，返回1到20之间的整数。
    """
    return random.randint(1, 100)

def ability_modifier(
    ability_value: int,
    
) -> int:
    return (ability_value - 10) // 2
