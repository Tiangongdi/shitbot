from src.agent.ai import Message

class SubAgent:
    def __init__(self, shared_memory=None):
        # 动态导入Bot类，避免循环导入
        from src.agent.bot import Bot
        # 强制使用独立记忆，忽略传入的shared_memory参数
        self.bot = Bot(None, if_user_or_subagent=True)
        # 初始化与普通智能体相同的提示词
        self.bot.init_prompt()
    
    def task(self, role: str, q: str):
        """执行子代理任务"""
        msg = Message(
            role="system",
            content=role    
        )   
        self.bot._add_message(msg)
        return self.bot.chat(q)
    
    async def execute_task(self, role: str, task: str):
        """执行任务
        
        Args:
            role: 子代理角色
            task: 任务内容
        
        Returns:
            str: 任务执行结果
        """
        # 添加任务特定的角色提示
        msg = Message(
            role="system",
            content=role
        )
        self.bot._add_message(msg)
        
        # 执行任务
        result = await self.bot.chat(task)
        return result
