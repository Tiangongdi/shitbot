---
name: ppt-generator
description: PPT演示文稿生成工具。基于用户提供的内容自动生成专业风格的PowerPoint演示文稿。当用户需要：(1) 生成PPT演示文稿，(2) 将文档转换为PPT，(3) 创建演示幻灯片，(4) 制作报告PPT时使用此技能。触发词：PPT、演示文稿、幻灯片、PowerPoint、生成PPT、制作PPT。
---

# PPT Generator Skill

快速生成专业风格的PowerPoint演示文稿。

## 快速开始

### 基本使用流程

1. **收集内容**：从用户处获取PPT主题和内容要点
2. **规划结构**：确定幻灯片数量和类型（封面、目录、内容页、双栏页、结束页）
3. **生成脚本**：使用 `scripts/create_ppt.py` 生成PPT
4. **执行脚本**：运行脚本生成最终文件

### 一键生成演示

```bash
# 使用虚拟环境中的Python执行
D:\project\ShitBot\shitbot_env\Scripts\python.exe scripts/create_ppt.py
```

**重要**：必须使用虚拟环境中的Python解释器，否则会找不到python-pptx模块。

## API参考

### PPTGenerator类

```python
from create_ppt import PPTGenerator

# 创建生成器实例
generator = PPTGenerator("我的演示文稿")
```

### 方法列表

#### 1. add_title_slide() - 添加标题页

用于封面和结束页。

```python
generator.add_title_slide(
    title="主标题",
    subtitle="副标题",      # 可选
    date="2026年3月14日"   # 可选，默认当前日期
)
```

**特点**：
- 深蓝色背景（RGB: 31, 73, 125）
- 大标题居中，白色粗体
- 副标题灰色，较小字号

#### 2. add_content_slide() - 添加内容页

用于展示列表、要点、说明性内容。

```python
generator.add_content_slide(
    title="页面标题",
    content_list=[
        "要点一",
        "要点二",
        ("主要点", ["子要点1", "子要点2"]),  # 支持二级列表
        "要点三"
    ]
)
```

**特点**：
- 蓝色标题栏
- 白色背景内容区
- 支持多级列表
- 自动换行

#### 3. add_two_column_slide() - 添加双栏页

用于对比、分类展示。

```python
generator.add_two_column_slide(
    title="对比分析",
    left_title="方案A",
    left_content=["优点1", "优点2", "缺点1"],
    right_title="方案B",
    right_content=["优点1", "优点2", "缺点1"]
)
```

**特点**：
- 左右两栏布局
- 各栏独立标题
- 项目符号列表
- 对称设计

#### 4. add_section_slide() - 添加章节分隔页

用于章节导航。

```python
generator.add_section_slide(
    section_title="章节标题",
    section_number=1  # 可选
)
```

#### 5. add_table_slide() - 添加表格页

用于数据展示。

```python
generator.add_table_slide(
    title="数据表格",
    headers=["列1", "列2", "列3"],
    rows=[
        ["数据1", "数据2", "数据3"],
        ["数据4", "数据5", "数据6"]
    ]
)
```

#### 6. add_image_slide() - 添加图片页

用于图片展示。

```python
generator.add_image_slide(
    title="图片展示",
    image_path="/path/to/image.png",
    caption="图片说明"  # 可选
)
```

#### 7. save() - 保存文件

```python
# 保存到默认位置（脚本所在目录）
output_path = generator.save()

# 或指定保存路径
output_path = generator.save("D:/output/my_presentation.pptx")
```

## 幻灯片类型详解

### 1. 标题页（Title Slide）

**适用场景**：
- 演示文稿封面
- 章节分隔页
- 结束致谢页

**设计规范**：
- 背景：深蓝色 RGB(31, 73, 125)
- 标题：54pt 白色粗体
- 副标题：28pt 浅灰色
- 日期：16pt 浅灰色

### 2. 内容页（Content Slide）

**适用场景**：
- 文字说明
- 要点列表
- 流程步骤
- 数据展示

**设计规范**：
- 标题栏：深蓝色背景
- 标题：36pt 白色粗体
- 正文：22pt 深灰色
- 每页建议不超过8个要点

### 3. 双栏页（Two-Column Slide）

**适用场景**：
- 对比分析
- 优缺点列举
- 分类说明
- 正反观点

**设计规范**：
- 栏标题：28pt 深蓝色粗体
- 栏内容：18pt 深灰色
- 中间分隔线

### 4. 表格页（Table Slide）

**适用场景**：
- 数据对比
- 计划安排
- 信息汇总

**设计规范**：
- 表头：深蓝色背景，白色粗体
- 数据行：交替背景色
- 字号：20pt

## 设计规范

### 颜色方案

```
主色调：深蓝色 RGB(31, 73, 125)
背景色：白色 RGB(255, 255, 255)
文字色：深灰 RGB(50, 50, 50)
副标题：浅灰 RGB(200, 200, 200)
强调色：浅蓝 RGB(68, 114, 196)
浅背景：浅蓝 RGB(240, 245, 250)
```

