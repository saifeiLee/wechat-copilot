import time
from AppKit import NSRunningApplication
from ApplicationServices import (
    AXUIElementCreateApplication,
    kAXWindowsAttribute,
    kAXTitleAttribute,
    kAXChildrenAttribute,
    kAXRoleAttribute,
    kAXValueAttribute,
    AXUIElementCopyAttributeValue,
    kAXSubroleAttribute,
    kAXDescriptionAttribute,
    AXUIElementCopyAttributeNames,
)
import asyncio
from accessibility.wechat_reader import WeChatReader
from hotkey.shortcut_manager import ShortcutManager
from ai.gpt_client import GPTClient
from ui.suggestion_window import SuggestionWindow
from config.settings import load_settings


class WeChatGPTAssistant:
    def __init__(self):
        self.settings = load_settings()
        self.wechat_reader = WeChatReader()
        self.gpt_client = GPTClient(
            self.settings.get("openai_api_key"),
            self.settings.get("openai_base_url"),
        )
        self.ui = SuggestionWindow()
        self.shortcut_manager = ShortcutManager(self.handle_shortcut)

    def handle_shortcut(self):
        """Handle shortcut press"""
        try:
            # Get current chat
            chat_title, messages = self.wechat_reader.get_current_chat()
            if not messages:
                self.ui.display_suggestion("No messages found in current chat")
                return

            # Get suggestion from GPT
            suggestion = self.gpt_client.get_suggestion(messages)

            # Display suggestion
            self.ui.display_suggestion(suggestion)
        except Exception as e:
            self.ui.display_suggestion(f"Error: {str(e)}")

    def run(self):
        """Start the application"""
        self.shortcut_manager.register_shortcut(self.settings.get("shortcut"))
        self.shortcut_manager.start()
        self.ui.run()


def main():
    """Entry point for the command-line script"""
    app = WeChatGPTAssistant()
    app.run()


if __name__ == "__main__":
    main()
