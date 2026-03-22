# AI API 平台 OpenAI SDK 兼容性文档

## 文档概述
本文档汇总了支持 Python OpenAI SDK 的各大 AI API 平台及其 base_url 配置，方便开发者快速切换不同平台。

---

## 一、国内平台

### 1. DeepSeek
- **base_url**: `https://api.deepseek.com/v1`
- **主要模型**: deepseek-chat, deepseek-reasoner, deepseek-r1
- **特点**: 100% 兼容 OpenAI API 格式，支持 Function Calling
- **示例代码**:
```python
from openai import OpenAI

client = OpenAI(
    api_key="your-deepseek-api-key",
    base_url="https://api.deepseek.com/v1"
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "你好"}]
)
```

### 2. 智谱AI (GLM系列)
- **base_url**: `https://open.bigmodel.cn/api/paas/v4/`
- **主要模型**: glm-4, glm-4.7, glm-4v
- **特点**: 完全适配 OpenAI SDK，支持 Claude SDK 兼容
- **示例代码**:
```python
from openai import OpenAI

client = OpenAI(
    api_key="your-zhipuai-api-key",
    base_url="https://open.bigmodel.cn/api/paas/v4/"
)

response = client.chat.completions.create(
    model="glm-4.7",
    messages=[{"role": "user", "content": "你好"}]
)
```

### 3. 月之暗面 Kimi (Moonshot)
- **base_url**: `https://api.moonshot.cn/v1`
- **主要模型**: kimi-k2.5, kimi-k2-turbo-preview, moonshot-v1-8k/32k/128k
- **特点**: 完全兼容 OpenAI API 格式，支持工具调用
- **示例代码**:
```python
from openai import OpenAI

client = OpenAI(
    api_key="your-moonshot-api-key",
    base_url="https://api.moonshot.cn/v1"
)

response = client.chat.completions.create(
    model="kimi-k2-turbo-preview",
    messages=[{"role": "user", "content": "你好"}]
)
```

### 4. 阿里云通义千问 (DashScope)
- **base_url**: `https://dashscope.aliyuncs.com/compatible-mode/v1`
- **主要模型**: qwen-plus, qwen-turbo, qwen-max, qwen-vl-plus
- **特点**: 支持多地域部署，支持视觉模型
- **地域配置**:
  - 北京: `https://dashscope.aliyuncs.com/compatible-mode/v1`
  - 新加坡: `https://dashscope-intl.aliyuncs.com/compatible-mode/v1`
  - 弗吉尼亚: `https://dashscope-us.aliyuncs.com/compatible-mode/v1`
- **示例代码**:
```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

response = client.chat.completions.create(
    model="qwen-plus",
    messages=[{"role": "user", "content": "你好"}]
)
```

### 5. 百度千帆 (ModelBuilder)
- **base_url**: `https://qianfan.baidubce.com/v2`
- **主要模型**: ERNIE系列
- **特点**: 企业级服务，支持模型微调
- **示例代码**:
```python
from openai import OpenAI

client = OpenAI(
    api_key="your-qianfan-api-key",
    base_url="https://qianfan.baidubce.com/v2"
)
```

### 6. 腾讯混元
- **base_url**: `https://api.hunyuan.cloud.tencent.com/v1`
- **主要模型**: hunyuan-lite, hunyuan-standard, hunyuan-pro
- **特点**: 支持多语言 SDK，企业级服务
- **示例代码**:
```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ.get("HUNYUAN_API_KEY"),
    base_url="https://api.hunyuan.cloud.tencent.com/v1"
)

response = client.chat.completions.create(
    model="hunyuan-lite",
    messages=[{"role": "user", "content": "你好"}]
)
```

### 7. 火山方舟
- **特点**: 字节跳动旗下，支持多种开源模型
- **文档**: https://www.volcengine.com/docs/82379/1330626

---

## 二、国外平台

### 1. OpenAI (官方)
- **base_url**: `https://api.openai.com/v1`
- **主要模型**: gpt-4, gpt-4-turbo, gpt-3.5-turbo, gpt-4o
- **特点**: 官方平台，功能最全
- **示例代码**:
```python
from openai import OpenAI

client = OpenAI(
    api_key="your-openai-api-key"
    # base_url 可省略，默认为官方地址
)
```

