from typing import Optional, Dict, Any
from string import Formatter
import venv
class SafeDict(dict):
    """
    安全字典类
    当访问不存在的键时返回 "null" 而不是抛出 KeyError
    """
    def __missing__(self, key):
        return "null"


class SafeFormatter(Formatter):
    """
    安全格式化器
    当格式化字符串中的键不存在时返回 "null"
    """
    def get_value(self, key, args, kwargs):
        if isinstance(key, str):
            return kwargs.get(key, "null")
        return super().get_value(key, args, kwargs)


def safe_format(template: str, data: Dict[str, Any]) -> str:
    """
    安全格式化字符串
    如果字典中没有对应的键，则使用 "null" 替换
    
    Args:
        template: 格式化字符串模板，如 "姓名: {name}, 年龄: {age}"
        data: 包含替换值的字典
        
    Returns:
        str: 格式化后的字符串
        
    Example:
        >>> data = {"name": "张三", "age": 18}
        >>> safe_format("姓名: {name}, 年龄: {age}, 职业: {job}", data)
        '姓名: 张三, 年龄: 18, 职业: null'
    """
    return SafeFormatter().format(template, **data)


def format_with_null(template: str, data: Dict[str, Any]) -> str:
    """
    使用 format_map 进行安全格式化
    如果字典中没有对应的键，则使用 "null" 替换
    
    Args:
        template: 格式化字符串模板
        data: 包含替换值的字典
        
    Returns:
        str: 格式化后的字符串
    """
    return template.format_map(SafeDict(data))

