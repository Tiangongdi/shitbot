---
name: ui-ux-pro-max
description: UI/UX design intelligence. 67 styles, 96 palettes, 57 fonts, 99 UX guidelines, 25 charts, 13 stacks.
version: 2.0.0
---

# ui-ux-pro-max

> 🎨 **智能 UI/UX 设计助手** - 从需求到设计系统，一站式解决方案

## 快速开始

### 一键生成设计系统

```bash
# 基础用法
python3 skills/ui-ux-pro-max/scripts/search.py "你的需求" --design-system -p "项目名称"

# 示例：SaaS 产品
python3 skills/ui-ux-pro-max/scripts/search.py "SaaS dashboard analytics" --design-system -p "DataFlow"

# 示例：电商网站
python3 skills/ui-ux-pro-max/scripts/search.py "e-commerce luxury fashion" --design-system -p "LuxeStore"
```

### 持久化设计系统

```bash
# 保存到文件系统（Master + Overrides 模式）
python3 skills/ui-ux-pro-max/scripts/search.py "需求" --design-system --persist -p "项目名"

# 创建页面特定覆盖
python3 skills/ui-ux-pro-max/scripts/search.py "需求" --design-system --persist -p "项目名" --page "dashboard"
```

**文件结构：**
```
design-system/
└── project-name/
    ├── MASTER.md          # 全局设计规则
    └── pages/
        ├── dashboard.md   # Dashboard 页面覆盖
        ├── checkout.md    # Checkout 页面覆盖
        └── ...
```

## 核心功能

### 1. 设计系统生成

**输入：** 产品类型 + 行业 + 关键词  
**输出：** 完整设计系统（风格、配色、字体、布局、组件规范）

**示例输出：**
```
+------------------------------------------------------------------------------------------+
|  TARGET: DATAFLOW - RECOMMENDED DESIGN SYSTEM                                           |
+------------------------------------------------------------------------------------------+
|                                                                                          |
|  PATTERN: Data-Dense Dashboard                                                          |
|     Conversion: High information density, real-time updates                             |
|     CTA: Top-right corner, always visible                                               |
|     Sections:                                                                            |
|       1. KPI Cards Row                                                                   |
|       2. Main Chart Area                                                                 |
|       3. Data Table                                                                      |
|                                                                                          |
|  STYLE: Dark Mode (OLED)                                                                 |
|     Keywords: dark, high contrast, eye-friendly, power efficient                        |
|     Best For: Analytics dashboards, monitoring tools, developer tools                   |
|     Performance: Excellent | Accessibility: WCAG AAA                                    |
|                                                                                          |
|  COLORS:                                                                                 |
|     Primary:    #2563EB                                                                  |
|     Secondary:  #3B82F6                                                                  |
|     CTA:        #F97316                                                                  |
|     Background: #0F172A                                                                  |
|     Text:       #F8FAFC                                                                  |
|                                                                                          |
|  TYPOGRAPHY: Inter / Inter                                                               |
|     Mood: Clean, modern, professional                                                    |
|     Google Fonts: https://fonts.google.com/specimen/Inter                               |
|                                                                                          |
|  KEY EFFECTS:                                                                            |
|     Minimal glow effects, vibrant neon accents, high contrast text                      |
|                                                                                          |
|  AVOID (Anti-patterns):                                                                  |
|     ❌ Low contrast text                                                                 |
|     ❌ Heavy animations on data updates                                                  |
|     ❌ Cluttered layouts without visual hierarchy                                        |
|                                                                                          |
|  PRE-DELIVERY CHECKLIST:                                                                 |
|     [ ] No emojis as icons (use SVG: Heroicons/Lucide)                                  |
|     [ ] cursor-pointer on all clickable elements                                        |
|     [ ] Hover states with smooth transitions (150-300ms)                                |
|     [ ] Light mode: text contrast 4.5:1 minimum                                         |
|     [ ] Focus states visible for keyboard nav                                           |
|     [ ] prefers-reduced-motion respected                                                |
|     [ ] Responsive: 375px, 768px, 1024px, 1440px                                        |
+------------------------------------------------------------------------------------------+
```

### 2. 领域搜索

| 领域 | 用途 | 示例关键词 |
|------|------|-----------|
| `product` | 产品类型推荐 | SaaS, e-commerce, healthcare, fintech |
| `style` | UI 风格、效果 | glassmorphism, minimalism, dark mode |
| `color` | 配色方案 | saas, ecommerce, healthcare |
| `typography` | 字体搭配 | elegant, playful, professional |
| `landing` | 落地页结构 | hero, testimonial, pricing |
| `chart` | 图表类型 | trend, comparison, funnel |
| `ux` | UX 最佳实践 | animation, accessibility, z-index |

