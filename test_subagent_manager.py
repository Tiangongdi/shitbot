from src.agent.subagent_manager import get_subagent_manager

# 获取SubAgent管理器单例
manager = get_subagent_manager()

# 打印初始subagent字典
print("初始subagent字典:", manager.subagent)

# 添加一些测试数据
manager.subagent["test_agent"] = {
    "name": "测试智能体",
    "role": "test",
    "description": "用于测试的智能体"
}

# 打印修改后的subagent字典
print("修改后的subagent字典:", manager.subagent)

# 保存到文件
save_result = manager.save_subagents()
print("保存结果:", save_result)

# 重新获取管理器实例（应该是同一个单例）
manager2 = get_subagent_manager()
print("重新获取的管理器subagent字典:", manager2.subagent)

print("测试完成!")
