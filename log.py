import os
from datetime import datetime
import json

class Log:
    def __init__(self):
        self.log = []
        self.log_path = os.path.join(os.path.dirname(__file__), ".", "Logs")  # 文件夹地址
        self.timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path)
    
    def add_log(self, log):
        """
        添加日志到记录
        
        Args:
            log: 要添加的日志
        """
        serializable_log = self._make_serializable(log)
        self.log.append(serializable_log)
        self.save_log() 
    
    def _make_serializable(self, obj):
        """
        将对象转换为可序列化的字典格式
        
        Args:
            obj: 要转换的对象
            
        Returns:
            可序列化的字典
        """
        if hasattr(obj, 'model_dump'):
            return obj.model_dump()
        elif hasattr(obj, '__dict__'):
            result = {}
            for key, value in obj.__dict__.items():
                if isinstance(value, list):
                    result[key] = [self._make_serializable(item) for item in value]
                elif hasattr(value, '__dict__'):
                    result[key] = self._make_serializable(value)
                else:
                    result[key] = value
            return result
        return obj 
    def save_log(self):
        """
        保存日志到文件
        """
        with open(os.path.join(self.log_path, f"{self.timestamp}.json"), "w", encoding="utf-8") as f:
            json.dump(self.log, f, ensure_ascii=False, indent=4)    