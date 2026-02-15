"""
虚拟环境管理工具
用于检测和创建 Python 虚拟环境
"""

import sys
import os
import subprocess
from pathlib import Path
from typing import Optional
class VenvManager:
    """
    虚拟环境管理器
    
    提供以下功能：
    1. 检测当前目录是否存在虚拟环境
    2. 如果不存在则自动创建
    3. 获取虚拟环境的 Python 解释器路径
    4. 激活虚拟环境
    """
    
    def __init__(self, venv_name: str = "code_venv"):
        """
        初始化虚拟环境管理器
        
        Args:
            venv_name: 虚拟环境文件夹名称，默认为 "venv"
        """
        self.venv_name = venv_name
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.venv_path = os.path.join(self.base_dir, venv_name)
        self.init_or_create()
        
    def check_venv_exists(self) -> bool:
        """
        检查虚拟环境是否存在
        
        Returns:
            bool: 如果虚拟环境存在返回 True，否则返回 False
        """
        venv_dir = Path(self.venv_path)
        return venv_dir.exists() and (venv_dir / "pyvenv.cfg").exists()
    
    def create_venv(self, python_path: Optional[str] = None) -> bool:
        """
        创建虚拟环境
        
        Args:
            python_path: 指定 Python 解释器路径，如果为 None 则使用当前 Python
            
        Returns:
            bool: 创建成功返回 True，失败返回 False
        """
        try:
            if self.check_venv_exists():
                print(f"虚拟环境 {self.venv_name} 已存在，无需创建")
                return True
            
            print(f"正在创建虚拟环境 {self.venv_name}...")
            
            if python_path:
                cmd = [python_path, "-m", "venv", self.venv_path]
            else:
                cmd = [sys.executable, "-m", "venv", self.venv_path] 
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            if result.returncode == 0:
                print(f"✓ 虚拟环境 {self.venv_name} 创建成功")
                print(f"  路径: {self.venv_path}")
                return True
            else:
                print(f"✗ 虚拟环境创建失败: {result.stderr}")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"✗ 创建虚拟环境时出错: {e.stderr}")
            return False
        except Exception as e:
            print(f"✗ 创建虚拟环境时发生错误: {str(e)}")
            return False
    
    def get_python_path(self) -> Optional[str]:
        """
        获取虚拟环境的 Python 解释器路径
        
        Returns:
            str: Python 解释器路径，如果虚拟环境不存在则返回 None
        """
        if not self.check_venv_exists():
            return None
        
        if sys.platform == "win32":
            return os.path.join(self.venv_path, "Scripts", "python.exe")
        else:
            return os.path.join(self.venv_path, "bin", "python")
    
    def get_pip_path(self) -> Optional[str]:
        """
        获取虚拟环境的 pip 路径
        
        Returns:
            str: pip 路径，如果虚拟环境不存在则返回 None
        """
        if not self.check_venv_exists():
            return None
        
        if sys.platform == "win32":
            return os.path.join(self.venv_path, "Scripts", "pip.exe")
        else:
            return os.path.join(self.venv_path, "bin", "pip")
    def get_package(self):
        pip_path = self.get_pip_path()
        if not pip_path:
            return None
        
        try:
            result = subprocess.run(
                [pip_path, "list"],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"✗ 获取已安装包时出错: {e.stderr}")
            return None
    
    def install_package(self, package: str) -> bool:
        """
        在虚拟环境中安装 Python 包
        
        Args:
            package: 包名，如 "requests" 或 "requests==2.28.0"
            
        Returns:
            bool: 安装成功返回 True，失败返回 False
        """
        pip_path = self.get_pip_path()
        if not pip_path:
            print("✗ 虚拟环境不存在，无法安装包")
            return False
        
        try:
            print(f"正在安装 {package}...")
            result = subprocess.run(
                [pip_path, "install", package],
                capture_output=True,
                text=True,
                check=True
            )
            
            if result.returncode == 0:
                print(f"✓ {package} 安装成功")
                return True
            else:
                print(f"✗ {package} 安装失败: {result.stderr}")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"✗ 安装包时出错: {e.stderr}")
            return False
        except Exception as e:
            print(f"✗ 安装包时发生错误: {str(e)}")
            return False
    
    def run_python(self, script: str) -> tuple:
        """
        在虚拟环境中运行 Python 脚本
        
        Args:
            script: Python 代码字符串
            
        Returns:
            tuple: (returncode, stdout, stderr)
        """
        python_path = self.get_python_path()
        if not python_path:
            return (1, "", "虚拟环境不存在")
        
        try:
            result = subprocess.run(
                [python_path, "-c", script],
                capture_output=True,
                text=True
            )
            return (result.returncode, result.stdout, result.stderr)
        except Exception as e:
            return (1, "", str(e))
    
    def init_or_create(self) -> bool:
        """
        初始化或创建虚拟环境
        
        如果虚拟环境不存在则创建，存在则直接返回成功
        
        Returns:
            bool: 成功返回 True，失败返回 False
        """
        if self.check_venv_exists():
            print(f"✓ 虚拟环境 {self.venv_name} 已存在")
            print(f"  路径: {self.venv_path}")
            print(f"  Python: {self.get_python_path()}")
            return True
        else:
            return self.create_venv()
    
    def get_info(self) -> dict:
        """
        获取虚拟环境信息
        
        Returns:
            dict: 包含虚拟环境信息的字典
        """
        info = {
            "name": self.venv_name,
            "path": self.venv_path,
            "exists": self.check_venv_exists(),
            "python_path": self.get_python_path(),
            "pip_path": self.get_pip_path()
        }
        return info


_global_venv_manager = None


def get_venv_manager(venv_name: str = "code_venv") -> VenvManager:
    """
    获取全局虚拟环境管理器实例（单例模式）
    
    Args:
        venv_name: 虚拟环境文件夹名称
        
    Returns:
        VenvManager: 全局虚拟环境管理器实例
    """
    global _global_venv_manager
    if _global_venv_manager is None:
        _global_venv_manager = VenvManager(venv_name)
    return _global_venv_manager

