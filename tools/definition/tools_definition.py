# Tools Definition Module
"""
工具定义模块，用于生成AI调用的工具定义列表
"""

def get_tools_definition(if_not_timer: bool, if_not_subagent: bool) -> list:
    """获取技能定义列表，用于 AI 调用"""
    tools = [
        {
            "type": "function",
            "function": {
                "name": "search_web",
                "description": "在网络上搜索信息",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "搜索查询词"
                        },
                        "count": {
                            "type": "integer",
                            "description": "返回结果数量",
                            "default": 5
                        }
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "webbot_task",
                "description": "让WebBot执行任务,WebBot是一个浏览器操作助手,它可以查看网页信息,点击网页,填写表单等浏览器修改功能",    
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "告诉WebBot要执行的任务"
                        }
                    },
                    "required": ["query"]                                    
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "write_file",
                "description": "给指定文件写入内容",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "要写入的文件路径"
                        },
                        "content": {
                            "type": "string",
                            "description": "要写入的内容"
                        }
                    },
                    "required": ["file_path", "content"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "read_file",
                "description": "读取指定文件内容",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "要读取的文件路径"
                        }
                    },
                    "required": ["file_path"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "copy_file",
                "description": "复制指定文件,到目标路径",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "source_path": {
                            "type": "string",
                            "description": "要复制的文件路径"
                        },
                        "dest_path": {
                            "type": "string",
                            "description": "要复制到的目标路径"
                        }
                    },
                    "required": ["source_path", "dest_path"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "move_file",
                "description": "移动指定文件,到目标路径",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "source_path": {
                            "type": "string",
                            "description": "要移动的文件路径"
                        },
                        "dest_path": {
                            "type": "string",
                            "description": "要移动到的目标路径"
                        }
                    },
                    "required": ["source_path", "dest_path"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "create_dir",
                "description": "创建目录",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "dir_path": {
                            "type": "string",
                            "description": "要创建的目录路径"
                        }
                    },
                    "required": ["dir_path"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_dir_content",
                "description": "获取目录内容",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "dir_path": {
                            "type": "string",
                            "description": "要获取内容的目录路径"
                        }
                    },
                    "required": ["dir_path"]
                }
            }
        },  
        {
            "type": "function",
            "function": {
                "name": "shell_command",
                "description": "执行 shell 命令",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "command": {
                            "type": "string",
                            "description": "要执行的 shell 命令"
                        },
                        "use_timeout": {
                            "type": "boolean",
                            "description": "是否启用超时限制，默认为true。启用后命令执行超过60秒将自动终止并返回当前输出，防止命令长时间等待用户输入",
                            "default": True
                        }
                    },
                    "required": ["command"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "send_email",
                "description": "发送邮件到指定邮箱",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "to_email": {
                            "type": "string",
                            "description": "收件人邮箱地址"
                        },
                        "subject": {
                            "type": "string",
                            "description": "邮件主题"
                        },
                        "body": {
                            "type": "string",
                            "description": "邮件正文内容"
                        }
                    },
                    "required": ["to_email", "subject", "body"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "cancel_timer",
                "description": "取消定时任务",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "string",
                            "description": "任务ID"
                        }
                    },
                    "required": ["task_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "pause_timer",
                "description": "暂停定时任务",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "string",
                            "description": "任务ID"
                        }
                    },
                    "required": ["task_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "resume_timer",
                "description": "恢复定时任务",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "string",
                            "description": "任务ID"
                        }
                    },
                    "required": ["task_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "list",
                "description": "列出所有定时任务",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_memory",
                "description": "让memory_bot在以前的对话记录总结信息",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "memory_description": {
                            "type": "string",
                            "description": "让memory_bot的总结信息"
                        }
                    },
                    "required": ["memory_description"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_doc_list",
                "description": "列出所有可以阅读的doc文档",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_doc",
                "description": "获取doc文档内容,建议先调用get_doc_list获取文档列表",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_name": {
                            "type": "string",
                            "description": "文档名称"
                        },
                        "key": {
                            "type": "string",
                            "description": "文档键"
                        }
                    },
                    "required": ["file_name", "key"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "run_code",
                "description": "运行python代码",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "python代码"
                        },
                    },
                    "required": ["code"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "run_code_file",
                "description": "运行python代码文件",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code_file": {
                            "type": "string",
                            "description": "python代码文件路径"
                        },
                    },
                    "required": ["code_file"]
                }
            }
        },  
        {
            "type": "function",
            "function": {
                "name": "get_role",
                "description": "列出所有可以阅读的角色",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_skill",
                "description": "列出所有可以阅读的技能文档",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "list_email_folders",
                "description": "列出邮箱中的所有文件夹",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_email_list",
                "description": "获取邮箱中的邮件列表",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "folder": {
                            "type": "string",
                            "description": "文件夹名称，默认为INBOX",
                            "default": "INBOX"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "返回邮件数量，默认10",
                            "default": 10
                        },
                        "unread_only": {
                            "type": "boolean",
                            "description": "是否只获取未读邮件，默认False",
                            "default": False
                        }
                    },
                    "required": []
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_email_content",
                "description": "获取指定邮件的详细内容",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "email_id": {
                            "type": "string",
                            "description": "邮件ID"
                        },
                        "folder": {
                            "type": "string",
                            "description": "文件夹名称，默认为INBOX",
                            "default": "INBOX"
                        }
                    },
                    "required": ["email_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "search_emails",
                "description": "搜索邮件（按主题、发件人、正文搜索）",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "criteria": {
                            "type": "string",
                            "description": "搜索关键词"
                        },
                        "folder": {
                            "type": "string",
                            "description": "文件夹名称，默认为INBOX",
                            "default": "INBOX"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "返回邮件数量，默认10",
                            "default": 10
                        }
                    },
                    "required": ["criteria"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "mark_email_read",
                "description": "标记邮件为已读",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "email_id": {
                            "type": "string",
                            "description": "邮件ID"
                        },
                        "folder": {
                            "type": "string",
                            "description": "文件夹名称，默认为INBOX",
                            "default": "INBOX"
                        }
                    },
                    "required": ["email_id"]
                }
            }
        },
        {
             "type": "function",
            "function": {
                    "name": "append_to_file",
                "description": "在指定文件末尾追加文本内容",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "要追加内容的文件路径"
                        },
                        "content": {
                            "type": "string",
                            "description": "要追加的文本内容"
                        }
                    },
                    "required": ["file_path", "content"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "insert_line_at",
                "description": "在指定文件的指定行插入文本",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "要插入内容的文件路径"
                        },
                        "line_number": {
                            "type": "integer",
                            "description": "要插入的行号，从1开始"
                        },
                        "content": {
                            "type": "string",
                            "description": "要插入的文本内容"
                        }
                    },
                    "required": ["file_path", "line_number", "content"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "read_line_at",
                "description": "查看指定文件的指定行文本，可查看单行或多行",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "要查看的文件路径"
                        },
                        "line_number": {
                            "type": "integer",
                            "description": "要查看的起始行号，从1开始"
                        },
                        "end_number": {
                            "type": "integer",
                            "description": "要查看的结束行号，从1开始。如果不提供或与line_number相同，则只查看单行"
                        }
                    },
                    "required": ["file_path", "line_number"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "delete_line_at",
                "description": "删除指定文件的指定行文本，可删除单行或多行",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "要删除行的文件路径"
                        },
                        "line_number": {
                            "type": "integer",
                            "description": "要删除的起始行号，从1开始"
                        },
                        "end_number": {
                            "type": "integer",
                            "description": "要删除的结束行号，从1开始。如果不提供或与line_number相同，则只删除单行"
                        }
                    },
                    "required": ["file_path", "line_number"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_line_info",
                "description": "获取文件的行信息：总行数和按关键词搜索匹配的行号",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "要查看的文件路径"
                        },
                        "keyword": {
                            "type": "string",
                            "description": "可选，搜索包含该关键词的行号，用于快速定位内容位置"
                        }
                    },
                    "required": ["file_path"]
                }
            }
        }
    ]
    
    # 添加非定时器相关工具
    if if_not_timer:
        not_timer_tools = [  
            {
                "type": "function",
                "function": {
                    "name": "delete_file",
                    "description": "删除文件",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "要删除的文件路径"
                            }
                        },
                        "required": ["file_path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "once_after",
                    "description": "定时任务：在指定时间后执行一次",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "time": {
                                "type": "integer",
                                "description": "延迟时间（秒）"
                            },
                            "task": {
                                "type": "string",
                                "description": "任务描述"
                            }
                        },
                        "required": ["time", "task"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "interval",
                    "description": "定时任务：周期性执行",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "interval_seconds": {
                                "type": "integer",
                                "description": "时间间隔（秒）"
                            },
                            "interval_count": {
                                "type": "integer",
                                "description": "触发次数，-1 表示无限次"
                            },
                            "task": {
                                "type": "string",
                                "description": "任务描述"
                            }
                        },
                        "required": ["interval_seconds", "interval_count", "task"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "daily_at",
                    "description": "定时任务：每天在指定时间执行",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "hour": {
                                "type": "integer",
                                "description": "小时（0-23）"
                            },
                            "minute": {
                                "type": "integer",
                                "description": "分钟（0-59）"
                            },
                            "task": {
                                "type": "string",
                                "description": "任务描述"
                            }
                        },
                        "required": ["hour", "task"]
                    }
                }
            }
        ]
        tools.extend(not_timer_tools) 
    
    # 添加非子智能体相关工具
    if if_not_subagent:
        not_subagent_tools = [
            {
                "type": "function",
                "function": {
                    "name": "subagent_task",
                    "description": "发布给子智能体的任务，该工具会创建一个拥有独立记忆的智能体，子智能体会根据任务描述执行任务，执行完任务会返回任务报告",      
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task": {
                                "type": "string",
                                "description": "要执行的任务描述"
                            },
                            "role": {
                                "type": "string",
                                "description": "要执行任务的子智能体的描述,这个会强行插入上下文中,你可以引用role库里面的人设"
                            }
                        },
                        "required": ["task","role"]    
                    }
                }
            }
        ]
        tools.extend(not_subagent_tools)
    
    return tools    
