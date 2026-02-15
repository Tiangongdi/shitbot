import os
import yaml
class Skill:
    def __init__(self) -> None:
        self.file_path = os.path.join(os.path.dirname(__file__), "..", "Skills")
        if not os.path.exists(self.file_path):
            os.makedirs(self.file_path)
        self.skill_list = [entry.name for entry in os.scandir(self.file_path) if entry.is_dir()] # 技能文件列表
        self.skill_dict = {} # 技能文件路径字典
        self.init_skill_dict()
    def init_skill_dict(self):
        for skill in self.skill_list:
            s= os.path.abspath(os.path.join(self.file_path, skill))
            if "SKILL.md" in [entry.name for entry in os.scandir(s)]:
                path = os.path.abspath(os.path.join(s, "SKILL.md"))
                name,description = self.get_skill_info(path)    
                dict = {"path": path, "name": name, "description": description}
                if name and description:
                    self.skill_dict[name] = dict
    def get_skill_info(self,path: str):
        if not os.path.exists(path):
            return None,None    
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        if content.startswith("---"):
            end = content.find("---", 3)
            if end != -1:
                skill_content = content[3:end].strip()
                data = yaml.safe_load(skill_content)
                return data.get('name'), data.get('description')
        return None, None
if __name__ == "__main__":
    skill = Skill()
    skill.init_skill_dict()