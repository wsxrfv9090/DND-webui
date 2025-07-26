#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试判定系统修复
"""

import asyncio
import json
from openai import AsyncOpenAI
from bin import utility as util
from bin import apis

async def test_judge_system():
    """测试判定系统"""
    print("=== 测试判定系统 ===")
    
    # 初始化
    client = AsyncOpenAI(api_key=util.API_KEY, base_url=util.BASE_URL)
    world_view = util.load_world_view()
    skills_str = util.get_skills_string()
    
    print(f"技能字符串: {skills_str}")
    print(f"技能字符串长度: {len(skills_str)}")
    
    # 测试用例
    test_cases = [
        "我要侦查这个房间",
        "我想说服这个NPC",
        "我要打开这个门",
        "我想查看这本书",
        "我要开车离开这里"
    ]
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\n--- 测试用例 {i}: {test_input} ---")
        
        # 调用AI分析
        need_judge, skill_name, difficulty = await apis.api_1_analyze_action(
            client=client,
            world_view=world_view,
            skills_str=skills_str,
            user_input=test_input
        )
        
        print(f"AI分析结果: need_judge={need_judge}, skill_name={skill_name}, difficulty={difficulty}")
        
        if need_judge and skill_name:
            # 模拟玩家技能数据
            player_skills = [
                {"技能名称": "侦查", "成功率": 75},
                {"技能名称": "说服", "成功率": 50},
                {"技能名称": "妙手", "成功率": 30},
                {"技能名称": "图书馆使用", "成功率": 60},
                {"技能名称": "驾驶", "成功率": 40}
            ]
            
            success_rate = util.get_skill_success_rate(skill_name, player_skills)
            print(f"技能成功率: {success_rate}")
            
            if success_rate > 0:
                print("✅ 判定系统正常工作")
            else:
                print("❌ 技能未找到或成功率为0")
        else:
            print("ℹ️ 无需判定")

if __name__ == "__main__":
    asyncio.run(test_judge_system()) 