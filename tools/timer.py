"""
定时器工具
提供定时提醒功能
支持三种定时模式：
1. 一次性延迟：多少秒后打印
2. 周期性定时：每隔多少秒打印
3. 每日定时：每日多少点打印
"""

from re import S
import sys
import os
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import threading
from typing import Dict, Any, Optional, Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
from memory import SharedMemory, get_shared_memory


@dataclass
class TimerTask:
    """
    定时任务数据类
    
    Attributes:
        id: 任务唯一标识符
        message: 任务描述/要打印的消息
        interval: 周期时间间隔（秒），用于周期性任务
        interval_count: 周期触发次数，用于周期性任务
        target_time: 目标触发时间，用于一次性任务
        daily_time: 每日定时时间 (hour, minute)
        callback: 回调函数，如果不提供则打印消息
        is_active: 任务是否处于活跃状态
        task_type: 任务类型 ("once", "interval", "daily")
    """
    id: str
    message: str
    interval: Optional[int] = None
    interval_count: Optional[int] = None
    target_time: Optional[datetime] = None
    daily_time: Optional[tuple] = None
    is_active: bool = True
    task_type: str = "once"
    next_trigger: Optional[datetime] = None


class Timer:
    """
    定时器管理器
    
    使用后台线程持续检查任务，当任务到达触发时间时执行相应的操作。
    支持三种定时模式：
    1. 一次性延迟：多少秒后打印
    2. 周期性定时：每隔多少秒打印
    3. 每日定时：每日多少点打印
    """
    
    def __init__(self):
        """
        初始化定时器
        
        Attributes:
            tasks: 存储所有任务的字典，key为任务ID
            _running: 定时器是否正在运行
            _thread: 后台线程对象
            _task_counter: 任务计数器，用于生成唯一任务ID
        """
        self.tasks: Dict[str, TimerTask] = {}
        self._running = False
        self._thread = None
        self._task_counter = 0
        self.bot = None
        self.init_timer()
    def init_timer(self):
        """
        初始化定时器
        从文件加载所有任务
        """
        try:
            with open("timer.json", "r") as f:
                content = f.read().strip()
                if not content:
                    return
                data = json.loads(content)
                list = data["tasks"]
                self._task_counter = data["counter"]
                for item in list:
                    task_data = {}
                    for key in ["id", "message", "interval", "interval_count", "target_time", "daily_time", "is_active", "task_type", "next_trigger"]:
                        if key in item:
                            if key == "target_time" and isinstance(item[key], str):
                                task_data[key] = datetime.strptime(item[key], "%Y-%m-%d %H:%M:%S")
                            elif key == "next_trigger" and isinstance(item[key], str):
                                task_data[key] = datetime.strptime(item[key], "%Y-%m-%d %H:%M:%S")
                            elif key == "daily_time" and isinstance(item[key], str):
                                hour, minute = map(int, item[key].split(":"))
                                task_data[key] = (hour, minute)
                            else:
                                task_data[key] = item[key]
                    task = TimerTask(**task_data)
                    self.tasks[task.id] = task
        except (FileNotFoundError, json.JSONDecodeError):
            pass
    def start(self):
        """
        启动定时器
        
        创建一个后台线程来运行事件循环，如果定时器已经在运行则不执行任何操作。
        线程设置为守护线程，主程序退出时会自动结束。
        """
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
    
    def stop(self):
        """
        停止定时器
        
        设置运行标志为False，并等待线程结束。
        等待超时时间为2秒。
        """
        self._running = False
        self.save()
        if self._thread:
            self._thread.join(timeout=2)
    
    def _run_loop(self):
        """
        运行事件循环（后台线程的主函数）
        
        持续检查所有任务，判断是否到达触发时间。
        每0.5秒检查一次所有任务。
        """
        while self._running:
            now = datetime.now()
            
            for task_id, task in list(self.tasks.items()):
                if not task.is_active:
                    continue
                
                should_trigger = False
                
                if task.task_type == "once":
                    if task.target_time and now >= task.target_time:
                        should_trigger = True
                        task.is_active = False
                
                elif task.task_type == "interval":
                    if task.target_time and now >= task.target_time:
                        if task.interval_count is None or task.interval_count > 0 or task.interval_count == -1: # 未指定次数或次数未用完
                            should_trigger = True # 触发任务
                            task.target_time = now + timedelta(seconds=task.interval) # 更新下次触发时间
                            if task.interval_count is not None and task.interval_count > 0 and task.interval_count != -1: # 次数未用完
                                task.interval_count -= 1
                
                elif task.task_type == "daily":
                    if task.daily_time:
                        hour, minute = task.daily_time
                        target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
                        
                        if target <= now:
                            target += timedelta(days=1)
                        
                        if task.target_time is None or now >= task.target_time:
                            should_trigger = True
                            task.target_time = target
                
                if should_trigger:
                    self._execute_task(task)
            
            time.sleep(0.5)
    
    def _execute_task(self, task: TimerTask):
        """
        执行任务
        
        Args:
            task: 要执行的任务对象
            
        如果任务有回调函数则调用回调函数，否则打印任务消息。
        捕获并打印执行过程中的异常。
        """
        try:
            if task.message:
                if self.bot is None:
                    from bot import Bot
                    self.bot = Bot(shared_memory=get_shared_memory())
                    self.bot.init_prompt()
                self.bot.chat(task.message)
        except Exception as e:
            print(f"[定时器错误] 任务 {task.id} 执行失败: {e}")
    
    def once_after(
        self,
        message: str,
        delay_seconds: int,
        task_id: Optional[str] = None,
    ) -> str:
        """
        多少秒后打印某句话（一次性任务）
        
        Args:
            message: 要打印的消息
            delay_seconds: 延迟秒数
            task_id: 任务ID，如果不提供则自动生成（格式：once_N）
            callback: 回调函数，如果不提供则打印消息
            
        Returns:
            str: 任务ID
            
        Example:
            >>> timer.once_after("该喝水了！", 5)
            'once_1'
        """
        self._task_counter += 1
        if not task_id:
            task_id = f"once_{self._task_counter}"
        
        target_time = datetime.now() + timedelta(seconds=delay_seconds)
        
        task = TimerTask(
            id=task_id,
            message=message,
            target_time=target_time,
            is_active=True,
            task_type="once"
        )
        
        self.tasks[task_id] = task
        
        if not self._running:
            self.start()
        self.save()
        return task_id
    
    def interval_every(
        self,
        message: str,
        interval_seconds: int,
        interval_count: Optional[int] = None,
        task_id: Optional[str] = None,
    ) -> str:
        """
        每隔多少秒打印某句话（周期性任务）
        
        Args:
            message: 要打印的消息
            interval_seconds: 间隔秒数
            interval_count: 触发次数，-1 表示无限次
            task_id: 任务ID，如果不提供则自动生成（格式：interval_N）
            callback: 回调函数，如果不提供则打印消息
            
        Returns:
            str: 任务ID
            
        Example:
            >>> timer.interval_every("注意休息眼睛", 3)
            'interval_1'
        """
        self._task_counter += 1
        if not task_id:
            task_id = f"interval_{self._task_counter}"
        
        target_time = datetime.now() + timedelta(seconds=interval_seconds)
        
        task = TimerTask(
            id=task_id,
            message=message,
            interval=interval_seconds,
            target_time=target_time,
            interval_count=interval_count,
            is_active=True,
            task_type="interval"
        )
        
        self.tasks[task_id] = task
        
        if not self._running:
            self.start()
        self.save()
        return task_id
    
    def daily_at(
        self,
        message: str,
        hour: int,
        minute: int,
        task_id: Optional[str] = None
    ) -> str:
        """
        每日多少点打印某句话（每日定时任务）
        
        Args:
            message: 要打印的消息
            hour: 小时 (0-23)
            minute: 分钟 (0-59)
            task_id: 任务ID，如果不提供则自动生成（格式：daily_N）
            callback: 回调函数，如果不提供则打印消息
            
        Returns:
            str: 任务ID
            
        Raises:
            ValueError: 当小时或分钟超出范围时抛出
            
        Example:
            >>> timer.daily_at("早上好！", 8, 0)
            'daily_1'
        """
        if not 0 <= hour <= 23:
            raise ValueError("小时必须在 0-23 之间")
        if not 0 <= minute <= 59:
            raise ValueError("分钟必须在 0-59 之间")
        
        self._task_counter += 1
        if not task_id:
            task_id = f"daily_{self._task_counter}"
        
        now = datetime.now()
        target_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        if target_time <= now:
            target_time += timedelta(days=1)
        
        task = TimerTask(
            id=task_id,
            message=message,
            daily_time=(hour, minute),
            target_time=target_time,
            is_active=True,
            task_type="daily"
        )
        
        self.tasks[task_id] = task
        
        if not self._running:
            self.start()
        self.save()
        return task_id
    
    def cancel(self, task_id: str) -> bool:
        """
        取消定时任务
        
        Args:
            task_id: 要取消的任务ID
            
        Returns:
            bool: 是否成功取消
            
        Example:
            >>> timer.cancel("once_1")
            True
        """
        if task_id in self.tasks:
            self.tasks[task_id].is_active = False
            del self.tasks[task_id]
            return True
        return False
    
    def pause(self, task_id: str) -> bool:
        """
        暂停定时任务（保留任务，只是停止执行）
        
        Args:
            task_id: 要暂停的任务ID
            
        Returns:
            bool: 是否成功暂停
            
        Example:
            >>> timer.pause("interval_1")
            True
        """
        if task_id in self.tasks:
            self.tasks[task_id].is_active = False
            return True
        return False
    
    def resume(self, task_id: str) -> bool:
        """
        恢复定时任务
        
        Args:
            task_id: 要恢复的任务ID
            
        Returns:
            bool: 是否成功恢复
            
        Example:
            >>> timer.resume("interval_1")
            True
        """
        if task_id in self.tasks:
            task = self.tasks[task_id]
            task.is_active = True
            
            if task.task_type == "once":
                if task.interval:
                    task.target_time = datetime.now() + timedelta(seconds=task.interval)
            elif task.task_type == "interval":
                task.target_time = datetime.now() + timedelta(seconds=task.interval)
            elif task.task_type == "daily":
                hour, minute = task.daily_time
                now = datetime.now()
                target_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
                if target_time <= now:
                    target_time += timedelta(days=1)
                task.target_time = target_time
            
            return True
        return False
    
    def get_tasks(self) -> list:
        """
        获取所有任务信息
        
        Returns:
            list: 任务信息列表，每个任务包含以下字段：
                - id: 任务ID
                - message: 任务消息
                - type: 任务类型
                - active: 是否活跃
                - remaining_seconds: 剩余秒数（一次性任务）
                - target_time: 目标时间（一次性任务）
                - interval_seconds: 间隔秒数（周期性任务）
                - next_trigger_in: 下次触发剩余秒数（周期性任务）
                - daily_time: 每日时间（每日任务）
                - next_trigger: 下次触发时间（每日任务）
                
        Example:
            >>> for task in timer.get_tasks():
            ...     print(task)
        """
        tasks_info = []
        now = datetime.now()
        
        for task in self.tasks.values():
            info = {
                "id": task.id,
                "message": task.message,
                "task_type": task.task_type,
                "is_active": task.is_active
            }
            
            if task.task_type == "once":
                if task.target_time:
                    remaining = (task.target_time - now).total_seconds()
                    info["remaining_seconds"] = int(remaining)
                    info["target_time"] = task.target_time.strftime("%Y-%m-%d %H:%M:%S")
            
            elif task.task_type == "interval":
                info["interval_seconds"] = task.interval
                if task.target_time:
                    remaining = (task.target_time - now).total_seconds()
                    info["next_trigger_in"] = int(remaining)
            
            elif task.task_type == "daily":
                hour, minute = task.daily_time
                info["daily_time"] = f"{hour:02d}:{minute:02d}"
                if task.target_time:
                    info["next_trigger"] = task.target_time.strftime("%Y-%m-%d %H:%M:%S")
            
            tasks_info.append(info)
        
        return tasks_info
    
    def clear_all(self):
        """
        清除所有任务
        
        删除所有任务并清空任务字典。
        定时器线程会继续运行，但没有任务可执行。
        """
        self.tasks.clear()
    def save(self):
        """
        保存当前所有任务（只保存未完成或将来会触发的任务）
        """
        now = datetime.now()
        tasks_to_save = []
        
        for task in self.tasks.values():
            # 跳过已取消的任务
            if not task.is_active:
                continue
            
            # 对于一次性任务，如果已经触发过，不保存
            if task.task_type == "once":
                if task.target_time and now >= task.target_time:
                    continue
            
            # 对于周期性任务，如果次数已用完，不保存
            elif task.task_type == "interval":
                if task.interval_count == 0:
                    continue
            
            # 每日任务一直保存
            tasks_to_save.append(task)
        
        # 转换任务为可序列化的格式
        list = []
        for task in tasks_to_save:
            task_info = {
                "id": task.id,
                "message": task.message,
                "task_type": task.task_type,
                "is_active": task.is_active
            }
            
            if task.task_type == "once":
                if task.target_time:
                    remaining = (task.target_time - now).total_seconds()
                    task_info["remaining_seconds"] = int(remaining)
                    task_info["target_time"] = task.target_time.strftime("%Y-%m-%d %H:%M:%S")
            
            elif task.task_type == "interval":
                task_info["interval_seconds"] = task.interval
                if task.target_time:
                    remaining = (task.target_time - now).total_seconds()
                    task_info["next_trigger_in"] = int(remaining)
                if task.interval_count is not None:
                    task_info["interval_count"] = task.interval_count
            
            elif task.task_type == "daily":
                hour, minute = task.daily_time
                task_info["daily_time"] = f"{hour:02d}:{minute:02d}"
                if task.target_time:
                    task_info["next_trigger"] = task.target_time.strftime("%Y-%m-%d %H:%M:%S")
            
            list.append(task_info)
        
        data = {
            "tasks": list,
            "counter": self._task_counter
        }
        
        with open("timer.json", "w") as f:
            json.dump(data, f, indent=4)

_global_timer = None


def get_timer() -> Timer:
    """
    获取全局定时器实例（单例模式）
    
    Returns:
        Timer: 全局定时器实例
        
    第一次调用时会创建并启动定时器，后续调用返回同一个实例。
    这样可以在整个应用中共享同一个定时器。
    
    Example:
        >>> timer = get_timer()
        >>> timer.once_after("测试", 5)
    """
    global _global_timer
    if _global_timer is None:
        _global_timer = Timer()
        _global_timer.start()
    return _global_timer


if __name__ == "__main__":
    print("=" * 60)
    print("定时器测试")
    print("=" * 60)
    
    timer = Timer()
    
    print("\n当前所有任务:")
    for task in timer.get_tasks():
        print(f"   {task}")
    
    
    task3 = timer.daily_at("每日定时提醒", 1,0)
    print(f"   任务ID: {task3}")
    
    print("\n剩余任务:")
    for task in timer.get_tasks():
        print(f"   {task}")
    timer.stop()
    print("\n测试完成")
