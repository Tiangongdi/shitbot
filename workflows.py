import os
from pathlib import Path
from config import load_settings

WORKFLOW_PATHS = {
    "coder": "CODER.md",
    "plan": "PLAN.md",
    "sole": "SOLE.md",      
}

class Workflow:
    def __init__(self):
        self.settings = load_settings()
        self.default_workflow = self.settings.default_workflow
        self.workflow_path = WORKFLOW_PATHS[self.default_workflow]
    
    def get_workflow_file(self) -> str:
        full_path = str(Path(__file__).parent / ".shitbot" / "workflows" / self.workflow_path)
        
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"工作流文件不存在: {full_path}")
        
        with open(full_path, 'r', encoding='utf-8') as f:
            return f.read()     
    
    def set_workflow(self, workflow: str):
        if workflow not in WORKFLOW_PATHS:
            raise ValueError(f"无效的工作流: {workflow}，可用的工作流: {list(WORKFLOW_PATHS.keys())}")
        self.default_workflow = workflow
        self.workflow_path = WORKFLOW_PATHS[workflow]
    
    def get_current_workflow(self) -> str:
        return self.default_workflow
    
    def get_available_workflows(self) -> list:
        return list(WORKFLOW_PATHS.keys())       