"""
定时器工具 - 重构版
提供定时任务功能

新架构流程：
1. 程序启动，后台监控线程持续检查任务是否到时间
2. 任务到达触发时间时，将任务放入执行队列
3. 任务执行器从队列取出任务，调用 Bot 进行交互式执行
4. Bot 在前台与用户交互，获取任务执行所需信息
5. Bot 在后台执行任务

支持三种定时模式：
1. 一次性延迟：多少秒后执行
2. 周期性定时：每隔多少秒执行
3. 每日定时：每日多少点执行
"""

import sys
import os
import json
import asyncio
import threading
import queue
from typing import Dict, Any, Optional, Callable, List
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

TIMER_JSON_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".shitbot", "datas", "timer.json")

class TaskStatus(Enum):
    """任务状态枚举"""
    PENDING = "pending"         # 等待执行
    RUNNING = "running"         # 正在执行
    COMPLETED = "completed"     # 已完成
    FAILED = "failed"           # 执行失败
    CANCELLED = "cancelled"     # 已取消


class TaskType(Enum):
    """任务类型枚举"""
    ONCE = "once"               # 一次性任务
    INTERVAL = "interval"       # 周期性任务
    DAILY = "daily"             # 每日定时任务


@dataclass
class TimerTask:
    """
    定时任务数据类
    
    Attributes:
        id: 任务唯一标识符
        description: 任务描述/要执行的内容
        interval: 周期时间间隔（秒），用于周期性任务
        interval_count: 周期触发次数，用于周期性任务 (-1表示无限次)
        target_time: 目标触发时间，用于一次性任务
        daily_time: 每日定时时间 (hour, minute)
        is_active: 任务是否处于活跃状态
        task_type: 任务类型
        status: 任务当前状态
        created_at: 任务创建时间
        last_triggered: 上次触发时间
        next_trigger: 下次触发时间
        execution_count: 已执行次数
        error_message: 错误信息（如果执行失败）
    """
    id: str
    description: str
    interval: Optional[int] = None
    interval_count: Optional[int] = None
    target_time: Optional[datetime] = None
    daily_time: Optional[tuple] = None
    is_active: bool = True
    task_type: str = "once"
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.now)
    last_triggered: Optional[datetime] = None
    next_trigger: Optional[datetime] = None
    execution_count: int = 0
    error_message: Optional[str] = None

    def to_dict(self) -> dict:
        """转换为字典（用于序列化）"""
        return {
            "id": self.id,
            "description": self.description,
            "interval": self.interval,
            "interval_count": self.interval_count,
            "target_time": self.target_time.strftime("%Y-%m-%d %H:%M:%S") if self.target_time else None,
            "daily_time": f"{self.daily_time[0]:02d}:{self.daily_time[1]:02d}" if self.daily_time else None,
            "is_active": self.is_active,
            "task_type": self.task_type,
            "status": self.status,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "last_triggered": self.last_triggered.strftime("%Y-%m-%d %H:%M:%S") if self.last_triggered else None,
            "next_trigger": self.next_trigger.strftime("%Y-%m-%d %H:%M:%S") if self.next_trigger else None,
            "execution_count": self.execution_count,
            "error_message": self.error_message
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "TimerTask":
        """从字典创建任务对象"""
        task_data = data.copy()
        
        # 转换时间字符串为 datetime 对象
        if task_data.get("target_time"):
            task_data["target_time"] = datetime.strptime(task_data["target_time"], "%Y-%m-%d %H:%M:%S")
        if task_data.get("next_trigger"):
            task_data["next_trigger"] = datetime.strptime(task_data["next_trigger"], "%Y-%m-%d %H:%M:%S")
        if task_data.get("last_triggered"):
            task_data["last_triggered"] = datetime.strptime(task_data["last_triggered"], "%Y-%m-%d %H:%M:%S")
        if task_data.get("created_at"):
            task_data["created_at"] = datetime.strptime(task_data["created_at"], "%Y-%m-%d %H:%M:%S")
        
        # 转换 daily_time 字符串为 tuple
        if task_data.get("daily_time"):
            hour, minute = map(int, task_data["daily_time"].split(":"))
            task_data["daily_time"] = (hour, minute)
        
        return cls(**task_data)


class TaskExecutor:
    """
    任务执行器
    
    负责从队列中获取待执行任务，并调用 Bot 进行交互式执行。
    使用独立线程运行，避免阻塞定时器监控线程。
    """
    
    def __init__(self, timer_instance=None):
        self._task_queue: queue.Queue[TimerTask] = queue.Queue()
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._bot = None
        self._callback: Optional[Callable[[TimerTask, str], None]] = None
        self._timer_instance = timer_instance
    
    def set_bot(self, bot):
        """设置 Bot 实例"""
        self._bot = bot
    
    def set_callback(self, callback: Callable[[TimerTask, str], None]):
        """设置任务执行完成后的回调函数"""
        self._callback = callback
    
    def start(self):
        """启动执行器线程"""
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
    
    def stop(self):
        """停止执行器线程"""
        self._running = False
        if self._thread:
            self._thread.join(timeout=2)
    
    def submit_task(self, task: TimerTask):
        """提交任务到执行队列"""
        self._task_queue.put(task)
    
    def _run_loop(self):
        """执行器主循环"""
        while self._running:
            try:
                # 从队列获取任务（阻塞等待，超时1秒）
                task = self._task_queue.get(timeout=1)
                self._execute_task(task)
            except queue.Empty:
                continue
            except Exception as e:
                print(f"[任务执行器] 执行循环出错: {e}")
    
    def _execute_task(self, task: TimerTask):
        """
        执行单个任务
        
        流程：
        1. 更新任务状态为运行中
        2. 调用 Bot 进行交互式执行
        3. 更新任务状态和结果
        4. 调用回调函数通知执行完成
        """
        task.status = TaskStatus.RUNNING.value
        task.last_triggered = datetime.now()
        task.execution_count += 1
        
        try:
            # 确保 Bot 已初始化
            if self._bot is None and self._timer_instance:
                self._timer_instance._init_bot()
            
            if self._bot is None:
                raise Exception("Bot 未初始化")
            
            # 构建任务执行提示
            execution_prompt = self._build_execution_prompt(task)
            
            # 使用 asyncio 运行异步 chat 方法
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            # 执行 Bot 交互
            result = loop.run_until_complete(
                self._bot.chat(execution_prompt, ui=None)
            )
            
            task.status = TaskStatus.COMPLETED.value
            task.error_message = None
            
        except Exception as e:
            task.status = TaskStatus.FAILED.value
            task.error_message = str(e)
        
        # 调用回调函数
        if self._callback:
            try:
                self._callback(task, task.error_message or "执行成功")
            except Exception as e:
                pass
    
    def _build_execution_prompt(self, task: TimerTask) -> str:
        """构建任务执行提示"""
        prompt = f"""【定时任务触发】

任务ID: {task.id}
任务类型: {task.task_type}
任务描述: {task.description}
触发时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
执行次数: {task.execution_count}

请根据任务描述执行相应操作。如果需要与用户交互获取更多信息，请写在ERROR.md文件里面。
如果可以直接执行，请立即开始执行并报告结果。

任务内容: {task.description}
"""
        return prompt


class Timer:
    """
    定时器管理器 - 重构版
    
    架构：
    - 后台监控线程：持续检查任务是否到达触发时间
    - 任务执行器：独立线程，负责调用 Bot 执行任务
    - 任务队列：待执行任务的缓冲队列
    
    流程：
    1. 监控线程发现任务到期 -> 放入执行队列
    2. 执行器从队列取出任务 -> 调用 Bot 交互执行
    3. Bot 与用户交互（如需）-> 后台执行任务
    """
    
    def __init__(self):
        """
        初始化定时器
        """
        self.tasks: Dict[str, TimerTask] = {}
        self._running = False
        self._monitor_thread: Optional[threading.Thread] = None
        self._task_counter = 0
        self._executor = TaskExecutor(timer_instance=self)
        
        # 延迟初始化 Bot（避免循环依赖）
        self._bot_initialized = False
        
        # 加载已保存的任务
        self._load_tasks()
    
    def _init_bot(self):
        """初始化 Bot 实例（延迟初始化）"""
        if self._bot_initialized:
            return
        
        try:
            from src.agent.bot import Bot
            bot = Bot(if_user_or_timer=False)
            bot.init_prompt()
            self._executor.set_bot(bot)
            self._bot_initialized = True
        except Exception as e:
            print(f"[定时器] Bot 初始化失败: {e}")
    
    def _load_tasks(self):
        """从文件加载任务"""
        try:
            with open(TIMER_JSON_PATH, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return
                
                data = json.loads(content)
                self._task_counter = data.get("counter", 0)
                now = datetime.now()
                
                for item in data.get("tasks", []):
                    try:
                        task = TimerTask.from_dict(item)
                        
                        if task.is_active and task.status == TaskStatus.RUNNING.value:
                            task.status = TaskStatus.PENDING.value
                        
                        if task.is_active:
                            if task.task_type == TaskType.DAILY.value:
                                if task.next_trigger and task.next_trigger <= now:
                                    hour, minute = task.daily_time
                                    next_trigger = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
                                    if next_trigger <= now:
                                        next_trigger += timedelta(days=1)
                                    task.next_trigger = next_trigger
                            
                            elif task.task_type == TaskType.ONCE.value:
                                if task.target_time and task.target_time <= now:
                                    task.is_active = False
                                    task.status = TaskStatus.CANCELLED.value
                            
                            elif task.task_type == TaskType.INTERVAL.value:
                                if task.next_trigger and task.next_trigger <= now:
                                    intervals_passed = int((now - task.next_trigger).total_seconds() / task.interval) + 1
                                    task.next_trigger = task.next_trigger + timedelta(seconds=intervals_passed * task.interval)
                                    if task.interval_count is not None and task.interval_count > 0:
                                        task.interval_count = max(0, task.interval_count - intervals_passed)
                                        if task.interval_count == 0:
                                            task.is_active = False
                        
                        self.tasks[task.id] = task
                    except Exception as e:
                        pass
                
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        except Exception as e:
            print(f"[定时器] 加载任务文件失败: {e}")
    
    def start(self):
        """
        启动定时器
        
        启动监控线程和执行器线程
        """
        if self._running:
            return
        
        self._running = True
        
        # 启动执行器
        self._executor.start()
        
        # 启动监控线程
        self._monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._monitor_thread.start()
    
    def stop(self):
        """
        停止定时器
        
        停止监控线程和执行器线程，并保存任务
        """
        self._running = False
        
        # 停止执行器
        self._executor.stop()
        
        # 等待监控线程结束
        if self._monitor_thread:
            self._monitor_thread.join(timeout=2)
        
        # 保存任务
        self._save_tasks()

    
    def _monitor_loop(self):
        """
        监控循环（后台线程）
        
        持续检查所有任务，将到期的任务提交给执行器
        """
        while self._running:
            try:
                now = datetime.now()
                
                for task_id, task in list(self.tasks.items()):
                    if not task.is_active:
                        continue
                    
                    if task.status == TaskStatus.RUNNING.value:
                        continue
                    
                    should_trigger = False
                    
                    if task.task_type == TaskType.ONCE.value:
                        # 一次性任务
                        if task.target_time and now >= task.target_time:
                            should_trigger = True
                            task.is_active = False  # 执行后标记为不活跃
                    
                    elif task.task_type == TaskType.INTERVAL.value:
                        # 周期性任务
                        if task.next_trigger and now >= task.next_trigger:
                            should_trigger = True
                            # 更新下次触发时间
                            task.next_trigger = now + timedelta(seconds=task.interval)
                            # 更新执行次数
                            if task.interval_count is not None and task.interval_count > 0:
                                task.interval_count -= 1
                                if task.interval_count == 0:
                                    task.is_active = False
                    
                    elif task.task_type == TaskType.DAILY.value:
                        # 每日定时任务
                        if task.next_trigger and now >= task.next_trigger:
                            should_trigger = True
                            # 计算明天的触发时间
                            hour, minute = task.daily_time
                            tomorrow = now + timedelta(days=1)
                            task.next_trigger = tomorrow.replace(
                                hour=hour, minute=minute, second=0, microsecond=0
                            )
                    
                    if should_trigger:
                        self._executor.submit_task(task)
                
                # 每0.5秒检查一次
                import time
                time.sleep(0.5)
                
            except Exception as e:
                print(f"[定时器] 监控循环出错: {e}")
                import time
                time.sleep(1)
    
    def _on_task_completed(self, task: TimerTask, result: str):
        """
        任务执行完成回调
        
        用于更新任务状态、保存到文件等
        """
        # 保存任务状态
        self._save_tasks()
    
    def _save_tasks(self):
        """保存任务到文件"""
        try:
            now = datetime.now()
            tasks_to_save = []
            
            for task in self.tasks.values():
                if not task.is_active and task.task_type == TaskType.ONCE.value:
                    continue
                
                tasks_to_save.append(task.to_dict())
            
            data = {
                "tasks": tasks_to_save,
                "counter": self._task_counter
            }
            
            os.makedirs(os.path.dirname(TIMER_JSON_PATH), exist_ok=True)
            
            with open(TIMER_JSON_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
                
        except Exception as e:
            print(f"[定时器] 保存任务失败: {e}")
    
    def _generate_task_id(self, prefix: str) -> str:
        """生成唯一任务ID"""
        self._task_counter += 1
        return f"{prefix}_{self._task_counter}"
    
    def once_after(
        self,
        description: str,
        delay_seconds: int,
        task_id: Optional[str] = None,
    ) -> str:
        """
        创建一次性延迟任务
        
        Args:
            description: 任务描述
            delay_seconds: 延迟秒数
            task_id: 任务ID，如果不提供则自动生成
            
        Returns:
            str: 任务ID
        """
        if not task_id:
            task_id = self._generate_task_id("once")
        
        target_time = datetime.now() + timedelta(seconds=delay_seconds)
        
        task = TimerTask(
            id=task_id,
            description=description,
            target_time=target_time,
            next_trigger=target_time,
            is_active=True,
            task_type=TaskType.ONCE.value
        )
        
        self.tasks[task_id] = task
        self._save_tasks()
        
        return task_id
    
    def interval_every(
        self,
        description: str,
        interval_seconds: int,
        interval_count: Optional[int] = None,
        task_id: Optional[str] = None,
    ) -> str:
        """
        创建周期性任务
        
        Args:
            description: 任务描述
            interval_seconds: 间隔秒数
            interval_count: 触发次数，None 或 -1 表示无限次
            task_id: 任务ID，如果不提供则自动生成
            
        Returns:
            str: 任务ID
        """
        if not task_id:
            task_id = self._generate_task_id("interval")
        
        next_trigger = datetime.now() + timedelta(seconds=interval_seconds)
        
        task = TimerTask(
            id=task_id,
            description=description,
            interval=interval_seconds,
            interval_count=interval_count,
            next_trigger=next_trigger,
            is_active=True,
            task_type=TaskType.INTERVAL.value
        )
        
        self.tasks[task_id] = task
        self._save_tasks()
        
        return task_id
    
    def daily_at(
        self,
        description: str,
        hour: int,
        minute: int,
        task_id: Optional[str] = None
    ) -> str:
        """
        创建每日定时任务
        
        Args:
            description: 任务描述
            hour: 小时 (0-23)
            minute: 分钟 (0-59)
            task_id: 任务ID，如果不提供则自动生成
            
        Returns:
            str: 任务ID
            
        Raises:
            ValueError: 当时间参数无效时
        """
        if not 0 <= hour <= 23:
            raise ValueError("小时必须在 0-23 之间")
        if not 0 <= minute <= 59:
            raise ValueError("分钟必须在 0-59 之间")
        
        if not task_id:
            task_id = self._generate_task_id("daily")
        
        now = datetime.now()
        next_trigger = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        if next_trigger <= now:
            next_trigger += timedelta(days=1)
        
        task = TimerTask(
            id=task_id,
            description=description,
            daily_time=(hour, minute),
            next_trigger=next_trigger,
            is_active=True,
            task_type=TaskType.DAILY.value
        )
        
        self.tasks[task_id] = task
        self._save_tasks()
        
        return task_id
    
    def cancel(self, task_id: str) -> bool:
        """
        取消任务
        
        Args:
            task_id: 任务ID
            
        Returns:
            bool: 是否成功取消
        """
        if task_id in self.tasks:
            task = self.tasks[task_id]
            task.is_active = False
            task.status = TaskStatus.CANCELLED.value
            self._save_tasks()
            return True
        return False
    
    def pause(self, task_id: str) -> bool:
        """
        暂停任务
        
        Args:
            task_id: 任务ID
            
        Returns:
            bool: 是否成功暂停
        """
        if task_id in self.tasks:
            self.tasks[task_id].is_active = False
            self._save_tasks()
            return True
        return False
    
    def resume(self, task_id: str) -> bool:
        """
        恢复任务
        
        Args:
            task_id: 任务ID
            
        Returns:
            bool: 是否成功恢复
        """
        if task_id not in self.tasks:
            return False
        
        task = self.tasks[task_id]
        task.is_active = True
        
        # 重新计算下次触发时间
        now = datetime.now()
        
        if task.task_type == TaskType.ONCE.value:
            # 一次性任务：如果已过期，设置为5秒后执行
            if task.target_time and now >= task.target_time:
                task.target_time = now + timedelta(seconds=5)
                task.next_trigger = task.target_time
        
        elif task.task_type == TaskType.INTERVAL.value:
            # 周期性任务
            task.next_trigger = now + timedelta(seconds=task.interval)
        
        elif task.task_type == TaskType.DAILY.value:
            # 每日任务
            hour, minute = task.daily_time
            next_trigger = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if next_trigger <= now:
                next_trigger += timedelta(days=1)
            task.next_trigger = next_trigger
        
        self._save_tasks()
        
        return True
    
    def get_task(self, task_id: str) -> Optional[TimerTask]:
        """
        获取单个任务信息
        
        Args:
            task_id: 任务ID
            
        Returns:
            TimerTask: 任务对象，不存在则返回 None
        """
        return self.tasks.get(task_id)
    
    def get_tasks(self, active_only: bool = False) -> List[dict]:
        """
        获取所有任务信息
        
        Args:
            active_only: 是否只返回活跃任务
            
        Returns:
            List[dict]: 任务信息列表
        """
        tasks_info = []
        now = datetime.now()
        
        for task in self.tasks.values():
            if active_only and not task.is_active:
                continue
            
            info = task.to_dict()
            
            # 添加计算字段
            if task.next_trigger:
                remaining = (task.next_trigger - now).total_seconds()
                info["remaining_seconds"] = int(max(0, remaining))
            
            tasks_info.append(info)
        
        # 按下次触发时间排序
        tasks_info.sort(key=lambda x: x.get("next_trigger") or "")
        return tasks_info
    
    def clear_all(self):
        """清除所有任务"""
        self.tasks.clear()
        self._save_tasks()
    
    def get_statistics(self) -> dict:
        """
        获取定时器统计信息
        
        Returns:
            dict: 统计信息
        """
        total = len(self.tasks)
        active = sum(1 for t in self.tasks.values() if t.is_active)
        pending = sum(1 for t in self.tasks.values() if t.status == TaskStatus.PENDING.value)
        running = sum(1 for t in self.tasks.values() if t.status == TaskStatus.RUNNING.value)
        completed = sum(1 for t in self.tasks.values() if t.status == TaskStatus.COMPLETED.value)
        failed = sum(1 for t in self.tasks.values() if t.status == TaskStatus.FAILED.value)
        
        return {
            "total_tasks": total,
            "active_tasks": active,
            "pending_tasks": pending,
            "running_tasks": running,
            "completed_tasks": completed,
            "failed_tasks": failed
        }


# 全局定时器实例（单例模式）
_global_timer: Optional[Timer] = None


def get_timer() -> Timer:
    """
    获取全局定时器实例
    
    Returns:
        Timer: 全局定时器实例
    """
    global _global_timer
    if _global_timer is None:
        _global_timer = Timer()
        _global_timer.start()
    return _global_timer


def stop_timer():
    """停止全局定时器"""
    global _global_timer
    if _global_timer is not None:
        _global_timer.stop()
        _global_timer = None


if __name__ == "__main__":
    # 测试代码
    print("=" * 60)
    print("定时器测试")
    print("=" * 60)
    
    timer = get_timer()
    
    # 显示当前任务
    print("\n当前所有任务:")
    for task in timer.get_tasks():
        print(f"   {task}")
    
    # 创建测试任务
    print("\n创建测试任务...")
    
    # 一次性任务（5秒后）
    task1 = timer.once_after("测试一次性任务", 5)
    print(f"   一次性任务: {task1}")
    
    # 周期性任务（每10秒，执行3次）
    task2 = timer.interval_every("测试周期性任务", 10, 3)
    print(f"   周期性任务: {task2}")
    
    # 每日任务
    task3 = timer.daily_at("测试每日任务", datetime.now().hour, datetime.now().minute + 1)
    print(f"   每日任务: {task3}")
    
    # 显示统计信息
    print("\n定时器统计:")
    print(f"   {timer.get_statistics()}")
    
    # 保持运行
    print("\n按 Ctrl+C 停止...")
    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n停止定时器...")
        stop_timer()
