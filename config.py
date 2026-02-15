import os
import yaml
from typing import Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class AIConfig:
    api_key: str
    value: str = "zai"
    model: str = "glm-5"


@dataclass
class BochaConfig:
    api_key: str
    base_url: str = "https://api.bocha.com"
    index_name: str = "news"


@dataclass
class BrowserConfig:
    """
    浏览器配置
    使用系统 Edge 浏览器，自动检测路径
    """
    playwright_browsers_path: Optional[str] = None


@dataclass
class UserConfig:
    """
    用户配置
    """
    user_name: str = "黎大白"
    bot_name: str = "偷摸零"
    bot_prompt: str = "你会经常说咕咕嘎嘎（企鹅叫）"


@dataclass
class EmailConfig:
    """
    邮件配置
    用于发送邮件的 SMTP 服务器配置
    """
    smtp_server: str = "smtp.163.com"
    smtp_port: int = 465
    email: str = ""
    password: str = ""
    use_tls: bool = True


@dataclass
class StopConfig:
    """
    停止配置
    用于配置需要停止的文件或功能
    """
    file: list = None

    def __post_init__(self):
        if self.file is None:
            self.file = []


@dataclass
class TavilyConfig:
    """
    Tavily 搜索 API 配置
    """
    key: str


@dataclass
class WebSearchConfig:
    """
    网页搜索配置
    web_search_ID: 1=博查搜索, 2=Tavily搜索
    """
    web_search_ID: int = 2


@dataclass
class AppConfig:
    user: UserConfig
    ai: AIConfig
    bocha: BochaConfig
    browser: BrowserConfig
    email: EmailConfig
    stop: StopConfig
    tavily: TavilyConfig
    web_search: WebSearchConfig
    default_provider: str = "minimax"


def load_config(config_path: Optional[str] = None) -> AppConfig:
    if config_path is None:
        config_path = os.environ.get(
            "CONFIG_PATH", 
            str(Path(__file__).parent / "config.yaml")
        )
    
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"配置文件不存在: {config_path}")
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config_data = yaml.safe_load(f)
    
    user_config_data = config_data.get('user', {})
    user_config = UserConfig(
        user_name=user_config_data.get('user_name', os.environ.get('USER_NAME', 'User')),
        bot_name=user_config_data.get('bot_name', os.environ.get('BOT_NAME', 'ShitBot')),
        bot_prompt=user_config_data.get('bot_prompt', os.environ.get('BOT_PROMPT', '默认'))
    )
    
    ai_config_data = config_data.get('ai', {})
    ai_config = AIConfig(
        api_key=ai_config_data.get('api_key', os.environ.get('AI_API_KEY', '')),
        value=ai_config_data.get('value', 'zai'),
        model=ai_config_data.get('model', 'MiniMax-Text-01')
    )
    
    bocha_config_data = config_data.get('bocha', {})
    bocha_config = BochaConfig(
        api_key=bocha_config_data.get('api_key', os.environ.get('BOCHA_API_KEY', '')),
        base_url=bocha_config_data.get('base_url', 'https://api.bocha.com'),
        index_name=bocha_config_data.get('index_name', 'news')
    )
    
    browser_config_data = config_data.get('browser', {})
    browser_config = BrowserConfig(
        playwright_browsers_path=browser_config_data.get('playwright_browsers_path')
    )
    
    email_config_data = config_data.get('email', {})
    email_config = EmailConfig(
        smtp_server=email_config_data.get('smtp_server', 'smtp.gmail.com'),
        smtp_port=email_config_data.get('smtp_port', 587),
        email=email_config_data.get('email', ''),
        password=email_config_data.get('password', ''),
        use_tls=email_config_data.get('use_tls', True)
    )
    
    stop_config_data = config_data.get('stop', {})
    stop_config = StopConfig(
        file=stop_config_data.get('file', [])
    )
    
    tavily_config_data = config_data.get('tavily', {})
    tavily_config = TavilyConfig(
        key=tavily_config_data.get('key', os.environ.get('TAVILY_API_KEY', ''))
    )
    
    web_search_config_data = config_data.get('web_search', {})
    web_search_config = WebSearchConfig(
        web_search_ID=web_search_config_data.get('web_search_ID', 1)
    )
    
    default_provider = config_data.get('default_provider', 'ai')
    
    return AppConfig(
        user=user_config,
        ai=ai_config,
        bocha=bocha_config,
        browser=browser_config,
        email=email_config,
        stop=stop_config,
        tavily=tavily_config,
        web_search=web_search_config,
        default_provider=default_provider
    )


