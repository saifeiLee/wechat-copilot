import os
from dotenv import load_dotenv


def load_settings():
    """Load application settings"""
    # Default settings
    settings = {
        "openai_api_key": "",
        "openai_base_url": "https://api.openai.com/v1",
        "shortcut": "cmd+shift+space",
    }

    # Load from config file
    config_path = os.path.expanduser("~/.wechat-copilot/config.env")
    if os.path.exists(config_path):
        load_dotenv(config_path)

        # Update settings from environment variables
        if os.getenv("OPENAI_API_KEY"):
            settings["openai_api_key"] = os.getenv("OPENAI_API_KEY")
        if os.getenv("OPENAI_BASE_URL"):
            settings["openai_base_url"] = os.getenv("OPENAI_BASE_URL")
        if os.getenv("SHORTCUT"):
            settings["shortcut"] = os.getenv("SHORTCUT")
    else:
        print(f"Warning: Config file not found at {config_path}")
        print("Please create it and add your OpenAI API key")

    # Validate required settings
    if not settings["openai_api_key"]:
        raise ValueError(
            "OPENAI_API_KEY is required. Please add it to ~/.wechat-copilot/config.env"
        )

    return settings