### 2. Azure OpenAI
- **base_url**: 需根据部署实例配置
- **格式**: `https://YOUR_RESOURCE_NAME.openai.azure.com/`
- **特点**: 企业级服务，数据隐私保护
- **示例代码**:
```python
from openai import OpenAI

client = OpenAI(
    api_key="your-azure-api-key",
    base_url="https://YOUR_RESOURCE_NAME.openai.azure.com/",
    default_headers={"api-key": "your-azure-api-key"}
)
```

### 3. Groq
- **base_url**: `https://api.groq.com/openai/v1`
- **主要模型**: llama-3.3-70b-versatile, mixtral-8x7b-32768, gemma2-9b-it
- **特点**: 极速推理，支持 Responses API
- **示例代码**:
```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": "Hello"}]
)
```

### 4. Together.ai
- **base_url**: `https://api.together.xyz/v1`
- **主要模型**: meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8, openai/gpt-oss-20b
- **特点**: 支持多种开源模型，价格实惠
- **示例代码**:
```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ.get("TOGETHER_API_KEY"),
    base_url="https://api.together.xyz/v1"
)

response = client.chat.completions.create(
    model="meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
    messages=[{"role": "user", "content": "Hello"}]
)
```

### 5. OpenRouter
- **base_url**: `https://openrouter.ai/api/v1`
- **主要模型**: 支持 293+ 种模型
- **特点**: 统一接口访问多种模型，自动格式转换
- **示例代码**:
```python
from openai import OpenAI

client = OpenAI(
    api_key="your-openrouter-api-key",
    base_url="https://openrouter.ai/api/v1"
)

response = client.chat.completions.create(
    model="anthropic/claude-3.5-sonnet",
    messages=[{"role": "user", "content": "Hello"}]
)
```

### 6. Perplexity AI
- **base_url**: `https://api.perplexity.ai/v1`
- **主要模型**: llama-3.1-sonar-small-128k-online, llama-3.1-sonar-large-128k-online
- **特点**: 在线搜索增强，实时信息
- **示例代码**:
```python
from openai import OpenAI

client = OpenAI(
    api_key="your-perplexity-api-key",
    base_url="https://api.perplexity.ai/v1"
)
```

### 7. Mistral AI
- **base_url**: `https://api.mistral.ai/v1`
- **主要模型**: mistral-large-latest, mistral-medium, codestral-latest
- **特点**: 欧洲领先 AI 公司，支持代码生成
- **示例代码**:
```python
from openai import OpenAI

client = OpenAI(
    api_key="your-mistral-api-key",
    base_url="https://api.mistral.ai/v1"
)
```

### 8. Cerebras
- **base_url**: `https://api.cerebras.ai/v1`
- **特点**: 高速推理
- **示例代码**:
```python
from openai import OpenAI

client = OpenAI(
    api_key="your-cerebras-api-key",
    base_url="https://api.cerebras.ai/v1"
)
```

### 9. Anyscale
- **base_url**: `https://api.endpoints.anyscale.com/v1`
- **特点**: 可扩展的模型服务
- **示例代码**:
```python
from openai import OpenAI

client = OpenAI(
    api_key="your-anyscale-api-key",
    base_url="https://api.endpoints.anyscale.com/v1"
)
```

---

## 三、快速切换指南

### 统一调用模式
所有平台都遵循相同的调用模式，只需修改三个参数：

```python
from openai import OpenAI

# 1. 创建客户端时配置
client = OpenAI(
    api_key="your-api-key",        # 各平台的 API Key
    base_url="platform-base-url"   # 各平台的 base_url
)

# 2. 调用方式完全一致
response = client.chat.completions.create(
    model="model-name",            # 各平台支持的模型名称
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "你好"}
    ]
)

print(response.choices[0].message.content)
```

### 环境变量配置建议
推荐使用环境变量管理 API Key：

