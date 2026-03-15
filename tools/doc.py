import os
class Doc:
    def __init__(self) -> None:
        self.file_path = os.path.join(os.path.dirname(__file__), "..", "Docs")  # 文件夹地址
        self.file_list = os.listdir(self.file_path)  # 文件列表
        self.file_dict = {}  # 文件字典 # 文件字典 
        self.value = {} # 一级标题字典
        self.get_file_list()
    def get_file_list(self):
        self.md_files = [os.path.splitext(f)[0] for f in os.listdir(self.file_path) if f.endswith('.md')]
        for file in self.md_files:
            v, result, current_keys_list = self.get_one_file(file)
            self.value[file] = {
                "value": v,
                "keys": current_keys_list
                }
            self.file_dict[file] = result
    def get_data(self,file_name,key):
        data = self.file_dict[file_name]
        if key in data:
            return data[key]
        else:
            return None
    def get_one_file(self,file_name):
        """
        获取一个文件的内容
        
        Args:
            file_name: 文件名称
        """
        with open(os.path.join(self.file_path, f"{file_name}.md"), "r", encoding="utf-8") as f:
            content = f.read()
        v = None
        # md生成json格式 里面每个#会被识别为标题成为key然后#下面内容生成字典
        lines = content.split("\n")# 按行分割
        result = {}
        current_key = ""
        current_content = []
        current_keys_list = []
        for line in lines:
            if line.startswith("##") and not line.startswith("###"):
                if current_key != "":
                    result[current_key] = "\n".join(current_content).strip()
                current_key = line[2:].strip()  # [2:] 跳过 "# "
                current_keys_list.append(current_key)
                current_content = []
            elif line.startswith("#") and not v: # 一级标题并且 v 为空
                v = line[2:].strip()  # [2:] 跳过 "# "
            else:
                current_content.append(line)
        if current_key != "":
            result[current_key] = "\n".join(current_content).strip()
        return v, result, current_keys_list
if __name__ == "__main__":
    doc = Doc()
    doc.get_file_list()