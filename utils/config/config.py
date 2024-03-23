import json

def load_config(config_file = "config/config.json"):
    """加载配置文件并返回配置字典"""
    with open(config_file, "r") as f:
        config = json.load(f)
    return config
