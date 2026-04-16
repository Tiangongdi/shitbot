from src.agent.ai import Message

class SubAgent:
    def __init__(self, shared_memory=None ,role="你没有而外Role Agent要求 请你根据任务内容执行任务", role_id=""):       
        # 动态导入Bot类，避免循环导入
        from src.agent.bot import Bot
        # 强制使用独立记忆，忽略传入的shared_memory参数
        self.role_id = role_id
        self.bot = Bot(None, if_user_or_subagent=False)
        self.role = role    
        # 初始化与普通智能体相同的提示词
        self.bot.init_prompt()
        self.set_role()
    def set_role(self):
        """设置子代理角色"""
        msg = Message(
            role="system",
            content=f"请阅读{self.role},你的智能体ID为:{self.role_id}"
        )   
        self.bot._add_message(msg)
    
    async def execute_task(self,  task: str):
        """执行任务
        
        Args:
            role: 子代理角色
            task: 任务内容
        
        Returns:
            str: 任务执行结果
        """
        # 添加任务特定的角色提示
        # 执行任务
        result = await self.bot.chat(task)
        return result