### 字体大小

```
封面标题：54pt 粗体
页面标题：36pt 粗体
正文内容：22pt
双栏内容：18pt
副标题：28pt
小字：16pt
```

### 页面尺寸

```
宽度：13.333 英寸（16:9宽屏）
高度：7.5 英寸
```

## 内容组织建议

### 标准结构

1. **封面** - 标题、副标题、日期
2. **目录** - 章节导航
3. **内容页** - 按章节展开
4. **总结** - 核心要点回顾
5. **结束页** - 致谢或联系方式

### 内容密度

- 每页不超过 8 个要点
- 每个要点不超过 2 行
- 适当使用空行分隔
- 重要内容可单独成页

## 使用示例

### 示例1：项目汇报PPT

```python
from create_ppt import PPTGenerator

generator = PPTGenerator("项目汇报")

# 封面
generator.add_title_slide(
    "XX项目汇报",
    "项目进展与成果展示",
    "2026年3月"
)

# 目录
generator.add_content_slide("目录", [
    "项目背景",
    "实施进展",
    "阶段性成果",
    "下一步计划"
])

# 内容页
generator.add_content_slide("项目背景", [
    "项目目标：提升用户体验",
    "项目周期：2025年1月-2026年6月",
    ("核心挑战", [
        "技术架构升级",
        "数据迁移风险"
    ])
])

# 双栏对比
generator.add_two_column_slide(
    "方案对比",
    "原方案",
    ["成本较低", "周期较短", "风险较高"],
    "新方案",
    ["成本较高", "周期较长", "风险可控"]
)

# 表格
generator.add_table_slide(
    "进度安排",
    ["阶段", "时间", "任务"],
    [
        ["第一阶段", "1-3月", "需求调研"],
        ["第二阶段", "4-6月", "系统开发"]
    ]
)

# 结束页
generator.add_title_slide("感谢聆听", "欢迎提问")

generator.save()
```

### 示例2：培训课件PPT

```python
from create_ppt import PPTGenerator

generator = PPTGenerator("Python入门培训")

# 封面
generator.add_title_slide(
    "Python编程入门",
    "从零开始学习Python",
    "培训讲师：XXX"
)

# 章节分隔
generator.add_section_slide("第一章：Python基础", 1)

# 内容
generator.add_content_slide("Python简介", [
    "Python是一种解释型编程语言",
    "由Guido van Rossum于1991年创建",
    ("特点", [
        "语法简洁易学",
        "丰富的标准库",
        "跨平台兼容"
    ])
])

generator.save()
```

## 高级功能

### 自定义样式

如需自定义颜色或字体，修改 `scripts/create_ppt.py` 中的以下参数：

```python
# 修改主色调
COLORS = {
    'primary': RGBColor(31, 73, 125),  # 改为其他RGB值
    ...
}

# 修改字体大小
FONT_SIZES = {
    'title': 54,  # 改为其他字号
    ...
}
```

### 添加图片

```python
generator.add_image_slide(
    title="产品展示",
    image_path="D:/images/product.png",
    caption="产品外观图"
)
```

### 批量生成

```python
# 从数据批量生成内容页
topics = [
    ("主题1", ["要点1", "要点2"]),
    ("主题2", ["要点1", "要点2"]),
]

for title, content in topics:
    generator.add_content_slide(title, content)
```

## 常见问题

### Q: 找不到python-pptx模块？

**解决方案**：使用虚拟环境中的Python解释器：
```bash
D:\project\ShitBot\shitbot_env\Scripts\python.exe your_script.py
```

### Q: 如何修改幻灯片顺序？

**解决方案**：在脚本中调整 `add_*_slide()` 函数的调用顺序。

### Q: 如何添加动画效果？

**解决方案**：python-pptx暂不支持动画，需在PowerPoint中手动添加。

### Q: 生成的PPT文件在哪里？

**解决方案**：默认保存到脚本所在目录，可在 `save()` 方法中指定路径。

### Q: 如何修改配色方案？

**解决方案**：修改 `PPTGenerator.COLORS` 字典中的颜色值。

## 最佳实践

1. **内容优先**：先整理好内容大纲，再生成PPT
2. **简洁明了**：每页聚焦一个主题
3. **视觉一致**：使用统一的设计风格
4. **适当留白**：避免内容过于拥挤
5. **测试预览**：生成后检查效果，必要时调整

## 工作流程

### 从文档生成PPT

1. 读取文档内容
2. 提取标题和要点
3. 规划幻灯片结构
4. 生成PPT脚本
5. 执行脚本输出文件

### 从零创建PPT

1. 询问用户主题和内容
2. 设计幻灯片结构
3. 编写内容要点
4. 生成并执行脚本
5. 交付PPT文件

## 参考资源

- [python-pptx官方文档](https://python-pptx.readthedocs.io/)
- [设计模式参考](references/design_patterns.md) - 更多幻灯片设计模式
