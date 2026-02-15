import os
from pathlib import Path
from config import load_config


class BotPromt:

    def get_prompt(self, prompt_file: str = "Bot.txt", prompt_dir: str = None) -> str:
        """
        获取提示词内容并替换变量
        
        Args:
            prompt_file: 提示词文件名，默认为 "Bot.txt"
            prompt_dir: 提示词目录路径，默认为 "promt" 目录
        
        Returns:
            替换变量后的提示词内容
        """
        if prompt_dir is None:
            prompt_dir = str(Path(__file__).parent / "prompt")
        
        prompt_path = os.path.join(prompt_dir, prompt_file)
        
        if not os.path.exists(prompt_path):
            raise FileNotFoundError(f"提示词文件不存在: {prompt_path}")
        
        with open(prompt_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return content

    def get_all_prompts(self, prompt_dir: str = None) -> dict:
        """
        获取提示词目录下所有提示词文件
        
        Args:
            prompt_dir: 提示词目录路径，默认为 "promt" 目录
        
        Returns:
            包含所有提示词的字典，键为文件名（不含扩展名），值为替换后的内容
        """
        if prompt_dir is None:
            prompt_dir = str(Path(__file__).parent / "prompt")
        
        if not os.path.exists(prompt_dir):
            raise FileNotFoundError(f"提示词目录不存在: {prompt_dir}")
        
        prompts = {}
        
        for filename in os.listdir(prompt_dir):
            if filename.endswith('.txt'):
                prompt_name = os.path.splitext(filename)[0]
                prompts[prompt_name] = self.get_prompt(filename, prompt_dir)
        
        return prompts  
if __name__ == "__main__":
    promt = BotPromt()
    print(promt.get_prompt("Bot.txt").format(name="BOT", user="林粒", user_set="看看"))  