```bash
# 搜索特定领域
python3 skills/ui-ux-pro-max/scripts/search.py "glassmorphism dark" --domain style
python3 skills/ui-ux-pro-max/scripts/search.py "real-time dashboard" --domain chart
python3 skills/ui-ux-pro-max/scripts/search.py "animation accessibility" --domain ux
```

### 3. 技术栈指南

支持 13 种技术栈：`html-tailwind`, `react`, `nextjs`, `vue`, `svelte`, `swiftui`, `react-native`, `flutter`, `shadcn`, `jetpack-compose`, `astro`, `nuxtjs`, `nuxt-ui`

```bash
# 获取技术栈特定指南
python3 skills/ui-ux-pro-max/scripts/search.py "responsive layout" --stack html-tailwind
python3 skills/ui-ux-pro-max/scripts/search.py "performance optimization" --stack react
```

## 工作流程

### Step 1: 分析需求

从用户请求中提取：
- **产品类型**: SaaS, e-commerce, dashboard, landing page
- **风格关键词**: minimal, playful, professional, elegant
- **行业**: healthcare, fintech, gaming, education
- **技术栈**: React, Vue, Next.js（默认 html-tailwind）

### Step 2: 生成设计系统（必需）

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<产品类型> <行业> <关键词>" --design-system -p "项目名"
```

**自动执行：**
1. 并行搜索 5 个领域（product, style, color, landing, typography）
2. 应用推理规则选择最佳匹配
3. 返回完整设计系统 + 反模式警告

### Step 3: 补充详细搜索（可选）

```bash
# 获取更多风格选项
python3 skills/ui-ux-pro-max/scripts/search.py "glassmorphism dark" --domain style

# 获取 UX 最佳实践
python3 skills/ui-ux-pro-max/scripts/search.py "animation accessibility" --domain ux

# 获取图表推荐
python3 skills/ui-ux-pro-max/scripts/search.py "real-time monitoring" --domain chart
```

### Step 4: 技术栈指南（默认 html-tailwind）

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "layout responsive form" --stack html-tailwind
```

## 输出格式

```bash
# ASCII 格式（默认）- 适合终端显示
python3 skills/ui-ux-pro-max/scripts/search.py "fintech crypto" --design-system

# Markdown 格式 - 适合文档
python3 skills/ui-ux-pro-max/scripts/search.py "fintech crypto" --design-system -f markdown

# JSON 格式 - 适合程序处理
python3 skills/ui-ux-pro-max/scripts/search.py "fintech crypto" --design-system --json
```

## 专业 UI 规则

### 图标与视觉元素

| 规则 | ✅ 推荐 | ❌ 避免 |
|------|--------|--------|
| **图标** | 使用 SVG 图标（Heroicons, Lucide） | 使用 emoji 作为 UI 图标 |
| **悬停状态** | 使用颜色/透明度过渡 | 使用会改变布局的缩放变换 |
| **品牌 Logo** | 从 Simple Icons 获取官方 SVG | 猜测或使用错误的 Logo 路径 |
| **图标尺寸** | 固定 viewBox (24x24) + w-6 h-6 | 随机混合不同图标尺寸 |

### 交互与光标

| 规则 | ✅ 推荐 | ❌ 避免 |
|------|--------|--------|
| **光标** | 所有可点击元素添加 `cursor-pointer` | 交互元素使用默认光标 |
| **悬停反馈** | 提供视觉反馈（颜色、阴影、边框） | 没有交互指示 |
| **过渡** | 使用 `transition-colors duration-200` | 瞬间状态变化或过慢（>500ms） |

### 明暗模式对比度

| 规则 | ✅ 推荐 | ❌ 避免 |
|------|--------|--------|
| **玻璃卡片亮色模式** | 使用 `bg-white/80` 或更高透明度 | 使用 `bg-white/10`（太透明） |
| **文本对比度亮色** | 使用 `#0F172A` (slate-900) | 使用 `#94A3B8` (slate-400) 作为正文 |
| **弱化文本亮色** | 使用 `#475569` (slate-600) 最小值 | 使用 gray-400 或更浅 |
| **边框可见性** | 亮色模式使用 `border-gray-200` | 使用 `border-white/10`（不可见） |

### 布局与间距

