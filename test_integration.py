#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
集成测试文件：测试main.py、test_ai.py和memory.py的完整集成
"""

import sys
import os
import json
import time

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_memory_system():
    """测试记忆系统"""
    print("=== 测试记忆系统 ===")
    try:
        import Memory
        
        # 初始化记忆系统
        Memory.initialize_memory()
        print("✓ 记忆系统初始化成功")
        
        # 获取初始记忆
        initial_memory = Memory.prepare_kp_memory()
        print(f"✓ 初始记忆长度: {len(initial_memory)} 字符")
        
        # 获取游戏摘要
        summary = Memory.get_game_summary()
        print(f"✓ 游戏摘要: {summary}")
        
        return True
    except Exception as e:
        print(f"✗ 记忆系统测试失败: {e}")
        return False

def test_ai_system():
    """测试AI系统"""
    print("\n=== 测试AI系统 ===")
    try:
        import ai.test_ai as ai_process
        
        # 测试基础功能
        test_input = "我要侦查这个房间"
        need_judge, skill_name, difficulty = ai_process.analyze_action(test_input)
        print(f"✓ 基础判定分析: 需要判定={need_judge}, 技能={skill_name}, 难度={difficulty}")
        
        # 测试带记忆的判定分析
        complete_memory = "测试记忆内容"
        need_judge_mem, skill_name_mem, difficulty_mem = ai_process.analyze_action_with_memory(test_input, complete_memory)
        print(f"✓ 带记忆判定分析: 需要判定={need_judge_mem}, 技能={skill_name_mem}, 难度={difficulty_mem}")
        
        # 测试描述生成
        description = ai_process.generate_description(test_input)
        print(f"✓ 描述生成: {len(description)} 字符")
        
        # 测试带记忆的描述生成
        description_mem = ai_process.generate_description_with_memory(test_input, None, complete_memory)
        print(f"✓ 带记忆描述生成: {len(description_mem)} 字符")
        
        return True
    except Exception as e:
        print(f"✗ AI系统测试失败: {e}")
        return False

def test_integrated_processing():
    """测试集成处理"""
    print("\n=== 测试集成处理 ===")
    try:
        from main_integrated import core_python_processing
        
        # 测试简单输入
        test_input = "你好"
        result = core_python_processing(test_input)
        print(f"✓ 简单输入处理: {len(result)} 字符")
        
        # 测试需要判定的输入
        test_input_judge = "我要仔细查看这个房间的每个角落"
        result_judge = core_python_processing(test_input_judge)
        print(f"✓ 判定输入处理: {len(result_judge)} 字符")
        
        return True
    except Exception as e:
        print(f"✗ 集成处理测试失败: {e}")
        return False

def test_memory_updates():
    """测试记忆更新"""
    print("\n=== 测试记忆更新 ===")
    try:
        import Memory
        import ai.test_ai as ai_process
        
        # 模拟一次交互
        user_input = "我在图书馆找到了关于斯夸特湖的历史记录"
        ai_response = "你成功在图书馆的《新英格兰本地历史》第78页找到了关于斯夸特湖的记载..."
        
        # 分析交互并生成记忆更新
        memory_updates = Memory.analyze_interaction_for_memory_update(user_input, ai_response)
        print(f"✓ 记忆更新分析: {memory_updates}")
        
        # 检查更新后的摘要
        updated_summary = Memory.get_game_summary()
        print(f"✓ 更新后摘要: {updated_summary}")
        
        return True
    except Exception as e:
        print(f"✗ 记忆更新测试失败: {e}")
        return False

def test_api_endpoints():
    """测试API端点"""
    print("\n=== 测试API端点 ===")
    try:
        from main_integrated import core_python_processing
        
        # 测试核心处理函数
        result = core_python_processing("测试消息")
        print(f"✓ 核心处理: {len(result)} 字符")
        
        return True
    except Exception as e:
        print(f"✗ API端点测试失败: {e}")
        return False

def run_all_tests():
    """运行所有测试"""
    print("开始运行集成测试...\n")
    
    tests = [
        ("记忆系统", test_memory_system),
        ("AI系统", test_ai_system),
        ("集成处理", test_integrated_processing),
        ("记忆更新", test_memory_updates),
        ("API端点", test_api_endpoints)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✓ {test_name} 测试通过\n")
            else:
                print(f"✗ {test_name} 测试失败\n")
        except Exception as e:
            print(f"✗ {test_name} 测试异常: {e}\n")
    
    print(f"=== 测试结果 ===")
    print(f"通过: {passed}/{total}")
    print(f"成功率: {passed/total*100:.1f}%")
    
    if passed == total:
        print("🎉 所有测试通过！集成成功！")
        return True
    else:
        print("⚠️  部分测试失败，请检查相关模块")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 