def create_default_config(config_path: str = "config.yaml"):
    default_config = {
        'user': {
            'user_name': 'User',
            'bot_name': 'ShitBot'
        },
        'ai': {
            'api_key': '',
            'value': 'zai',
            'model': 'MiniMax-Text-01'
        },
        'bocha': {
            'api_key': '',
            'base_url': 'https://api.bocha.com',
            'index_name': 'news'
        },
        'browser': {
            'playwright_browsers_path': '',
        },
        'email': {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'email': '',
            'password': '',
            'use_tls': True
        },
        'stop': {
            'file': []
        },
        'tavily': {
            'key': ''
        },
        'web_search': {
            'web_search_ID': 1
        },
        'default_provider': 'glm '
    }
    
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(default_config, f, default_flow_style=False, allow_unicode=True)
    
    print(f"默认配置文件已创建: {config_path}")


def setup_wizard(config_path: str = "config.yaml"):
    """
    首次运行配置向导
    引导用户设置 API 密钥、用户名和机器人名称
    """
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.prompt import Prompt
    from rich import print as rprint
    from read_models import read_models_json_relative
    
    console = Console()
    models_data = read_models_json_relative()   
    
    # 确保正确获取 domestic_common_models 列表
    if models_data and 'domestic_common_models' in models_data:
        models = models_data['domestic_common_models']
    else:
        # 如果获取失败，使用默认模型列表
        models = [
            {"name": "MOONSHOT(Kimi) - 月之暗面", "value": "moonshot"},
            {"name": "DEEPSEEK - 深度求索", "value": "deepseek"},
            {"name": "MINIMAX", "value": "minimax"},
            {"name": "XIAOMI_MIMO - 小米", "value": "xiaomi_mimo"},
            {"name": "VOLCENGINE - 火山引擎", "value": "volcengine"},
            {"name": "DASHSCOPE - 阿里云", "value": "dashscope"},
            {"name": "ZHIPU(ZAI) - 智谱AI", "value": "zai"},
            {"name": "OPENAI - ChatGPT", "value": "openai"},
            {"name": "ANTHROPIC - Claude", "value": "anthropic"},
            {"name": "GEMINI - Google", "value": "gemini"},
            {"name": "COHERE", "value": "cohere"},
            {"name": "MISTRAL", "value": "mistral"},
            {"name": "GROQ", "value": "groq"},
            {"name": "PERPLEXITY", "value": "perplexity"},
            {"name": "OPENROUTER", "value": "openrouter"}
        ]
        print("警告: 无法读取 models.json 文件，使用默认模型列表")
    
    print("\n")
    console.print(Panel(
        Text("欢迎使用 ShitBot！\n请按提示完成初始配置", justify="center"),
        title="首次运行配置向导",
        style="cyan"
    ))
    
    print("\n[1/5] 用户设置")
    print("-" * 40)
    
    user_name = Prompt.ask("请输入您的名字", default="User")
    bot_name = Prompt.ask("请输入机器人名字", default="ShitBot")
    bot_prompt = Prompt.ask("请输入机器人语气提示词,例如：请用一个智能助手的语气回答", default="请用一个智能助手的语气回答")
    print("\n[2/5] AI API 设置")
    print("-" * 40)
    print("选择 AI 模型:")
    for i, model in enumerate(models, 1):
        print(f"[{str(i)}] {model['name']}")
    model_index = Prompt.ask("请选择模型 [1-{}]".format(len(models)), default="1")
    model_api = models[int(model_index) - 1]['value']   

    print("请注册账号并申请 API 密钥")
    print("按 Enter 跳过（后续可随时配置）")
    
    ai_api_key = Prompt.ask("请输入 AI API 密钥", default="")

    print("填写使用的模型")
    model = Prompt.ask("请输入使用的模型", default="")   
    
    print("\n[3/5] 网页搜索服务设置")
    print("-" * 40)
    print("选择默认的网页搜索服务:")
    print("  1. 博查搜索 (Bocha)")
    print("  2. Tavily 搜索")
    web_search_id = Prompt.ask("请选择 [1/2]", default="1")
    bocha_api_key = ""
    tavily_api_key = "" 
    if  web_search_id == "1":
        print("\n 博查搜索 API 设置")
        print("-" * 40)
        print("获取地址: https://www.bocha.com/")
        print("请注册账号并申请 API 密钥")
        print("按 Enter 跳过（后续可随时配置）")
        
        bocha_api_key = Prompt.ask("请输入博查搜索 API 密钥", default="")
    else:
        print("\n Tavily 搜索 API 设置")
        print("-" * 40)
        print("获取地址: https://tavily.com/")
        print("请注册账号并申请 API 密钥")
        print("按 Enter 跳过（后续可随时配置）")
        
        tavily_api_key = Prompt.ask("请输入 Tavily 搜索 API 密钥", default="")
    
    print("\n[4/5] 邮件服务设置")
    print("-" * 40)
    print("用于发送邮件的 SMTP 服务器配置")
    print("常见邮箱服务商配置:")
    print("  - Gmail: smtp.gmail.com:587")
    print("  - QQ邮箱: smtp.qq.com:587")
    print("  - 163邮箱: smtp.163.com:465")
    print("  - Outlook: smtp-mail.outlook.com:587")
    print("注意: 使用 Gmail 需要生成应用专用密码")
    print("按 Enter 跳过（后续可随时配置）")
    
    email_address = Prompt.ask("请输入邮箱地址", default="")
    email_password = Prompt.ask("请输入邮箱密码或授权码", default="")
    smtp_server = Prompt.ask("请输入 SMTP 服务器地址", default="smtp.gmail.com")
    smtp_port = Prompt.ask("请输入 SMTP 端口", default="587")
    
    print("\n[5/5] 禁止访问文件夹设置")
    print("-" * 40)
    print("以下输入你要禁止模型访问的文件夹路径（按 Enter 结束）")
    file_num = 1
    stop_file = []
    while True:
        stop_file = Prompt.ask(f"[{file_num}]", default="")
        if not stop_file:
            break
        stop_file.append(stop_file)
        file_num += 1

    print("\n保存配置")
    print("-" * 40)
    
    config = {
        'user': {
            'user_name': user_name,
            'bot_name': bot_name,
            'bot_prompt': bot_prompt
        },
        'ai': {
            'api_key': ai_api_key,
            'value': model_api,
            'model': model
        },
        'bocha': {
            'api_key': bocha_api_key,
            'base_url': 'https://api.bocha.com',
            'index_name': 'news'
        },
        'tavily': {
            'key': tavily_api_key
        },
        'web_search': {
            'web_search_ID': int(web_search_id)
        },
        'browser': {
            'playwright_browsers_path': ''
        },
        'email': {
            'smtp_server': smtp_server,
            'smtp_port': int(smtp_port),
            'email': email_address,
            'password': email_password,
            'use_tls': True
        },
        'stop': {
            'file': stop_file
        },
        'default_provider': 'ai'
    }
    
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
    
    console.print(Panel(
        Text(f"✓ 配置已保存到: {config_path}\n\n"
             f"用户名称: {user_name}\n"
             f"机器人名称: {bot_name}\n"
             f"AI API: {'✓ 已配置' if ai_api_key else '○ 未配置'}\n"
             f"搜索 API: {'✓ 已配置' if not (int(web_search_id) == 0) else '○ 未配置'}\n"
             f"邮件服务: {'✓ 已配置' if email_address else '○ 未配置'}\n\n"
             "如需修改配置，可编辑 config.yaml 文件,或者执行init_project.py重新配置",
             justify="center"),
        title="配置完成",
        style="green"
    ))
    
    return True
