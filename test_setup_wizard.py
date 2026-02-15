#!/usr/bin/env python3
"""
测试 setup_wizard 函数的模型选择部分
"""
import sys
import os

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import setup_wizard
from read_models import read_models_json_relative

def test_model_selection():
    """测试模型选择功能"""
    print("=== 测试模型选择功能 ===")
    
    # 测试读取模型数据
    models_data = read_models_json_relative()
    print(f"读取模型数据: {models_data is not None}")
    
    if models_data and 'domestic_common_models' in models_data:
        models = models_data['domestic_common_models']
        print(f"获取到 {len(models)} 个模型")
        print("模型列表:")
        for i, model in enumerate(models, 1):
            print(f"[{i}] {model['name']} (value: {model['value']})")
    else:
        print("警告: 无法读取 models.json 文件")
    
    print("\n测试完成！")

if __name__ == "__main__":
    test_model_selection()
