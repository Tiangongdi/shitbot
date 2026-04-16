import asyncio
import threading
import json
import os
import queue
from datetime import datetime
from typing import Dict, Optional, List
from src.agent.ai import Message
from src.agent.subagent import SubAgent


class SubAgentManager:
    """SubAgent任务管理器 - 管理多个子智能体的并行任务执行"""
    _task_counter: int = 0  # 类级别的任务计数器
    _counter_lock = threading.Lock()  # 保护计数器的原子操作
    _instance: Optional['SubAgentManager'] = None  # 单例实例

    def __init__(self):
        """初始化管理器"""
        # 互斥锁保护所有共享数据的并发访问
        self._lock = threading.Lock()

        # 常量：配置文件路径
        self._subagent_file = os.path.join(
            os.path.dirname(__file__), '..', '..',
            '.shitbot', 'datas', 'subagent.json'
        )

        # 静态配置（持久化到磁盘）
        self._subagent_configs: Dict[str, Dict[str, str]] = {}  # role_id -> {role, description}

        # 运行时状态（内存中，不持久化）
        self._subagent_states: Dict[str, str] = {}  # role_id -> 'free'|'working'
        self._agents: Dict[str, Optional[SubAgent]] = {}  # role_id -> SubAgent实例 (懒加载，None表示未创建)
        self._tasks: Dict[str, Dict] = {}  # task_id -> {thread, task, role_id}
        self._completed_queue: queue.Queue = queue.Queue()  # 已完成任务队列

        # 加载配置（只加载配置，不立即创建实例，避免循环依赖递归）
        self._load_subagents()

    def _load_subagents(self) -> None:
        """从文件加载子智能体配置（仅静态配置）"""
        try:
            if os.path.exists(self._subagent_file) and os.path.getsize(self._subagent_file) > 0:
                with open(self._subagent_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    with self._lock:
                        self._subagent_configs = loaded
                        # 初始化所有子智能体状态为free
                        for role_id in loaded:
                            self._subagent_states[role_id] = 'free'
        except Exception as e:
            print(f"加载子智能体配置失败: {e}")
            with self._lock:
                self._subagent_configs = {}

    def _save_subagents(self) -> bool:
        """保存子智能体静态配置到文件（原子写入）"""
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(self._subagent_file), exist_ok=True)

            # 先写入临时文件，再原子替换，防止并发损坏
            temp_file = self._subagent_file + '.tmp'
            with self._lock:
                configs_copy = self._subagent_configs.copy()

            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(configs_copy, f, ensure_ascii=False, indent=2)

            # 原子替换（Windows 上 os.replace 也是原子的）
            os.replace(temp_file, self._subagent_file)
            return True
        except Exception as e:
            print(f"保存子智能体配置失败: {e}")
            return False

    def _get_or_create_agent(self, role_id: str) -> Optional[SubAgent]:
        """懒加载获取或创建子智能体实例（避免循环依赖递归）"""
        with self._lock:
            if role_id not in self._agents or self._agents[role_id] is None:
                # 懒加载创建实例
                info = self._subagent_configs.get(role_id)
                if info is None:
                    return None
                self._agents[role_id] = SubAgent(role=info["role"], role_id=role_id)
            return self._agents[role_id]

    def __new__(cls):
        """单例获取"""
        if cls._instance is None:
            with threading.Lock():
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def _generate_task_id(cls) -> str:
        """生成唯一的任务ID（线程安全原子操作）

        格式：TASK_YYYYMMDD_HHMMSS_XXX
        例如：TASK_20240406_123456_001
        """
        with cls._counter_lock:
            cls._task_counter += 1
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            return f"TASK_{timestamp}_{cls._task_counter:03d}"

    def create_subagent(self, role: str, description: str) -> str:
        """创建新的子智能体

        Args:
            role: 子智能体角色
            description: 子智能体描述

        Returns:
            str: 创建结果的字符串消息
        """
        role_id = self._generate_task_id()
        with self._lock:
            self._subagent_configs[role_id] = {
                "role": role,
                "description": description
            }
            self._subagent_states[role_id] = 'free'
            self._agents[role_id] = None  # 懒加载，使用时再创建

        self._save_subagents()
        return f"子智能体创建成功，ID: {role_id}，角色: {role}"

    def get_completed_task(self, block: bool = False, timeout: Optional[float] = None) -> Optional[Dict]:
        """从完成队列获取一个已完成的任务结果

        Args:
            block: 是否阻塞等待
            timeout: 超时时间（秒）

        Returns:
            任务信息字典，如果队列为空返回 None
        """
        try:
            return self._completed_queue.get(block=block, timeout=timeout)
        except queue.Empty:
            return None

    def has_completed_tasks(self) -> bool:
        """检查是否有已完成的任务待处理"""
        return not self._completed_queue.empty()

    def run_background_task(self, role_id: str, task: str, main_agent_memory, completion_callback: None = None) -> str:
        """在后台并行执行任务

        Args:
            role_id: 子代理角色ID
            task: 任务内容
            main_agent_memory: 主智能体的记忆对象
            completion_callback: 任务完成后的回调函数（保留兼容性，未使用）

        Returns:
            str: 任务启动提示信息
        """
        # 原子检查和新增：加锁防止TOCTOU问题
        with self._lock:
            # 限制同时运行最多 10 个任务
            if len(self._tasks) >= 10:
                return f"错误：同时运行的任务最多 10 个，当前已有 {len(self._tasks)} 个，请先等待部分完成后再添加新任务"

            # 检查子智能体配置存在
            if role_id not in self._subagent_configs:
                return f"错误：子智能体 {role_id} 不存在"

            # 检查子智能体是否空闲
            if self._subagent_states.get(role_id) != 'free':
                return f"错误：子智能体 {role_id} 当前正在执行任务，请等待完成"

            # 生成唯一任务ID
            task_id = self._generate_task_id()

            # 标记子智能体为工作中
            self._subagent_states[role_id] = 'working'

            # 创建后台线程执行任务，多个任务并行执行
            start_message = f"[{task_id}] 子智能体 {role_id} 已启动后台任务: {task}"

            thread = threading.Thread(
                target=self._background_task_wrapper,
                args=(task_id, role_id, task, main_agent_memory),
                daemon=True
            )

            # 保存任务信息
            self._tasks[task_id] = {
                'thread': thread,
                'task': task,
                'role_id': role_id
            }

        # 启动后台线程（在外层启动减少锁持有时间）
        thread.start()
        return start_message

    def _background_task_wrapper(self, task_id: str, role_id: str, task: str, main_agent_memory):
        """后台任务包装器 - 在独立线程执行，处理异常和完成通知

        每个任务仍然创建独立事件循环，保持当前行为不变
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result: Optional[str] = None

        try:
            # 懒加载获取子智能体实例
            task_agent = self._get_or_create_agent(role_id)

            if task_agent is None:
                result = f"错误：子智能体 {role_id} 不存在"
                return

            # 执行任务
            result = loop.run_until_complete(task_agent.execute_task(task))

            # 任务完成后，将结果添加到主智能体记忆
            if main_agent_memory:
                completion_message = Message(
                    role="system",
                    content=f"[{task_id}] 子智能体 {role_id} 任务完成报告: {result}"
                )
                main_agent_memory.add_message(completion_message)

            # 将任务放入完成队列
            self._completed_queue.put({
                'task_id': task_id,
                'role_id': role_id,
                'result': result,
                'timestamp': datetime.now()
            })

        except Exception as e:
            result = f"任务执行异常: {str(e)}"
            print(f"子智能体任务异常 [{task_id}] {role_id}: {e}")
        finally:
            # 标记子智能体为空闲（运行时状态，不持久化到磁盘）
            with self._lock:
                if role_id in self._subagent_states:
                    self._subagent_states[role_id] = 'free'
                # 从任务列表删除
                if task_id in self._tasks:
                    del self._tasks[task_id]
            loop.close()

    def wait_all_tasks(self) -> str:
        """等待所有后台子智能体任务完成

        Returns:
            str: 等待完成后的总结报告
        """
        # 获取当前任务列表的拷贝，避免遍历时修改
        with self._lock:
            if not self._tasks:
                return "当前没有正在运行的子智能体任务"
            task_list = list(self._tasks.items())

        task_count = len(task_list)
        # 等待所有线程完成
        for task_id, task_info in task_list:
            thread = task_info['thread']
            thread.join()

        # 收集所有已完成的结果信息（只收集状态信息）
        completed_results: List[Dict] = []
        # _completed_queue 本身线程安全，不需要加锁
        while not self._completed_queue.empty():
            completed = self._completed_queue.get()
            completed_results.append(completed)
            # 确保标记为空闲（保险，_background_task_wrapper 已经处理过）
            with self._lock:
                if completed['role_id'] in self._subagent_states:
                    self._subagent_states[completed['role_id']] = 'free'

        # 生成总结报告
        if not completed_results:
            return f"已等待 {task_count} 个任务完成，但没有收集到结果"

        summary = f"所有 {len(completed_results)} 个子智能体任务已完成:\n"
        for completed in completed_results:
            summary += f"- [{completed['task_id']}] 子智能体 {completed['role_id']}: 已完成\n"

        return summary

    def get_task_count(self) -> int:
        """获取当前正在执行的任务数量"""
        with self._lock:
            return len(self._tasks)

    def get_tasks(self) -> Dict:
        """获取所有任务信息（返回拷贝）"""
        with self._lock:
            return self._tasks.copy()

    def get_subagent(self) -> str:
        """获取所有子智能体信息"""
        with self._lock:
            configs_copy = self._subagent_configs.copy()
            states_copy = self._subagent_states.copy()

        text = "当前子智能体列表:\n"
        for role_id, info in configs_copy.items():
            state = states_copy.get(role_id, 'unknown')
            if state == 'working':
                text += f"{role_id}: {info['description']} ({info['role']}) [运行中]\n"
            else:
                text += f"{role_id}: {info['description']} ({info['role']}) [空闲]\n"
        return text


# 全局单例获取
_subagent_manager: Optional[SubAgentManager] = None


def get_subagent_manager() -> SubAgentManager:
    """获取SubAgent管理器单例（线程安全初始化）"""
    global _subagent_manager
    if _subagent_manager is None:
        with threading.Lock():
            if _subagent_manager is None:
                _subagent_manager = SubAgentManager()
    return _subagent_manager