```python
import os
from openai import OpenAI

# 配置示例
PLATFORMS = {
    "deepseek": {
        "api_key": os.getenv("DEEPSEEK_API_KEY"),
        "base_url": "https://api.deepseek.com/v1"
    },
    "zhipu": {
        "api_key": os.getenv("ZHIPUAI_API_KEY"),
        "base_url": "https://open.bigmodel.cn/api/paas/v4/"
    },
    "moonshot": {
        "api_key": os.getenv("MOONSHOT_API_KEY"),
        "base_url": "https://api.moonshot.cn/v1"
    },
    "qwen": {
        "api_key": os.getenv("DASHSCOPE_API_KEY"),
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1"
    },
    "groq": {
        "api_key": os.getenv("GROQ_API_KEY"),
        "base_url": "https://api.groq.com/openai/v1"
    }
}

# 动态选择平台
def get_client(platform_name):
    config = PLATFORMS[platform_name]
    return OpenAI(
        api_key=config["api_key"],
        base_url=config["base_url"]
    )
```

---

## 四、平台对比表

| 平台 | base_url | 主要特点 | 推荐场景 |
|------|----------|----------|----------|
| **DeepSeek** | `https://api.deepseek.com/v1` | 性价比高，支持推理模型 | 日常开发、推理任务 |
| **智谱AI** | `https://open.bigmodel.cn/api/paas/v4/` | 中文能力强，多模态 | 中文应用、企业服务 |
| **Kimi** | `https://api.moonshot.cn/v1` | 长文本处理，联网搜索 | 文档处理、信息检索 |
| **通义千问** | `https://dashscope.aliyuncs.com/compatible-mode/v1` | 多地域部署，企业级 | 企业应用、多模态 |
| **Groq** | `https://api.groq.com/openai/v1` | 极速推理 | 实时应用、高并发 |
| **Together.ai** | `https://api.together.xyz/v1` | 模型丰富，价格实惠 | 实验开发、多模型对比 |
| **OpenRouter** | `https://openrouter.ai/api/v1` | 统一接口，模型最多 | 多模型切换、测试 |

---

## 五、注意事项

### 1. API Key 安全
- 不要在代码中硬编码 API Key
- 使用环境变量或配置文件管理
- 定期轮换 API Key

### 2. 模型名称差异
- 各平台的模型名称不同，需要查阅对应文档
- 部分平台支持模型别名

### 3. 功能兼容性
- 不是所有平台都支持 OpenAI 的全部功能
- 例如：Function Calling、Vision、Fine-tuning 等功能的支持程度不同
- 使用前请查阅平台文档确认

### 4. 速率限制
- 各平台有不同的速率限制（RPM/TPM）
- 建议实现重试机制和错误处理

### 5. 费用差异
- 各平台定价策略不同
- 建议根据使用场景选择性价比最高的平台

---

## 六、常见问题

### Q1: 如何选择合适的平台？
**A**: 根据需求选择：
- 追求速度：Groq
- 追求性价比：DeepSeek、Together.ai
- 中文场景：智谱AI、通义千问、Kimi
- 企业级服务：Azure OpenAI、阿里云、百度千帆
- 多模型测试：OpenRouter

### Q2: 是否可以在不同平台间无缝切换？
**A**: 大部分场景可以，但需要注意：
- 模型名称需要修改
- 部分高级功能可能不支持
- 输出风格可能有差异

### Q3: 如何处理平台特有的参数？
**A**: 使用 `extra_body` 参数传递平台特有参数：
```python
response = client.chat.completions.create(
    model="model-name",
    messages=[...],
    extra_body={
        "platform_specific_param": "value"
    }
)
```

---

## 七、更新日志

- **2026-02-13**: 初始版本，汇总国内外主流 AI API 平台

---

## 八、参考链接

- [DeepSeek API 文档](https://api-docs.deepseek.com/)
- [智谱AI 开放平台](https://open.bigmodel.cn/)
- [Moonshot AI 开放平台](https://platform.moonshot.cn/)
- [阿里云 DashScope](https://help.aliyun.com/zh/model-studio/)
- [Groq 文档](https://console.groq.com/docs)
- [Together.ai 文档](https://docs.together.ai/)
- [OpenRouter 文档](https://openrouter.ai/docs)

---

**文档维护**: 偷摸零 (ShitBot Assistant)  
**最后更新**: 2026-02-13
