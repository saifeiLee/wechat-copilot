import rumps


class SuggestionWindow(rumps.App):
    def __init__(self):
        super().__init__("WeChat GPT Assistant")
        self.menu = ["Preferences", "About", "Quit"]

    def display_suggestion(self, suggestion):
        """Display the suggestion in a native macOS notification"""
        print(f"Displaying suggestion: {suggestion}")
        # rumps.notification(
        #     title="WeChat GPT Assistant", subtitle="Suggestion", message=suggestion
        # )
