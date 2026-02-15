from read_models import read_models_json_relative

# 读取模型数据
models_data = read_models_json_relative()

# 访问 domestic_common_models 列表
if models_data and 'domestic_common_models' in models_data:
    models = models_data['domestic_common_models']
    
    # 遍历并打印所有模型
    for i, model in enumerate(models, 1):
        print(f"[{i}] {model['name']} (value: {model['value']})")
    
    # 获取特定索引的模型值
    model_index = 1
    if 1 <= model_index <= len(models):
        model_value = models[int(model_index) - 1]['value']
        print(f"\nSelected model value: {model_value}")
    else:
        print("Invalid model index")
else:
    print("Failed to read models data")