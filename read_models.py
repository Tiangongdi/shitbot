import json

# 方法1：使用内置的 json 模块读取文件
def read_models_json():
    """读取 models.json 文件的全部内容"""
    try:
        with open('d:\\project\\ShitBot\\models.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return None

# 方法2：如果在项目内部，可以使用相对路径
def read_models_json_relative():
    """使用相对路径读取 models.json 文件"""
    try:
        with open('models.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return None

# 示例用法
if __name__ == "__main__":
    # 使用绝对路径
    data1 = read_models_json()
    print("使用绝对路径读取的内容:")
    print(json.dumps(data1, ensure_ascii=False, indent=2))
    
    print("\n" + "="*50 + "\n")
    
    # 使用相对路径
    data2 = read_models_json_relative()
    print("使用相对路径读取的内容:")
    print(json.dumps(data2, ensure_ascii=False, indent=2))
    
    # 访问具体数据
    if data1:
        print("\n" + "="*50 + "\n")
        print("获取所有模型名称:")
        for model in data1.get('domestic_common_models', []):
            print(f"- {model['name']} (value: {model['value']})")
