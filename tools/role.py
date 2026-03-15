import os
import yaml
class Role:
    def __init__(self) -> None:
        self.file_path = os.path.join(os.path.dirname(__file__), "..", "Roles")
        if not os.path.exists(self.file_path):
            os.makedirs(self.file_path)
        self.role_list = [entry.name for entry in os.scandir(self.file_path) if entry.is_dir()] # 角色文件列表
        self.role_dict = {} # 角色文件路径字典
        self.init_role_dict()
    def init_role_dict(self):
        for role in self.role_list:
            s= os.path.abspath(os.path.join(self.file_path, role))
            if "ROLE.md" in [entry.name for entry in os.scandir(s)]:
                path = os.path.abspath(os.path.join(s, "ROLE.md"))
                name,description = self.get_role_info(path)    
                dict = {"path": path, "name": name, "description": description}
                if name and description:
                    self.role_dict[name] = dict
    def get_role_info(self,path: str):
        if not os.path.exists(path):
            return None,None    
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        if content.startswith("---"):
            end = content.find("---", 3)
            if end != -1:
                role_content = content[3:end].strip()
                data = yaml.safe_load(role_content)
                return data.get('name'), data.get('description')
        return None, None
if __name__ == "__main__":
    role = Role()
    print(role.role_dict)
