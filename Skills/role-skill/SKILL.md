---
name: role-skill
description: "Create or update AgentRoles. Use when designing, structuring, or defining roles with specific behaviors, skills, and tool recommendations for AI agents."
---

# Role Creator Skill

This skill provides guidance for creating effective roles for AI agents.

## About Roles

Roles are modular, self-contained definitions that shape how an AI agent behaves, what tasks it focuses on, and what tools it should use. Think of them as "personas" or "job descriptions" that transform a general-purpose agent into a specialized one with specific expertise and responsibilities.

### What Roles Provide

1. **Behavioral guidance** - How the agent should approach tasks
2. **Task definitions** - What the agent is responsible for
3. **Skill requirements** - What capabilities the agent should have
4. **Tool recommendations** - Which tools are most useful for this role

## Role Structure

Every role consists of a single `ROLE.md` file:

```
RoleName/
└── ROLE.md
    ├── YAML frontmatter (required)
    │   ├── name: (required)
    │   └── description: (required)
    └── Markdown body (required)
        ├── 描述 (Description)
        ├── 任务 (Tasks)
        ├── 技能 (Skills)
        └── 建议使用工具 (Recommended Tools)
```

### ROLE.md Format

```markdown
---
name: RoleName
description: "A brief description of what this role does and when to use it."
---
# RoleName Role

## 描述
[Detailed description of the role's purpose and behavior]

## 任务
1. [Task 1]
2. [Task 2]
...

## 技能
1. [Skill 1]
2. [Skill 2]
...

## 建议使用工具
1. tool_name: [Description of usage]
...
```

## Role Creation Process

### Step 1: Understand the Role Requirements

Ask the user:
- What is the role's name?
- What is the main purpose of this role?
- What tasks should this role handle?
- What skills are required?
- What tools would be most useful?

### Step 2: Create the Role Directory

Create a directory under `.\ShitBot\Roles\` with the role name:

```
.\ShitBot\Roles\RoleName\
```

### Step 3: Write the Role.md File

Create the `ROLE.md` file with proper frontmatter and body content.

**Frontmatter Guidelines:**
- `name`: Use PascalCase (e.g., "Coder", "DataAnalyst", "ProjectManager")
- `description`: Be specific about what the role does and when to use it

**Body Guidelines:**
- Use Chinese section headers: 描述, 任务, 技能, 建议使用工具
- Be concise but comprehensive
- List specific, actionable tasks
- Include relevant tool recommendations

### Step 4: Validate the Role

Ensure the role:
- Has valid YAML frontmatter
- Contains all required sections
- Has a clear, actionable description
- Lists relevant tools available in the system

## Template Reference

See [role-template.md](references/role-template.md) for a complete template example.

## Best Practices

1. **Be specific** - Vague roles lead to vague behavior
2. **Focus on outcomes** - Describe what the role should achieve
3. **Match tools to tasks** - Recommend tools that directly support the role's tasks
4. **Keep it concise** - Roles should be easy to understand at a glance
5. **Use consistent formatting** - Follow the standard structure for all roles
