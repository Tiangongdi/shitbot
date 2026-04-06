import asyncio
import threading
from datetime import datetime
from src.agent.ai import Message

class SubAgentManager:
    """SubAgent任务管理器"""
    _task_counter = 0  # 类级别的任务计数器
    _instance = None   # 单例实例
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.tasks = {}
        return cls._instance
    
    @classmethod
    def _generate_task_id(cls) -> str:
        """生成唯一的任务ID
        
        格式：TASK_YYYYMMDD_HHMMSS_XXX
        例如：TASK_20240406_123456_001
        """
        cls._task_counter += 1
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"TASK_{timestamp}_{cls._task_counter:03d}"
    
    def run_background_task(self, role: str, task: str, main_agent_memory):
        """在后台执行任务
        
        Args:
            role: 子代理角色
            task: 任务内容
            main_agent_memory: 主智能体的记忆对象
        
        Returns:
            str: 任务开始的提示信息
        """
        # 生成唯一任务ID
        task_id = self._generate_task_id()
        
        # 立即返回提示信息
        start_message = f"[{task_id}] Subagent正在后台执行任务: {task}"
        
        # 创建后台线程执行任务
        def background_task():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                # 动态导入SubAgent，避免循环导入
                from src.agent.subagent import SubAgent
                # 为每个任务创建独立的SubAgent实例，确保记忆隔离
                task_agent = SubAgent()
                # 执行任务
                result = loop.run_until_complete(task_agent.execute_task(role, task))
                # 任务完成后，将结果添加到主智能体记忆
                if main_agent_memory:
                    completion_message = Message(
                        role="system",
                        content=f"[{task_id}] 任务完成报告: {result}"
                    )
                    main_agent_memory.add_message(completion_message)
            finally:
                loop.close()
                # 任务完成后，从任务字典中删除
                if task_id in self.tasks:
                    del self.tasks[task_id]
        
        # 启动后台线程
        thread = threading.Thread(target=background_task, daemon=True)
        thread.start()
        
        # 保存任务信息
        self.tasks[task_id] = {
            'thread': thread,
            'task': task
        }
        
        return start_message
    
    def get_task_count(self) -> int:
        """获取当前正在执行的任务数量"""
        return len(self.tasks)
    
    def get_tasks(self) -> dict:
        """获取所有任务信息"""
        return self.tasks.copy()


# 全局单例
_subagent_manager = None

def get_subagent_manager() -> SubAgentManager:
    """获取SubAgent管理器单例"""
    global _subagent_manager
    if _subagent_manager is None:
        _subagent_manager = SubAgentManager()
    return _subagent_manager
