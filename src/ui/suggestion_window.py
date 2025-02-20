import rumps
import os
import pyperclip


def show_notification(message):
    # 转义消息中的双引号，防止破坏 osascript 命令
    escaped_message = message.replace('"', '\\"')
    os.system(f'''
        osascript -e 'display notification "{escaped_message}" with title "WeChat GPT Assistant"'
    ''')
    # 自动复制消息到剪贴板
    pyperclip.copy(message)


class SuggestionWindow(rumps.App):
    def __init__(self):
        super().__init__("WeChat GPT Assistant")
        self.menu = ["Preferences", "About", "Quit"]

    def display_suggestion(self, suggestion):
        """Display the suggestion in a native macOS notification"""
        print(f"Displaying suggestion: {suggestion}")
        show_notification(suggestion)
