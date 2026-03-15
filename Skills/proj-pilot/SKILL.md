---
name: proj-pilot
description: 项目管理助手。这是一个帮助用户扩展，验证项目灵感的工作流，包括项目规划、技术选型、项目市场调研等，当用户需要评估项目灵感的可行性时使用此技能。     
---
# proj-pilot工作流
## 1. 开发者个人分析
- 调用user-profile-generator技能，生成开发者画像，方便后续项目规划和技术选型。地址：.\Skills\user-profile-generator\SKILL.md
- 建议生成的报告保存到项目根目录下的user-profile.md文件中，方便后续查看，以及在这个工作流开始之前可以进行查看，如果有旧的报告，就可以直接使用，跳过调用user-profile-generator技能。
## 2. 项目灵感分叉
- 调用idea-expander技能，丰富项目灵感。地址：.\Skills\idea-expander\SKILL.md
## 3. 项目市场调研
- 调用market-research技能，调研项目市场需求。地址：.\Skills\market-research\SKILL.md
## 4. 技术选型报告
- 调用tech-selection-report技能，生成技术选型报告。地址：.\Skills\tech-selection-report\SKILL.md
## 5. 项目规划
- 生成一个MD市场报告文件，并且问对方保存到哪里。

