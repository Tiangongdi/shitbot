# SubAgent System - Introduction & Usage Guide

## What is SubAgent?

The **SubAgent system** is a parallel task processing architecture that allows the main agent to delegate tasks to independently running child agents. Each SubAgent has its own isolated memory space, runs asynchronously in the background, and automatically reports results back to the main agent upon completion.

## Key Benefits

- **Memory Isolation**: Each SubAgent gets a fresh, independent context that doesn't pollute the main agent's conversation history
- **Non-blocking Execution**: Tasks run in background daemon threads, so the main agent can continue interacting with the user immediately
- **Automatic Result Reporting**: When finished, results are automatically written back to the main agent's shared memory
- **Role Specialization**: You can inject specialized role prompts into SubAgents for domain-specific tasks
- **Parallel Processing**: Multiple SubAgents can work on different tasks simultaneously
- **SubAgent Management**: Create and manage multiple SubAgents with different roles for different tasks

## How It Works

### 1. **Checking Existing SubAgents**
Before creating a new SubAgent, it's recommended to check if there are existing SubAgents with the required role:
- Call `get_subagent()` to list all available SubAgents
- Review the list to see if there's already a SubAgent with the role you need
- Reuse existing SubAgents whenever possible to avoid unnecessary duplication

### 2. **Creating a SubAgent**
If no suitable SubAgent exists, call `create_subagent(role, description)`:
- A unique role ID is generated for the new SubAgent
- The SubAgent is initialized with the specified role and description
- The SubAgent is stored in the SubAgentManager for future use

### 3. **Assigning Tasks to SubAgents**
When you call `subagent_task(task, role_id)`:
- The SubAgentManager generates a unique task ID (format: `TASK_YYYYMMDD_HHMMSS_XXX`)
- A new daemon thread is created
- The specified SubAgent is retrieved from the manager
- The task executes asynchronously in the background

### 4. **Upon Completion**:
- The result is wrapped in a completion message
- The message is added to the main agent's shared memory
- The SubAgent returns to idle state, ready for new tasks

## Use Cases

✅ **Use SubAgent for:**

1. **Long-running tasks** - Web research, document generation, code analysis that takes time
   - *Example*: "Research the latest LLM models and create a comparison table"

2. **Parallel task execution** - Multiple independent tasks that can run concurrently
   - *Example*: One SubAgent researches market data, another drafts the introduction, third creates code examples

3. **Domain-specific expertise** - Assign specialized roles for specialized work
   - *Example*: Use the `SpringBootCoder` role for backend API design, `MarketAnalyst` for competitive analysis

4. **Task decomposition** - Break a complex project into parallel sub-tasks
   - *Example*: Main agent plans the project, delegates components to different SubAgents

❌ **Don't use SubAgent when:**

1. You need an immediate answer to a simple question
2. The task heavily depends on the current conversation context that the SubAgent can't access
3. The task is trivial and would complete faster with direct execution

## Important Constraints

- **No recursive calling**: SubAgents cannot see the `subagent_task` tool - this prevents infinite recursion
- **Daemon threads**: If the main program exits, all background SubAgents exit automatically
- **Memory isolation**: SubAgent memory is discarded after task completion - only the final result is kept in main agent memory

## Available Tools

### 1. `create_subagent(role, description)`
- **Description**: Creates a new SubAgent with the specified role and description
- **Parameters**:
  - `role`: Reference to an existing role document (e.g., "MarketAnalyst")
  - `description`: Brief description of the SubAgent's purpose
- **Returns**: The role ID of the created SubAgent

### 2. `subagent_task(task, role_id)`
- **Description**: Assigns a task to the specified SubAgent
- **Parameters**:
  - `task`: Detailed task description
  - `role_id`: The role ID of the SubAgent to execute the task
- **Returns**: A message confirming the task has started

### 3. `get_subagent()`
- **Description**: Gets information about all available SubAgents
- **Parameters**: None
- **Returns**: List of SubAgents with their role IDs and descriptions

## Example Usage

### Step 1: Check Existing SubAgents

```
Tool: get_subagent
```

### Step 2: Create a SubAgent (if needed)

If no suitable SubAgent exists, create a new one:

```
Tool: create_subagent
Parameters:
{
  "role": "MarketAnalyst",
  "description": "Professional market analyst specializing in AI industry research"
}
```

### Step 3: Assign a Task to the SubAgent

```
Tool: subagent_task
Parameters:
{
  "task": "Analyze the competitive landscape of open-source AI agent projects on GitHub. Identify key players, market trends, and competitive advantages.",
  "role_id": "TASK_20240406_123456_001"  // Use the role ID from create_subagent or get_subagent
}
```

## Role Parameter Instructions

The `role` parameter in `create_subagent` is used to specify the role of the SubAgent. When using it, you need to ensure:

1. **Only reference existing role documents and skill documents**: The `role` parameter should be a reference to an existing role document, not a complete role description written directly in the parameter.

2. **Create necessary documents**: If there are no required role or skill documents, you should first create the corresponding documents, and then reference them in the `role` parameter.

3. **Facilitate subsequent calls**: By pre-creating and referencing standardized role and skill documents, you can ensure that SubAgents can consistently perform the same type of tasks in subsequent tasks.

## Best Practices

1. **Create and reuse SubAgents**: Create SubAgents with specific roles once and reuse them for multiple tasks
2. **Use descriptive role names**: Choose clear, descriptive names for SubAgents to easily identify their purpose
3. **Provide detailed task descriptions**: The more specific the task description, the better the SubAgent can perform
4. **Monitor task progress**: Since SubAgents run in the background, check the main agent's memory for task completion reports
5. **Use multiple SubAgents for parallel tasks**: Create different SubAgents for different types of tasks to maximize parallel processing

---

*The SubAgent system enables scalable, parallel task execution while keeping your main conversation responsive. Use it to get more work done concurrently without blocking user interaction.*