| 规则 | ✅ 推荐 | ❌ 避免 |
|------|--------|--------|
| **浮动导航栏** | 添加 `top-4 left-4 right-4` 间距 | 导航栏紧贴 `top-0 left-0 right-0` |
| **内容内边距** | 考虑固定导航栏高度 | 让内容隐藏在固定元素后面 |
| **一致的最大宽度** | 使用相同的 `max-w-6xl` 或 `max-w-7xl` | 混合不同的容器宽度 |

## 交付前检查清单

### 视觉质量
- [ ] 没有使用 emoji 作为图标（使用 SVG）
- [ ] 所有图标来自一致的图标集（Heroicons/Lucide）
- [ ] 品牌 Logo 正确（从 Simple Icons 验证）
- [ ] 悬停状态不会导致布局偏移
- [ ] 直接使用主题颜色（bg-primary）而不是 var() 包装器

### 交互
- [ ] 所有可点击元素都有 `cursor-pointer`
- [ ] 悬停状态提供清晰的视觉反馈
- [ ] 过渡平滑（150-300ms）
- [ ] 焦点状态对键盘导航可见

### 明暗模式
- [ ] 亮色模式文本有足够的对比度（4.5:1 最小值）
- [ ] 玻璃/透明元素在亮色模式中可见
- [ ] 边框在两种模式中都可见
- [ ] 交付前测试两种模式

### 布局
- [ ] 浮动元素与边缘有适当的间距
- [ ] 没有内容隐藏在固定导航栏后面
- [ ] 在 375px, 768px, 1024px, 1440px 响应式
- [ ] 移动端没有水平滚动

### 可访问性
- [ ] 所有图片都有 alt 文本
- [ ] 表单输入都有标签
- [ ] 颜色不是唯一的指示器
- [ ] 尊重 `prefers-reduced-motion`

## 高级用法

### 1. 智能页面覆盖

系统会根据页面类型自动生成智能覆盖：

```bash
# Dashboard 页面会自动推荐数据密集布局
python3 skills/ui-ux-pro-max/scripts/search.py "SaaS analytics" --design-system --persist -p "DataApp" --page "dashboard"

# Checkout 页面会自动推荐转化优化布局
python3 skills/ui-ux-pro-max/scripts/search.py "e-commerce" --design-system --persist -p "Shop" --page "checkout"
```

### 2. 多项目并行

```bash
# 项目 A
python3 skills/ui-ux-pro-max/scripts/search.py "fintech crypto" --design-system --persist -p "CryptoApp"

# 项目 B
python3 skills/ui-ux-pro-max/scripts/search.py "healthcare telemedicine" --design-system --persist -p "HealthApp"
```

### 3. 迭代优化

```bash
# 第一次搜索
python3 skills/ui-ux-pro-max/scripts/search.py "SaaS" --design-system -p "MyApp"

# 根据结果调整关键词
python3 skills/ui-ux-pro-max/scripts/search.py "SaaS analytics dashboard dark mode" --design-system -p "MyApp"

# 持久化最终版本
python3 skills/ui-ux-pro-max/scripts/search.py "SaaS analytics dashboard dark mode professional" --design-system --persist -p "MyApp"
```

## 常见问题

### Q: 如何选择合适的关键词？
**A:** 关键词越具体，结果越精准：
- ❌ "app" → 太宽泛
- ✅ "healthcare SaaS dashboard analytics" → 精准

### Q: 设计系统生成后如何使用？
**A:** 
1. 查看 `design-system/项目名/MASTER.md` 获取全局规则
2. 为特定页面创建覆盖文件（如 `pages/dashboard.md`）
3. 页面文件会自动覆盖 Master 文件的规则

### Q: 如何处理多语言项目？
**A:** 系统支持多语言关键词，但建议使用英文关键词以获得最佳结果。

### Q: 如何更新设计系统？
**A:** 重新运行命令即可覆盖现有文件。建议使用版本控制系统跟踪变更。

## 性能优化建议

1. **缓存机制** - 系统会自动缓存 CSV 数据，避免重复加载
2. **并行搜索** - 多领域搜索并行执行，提升速度
3. **增量更新** - 只更新变更的文件，避免全量重写

## 更新日志

### v2.0.0 (2025-01-XX)
- ✨ 新增智能页面覆盖功能
- ✨ 新增 13 种技术栈支持
- ✨ 新增 Master + Overrides 持久化模式
- 🚀 优化搜索性能（并行搜索）
- 🐛 修复 BM25 算法在短查询时的精度问题
- 📝 重构文档，提升可读性

### v1.0.0 (2024-XX-XX)
- 🎉 初始版本发布

## 贡献指南

欢迎贡献新的设计风格、配色方案或技术栈指南！

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 许可证

MIT License - 详见 LICENSE 文件
