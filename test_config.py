import os
import yaml
import tempfile
from config import load_config, create_default_config

# 测试 1: 测试空配置文件
def test_empty_config():
    print("=== 测试 1: 空配置文件 ===")
    
    # 创建临时空配置文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        temp_config_path = f.name
    
    try:
        # 写入空内容
        with open(temp_config_path, 'w', encoding='utf-8') as f:
            f.write('')
        
        # 加载配置
        config = load_config(temp_config_path)
        print("✓ 成功加载空配置文件")
        print(f"  - 用户名称: {config.user.user_name}")
        print(f"  - 机器人名称: {config.user.bot_name}")
        print(f"  - AI API: {config.ai.value}")
        print(f"  - 默认提供者: {config.default_provider}")
    finally:
        # 清理临时文件
        if os.path.exists(temp_config_path):
            os.unlink(temp_config_path)

# 测试 2: 测试不存在的配置文件
def test_nonexistent_config():
    print("\n=== 测试 2: 不存在的配置文件 ===")
    
    # 使用不存在的文件路径
    nonexistent_path = "nonexistent_config.yaml"
    
    try:
        # 确保文件不存在
        if os.path.exists(nonexistent_path):
            os.unlink(nonexistent_path)
        
        # 加载配置
        config = load_config(nonexistent_path)
        print("✓ 成功处理不存在的配置文件")
        print(f"  - 用户名称: {config.user.user_name}")
        print(f"  - 机器人名称: {config.user.bot_name}")
        print(f"  - AI API: {config.ai.value}")
        print(f"  - 默认提供者: {config.default_provider}")
    finally:
        # 清理临时文件
        if os.path.exists(nonexistent_path):
            os.unlink(nonexistent_path)

# 测试 3: 测试正常配置文件
def test_normal_config():
    print("\n=== 测试 3: 正常配置文件 ===")
    
    # 创建临时配置文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        temp_config_path = f.name
    
    try:
        # 写入测试配置
        test_config = {
            'user': {
                'user_name': 'TestUser',
                'bot_name': 'TestBot'
            },
            'ai': {
                'api_key': 'test_key',
                'value': 'openai',
                'model': 'gpt-3.5-turbo'
            }
        }
        
        with open(temp_config_path, 'w', encoding='utf-8') as f:
            yaml.dump(test_config, f, allow_unicode=True)
        
        # 加载配置
        config = load_config(temp_config_path)
        print("✓ 成功加载正常配置文件")
        print(f"  - 用户名称: {config.user.user_name}")
        print(f"  - 机器人名称: {config.user.bot_name}")
        print(f"  - AI API: {config.ai.value}")
        print(f"  - AI 模型: {config.ai.model}")
        print(f"  - 默认提供者: {config.default_provider}")
    finally:
        # 清理临时文件
        if os.path.exists(temp_config_path):
            os.unlink(temp_config_path)

if __name__ == "__main__":
    print("开始测试配置加载功能...")
    test_empty_config()
    test_nonexistent_config()
    test_normal_config()
    print("\n所有测试完成！")
