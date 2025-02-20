import rumps
import os


def show_notification(message):
    os.system(f"""
        osascript -e 'display notification "{message}" with title "WeChat GPT Assistant" with alert'
    """)


class SuggestionWindow(rumps.App):
    def __init__(self):
        super().__init__("WeChat GPT Assistant")
        self.menu = ["Preferences", "About", "Quit"]

    def display_suggestion(self, suggestion):
        """Display the suggestion in a native macOS notification"""
        print(f"Displaying suggestion: {suggestion}")
        show_notification(suggestion)
