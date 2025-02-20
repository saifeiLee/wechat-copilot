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
)

from .util import get_window_title, get_chat_info


class WeChatReader:
    def __init__(self):
        self.app_element = None
        self.initialize_wechat()

    def initialize_wechat(self):
        wechat_apps = NSRunningApplication.runningApplicationsWithBundleIdentifier_(
            "com.tencent.xinWeChat"
        )
        if not wechat_apps:
            raise RuntimeError("WeChat is not running")

        wechat = wechat_apps[0]
        pid = wechat.processIdentifier()
        self.app_element = AXUIElementCreateApplication(pid)

    def get_current_chat(self):
        """Returns tuple of (chat_title, messages)"""
        windows = self._get_windows()
        target_window = self._find_chat_window(windows)
        if not target_window:
            return None, []

        return self._get_chat_info(target_window)

    def _get_windows(self):
        err, windows = AXUIElementCopyAttributeValue(
            self.app_element, kAXWindowsAttribute, None
        )
        return windows

    def _find_chat_window(self, windows):
        for window in windows:
            title = get_window_title(window)
            if title and ("微信" in title or "WeChat" in title):
                return window
        return None

    def _get_chat_info(self, window):
        chat_title, messages = get_chat_info(window)
        return chat_title, messages
