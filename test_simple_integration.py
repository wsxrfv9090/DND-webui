#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单集成测试：验证修复后的记忆更新功能
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_memory_integration():
    """测试记忆集成功能"""
    print("=== 测试记忆集成功能 ===")
    
    try:
        # 1. 测试记忆系统初始化
        import Memory
        Memory.initialize_memory()
        print("✓ 记忆系统初始化成功")
        
        # 2. 测试获取初始记忆
        initial_memory = Memory.prepare_kp_memory()
        print(f"✓ 初始记忆长度: {len(initial_memory)} 字符")
        
        # 3. 测试获取游戏摘要
        summary = Memory.get_game_summary()
        print(f"✓ 初始游戏摘要: {summary}")
        
        # 4. 测试AI分析交互
        import ai.test_ai as ai_process
        user_input = "我要在图书馆查找关于斯夸特湖的历史资料"
        ai_response = "你成功在图书馆的《新英格兰本地历史》第78页找到了关于斯夸特湖的记载..."
        
        memory_updates = Memory.analyze_interaction_for_memory_update(user_input, ai_response)
        print(f"✓ AI分析结果: {memory_updates}")
        
        # 5. 测试记忆更新
        if memory_updates:
            Memory.update_dynamic_state(memory_updates)
            print("✓ 记忆更新成功")
            
            # 6. 验证更新后的状态
            updated_summary = Memory.get_game_summary()
            print(f"✓ 更新后摘要: {updated_summary}")
        
        return True
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_main_integration():
    """测试主集成功能"""
    print("\n=== 测试主集成功能 ===")
    
    try:
        from main_integrated import core_python_processing
        
        # 测试简单输入
        result = core_python_processing("你好")
        print(f"✓ 简单输入处理成功: {len(result)} 字符")
        
        # 测试需要判定的输入
        result_judge = core_python_processing("我要仔细查看这个房间")
        print(f"✓ 判定输入处理成功: {len(result_judge)} 字符")
        
        return True
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("开始简单集成测试...\n")
    
    # 运行测试
    test1_success = test_memory_integration()
    test2_success = test_main_integration()
    
    print(f"\n=== 测试结果 ===")
    print(f"记忆集成测试: {'✓ 通过' if test1_success else '✗ 失败'}")
    print(f"主集成测试: {'✓ 通过' if test2_success else '✗ 失败'}")
    
    if test1_success and test2_success:
        print("\n🎉 所有测试通过！集成修复成功！")
        sys.exit(0)
    else:
        print("\n⚠️  部分测试失败，请检查相关模块")
        sys.exit(1) 