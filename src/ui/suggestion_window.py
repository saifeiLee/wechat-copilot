import rumps
import os
import pyperclip


def show_notification(message):
    os.system(f"""
        osascript -e 'display notification "{message}" with title "WeChat GPT Assistant" with alert'
    """)
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
