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


def print_all_attributes(element):
    try:
        # 获取所有属性名称
        err, attributes = AXUIElementCopyAttributeNames(element, None)
        if err != 0:
            print(f"获取属性名称失败，错误码: {err}")
            return

        print("\n=== 元素属性列表 ===")
        for attr in attributes:
            try:
                err, value = AXUIElementCopyAttributeValue(element, attr, None)
                print(f"属性: {attr}")
                print(f"值: {value}")
                print("---")
            except Exception as e:
                print(f"读取属性 {attr} 失败: {e}")
                print("---")
    except Exception as e:
        print(f"获取属性列表失败: {e}")


def get_window_title(window):
    try:
        idx, title = AXUIElementCopyAttributeValue(window, kAXTitleAttribute, None)
        if isinstance(title, tuple):
            title = title[1]
            return title
        elif isinstance(title, str):
            return title
        else:
            return str(title)
    except Exception as e:
        print("获取窗口标题出错:", e)
        return None


def find_element_by_role(parent, role_name):
    try:
        _, children = AXUIElementCopyAttributeValue(parent, kAXChildrenAttribute, None)
        if not children:
            return None

        for child in children:
            # 获取元素的角色信息
            _, role = AXUIElementCopyAttributeValue(child, kAXRoleAttribute, None)
            _, subrole = AXUIElementCopyAttributeValue(child, kAXSubroleAttribute, None)

            # 获取元素的描述信息（可能包含类名）
            _, description = AXUIElementCopyAttributeValue(
                child, kAXDescriptionAttribute, None
            )

            # 打印调试信息
            print(
                f"Element - Role: {role}, Subrole: {subrole}, Description: {description}"
            )

            # 检查是否匹配目标类型
            if (description and role_name in description) or (
                role and role_name in role
            ):
                return child

        return None
    except Exception as e:
        print(f"查找元素出错: {e}")
        return None


def get_chat_info(window):
    title = None
    messages = []
    try:
        # 查找 MMSplitView
        split_view = find_element_by_role(window, "AXSplitGroup")
        if not split_view:
            print("未找到 MMSplitView")
            return None

        # 查找 MMChatDetailSplitView
        chat_detail_view = find_element_by_role(split_view, "AXSplitGroup")
        if not chat_detail_view:
            print("未找到 MMChatDetailSplitView")
            return None

        # 查找标题文本元素
        _, children = AXUIElementCopyAttributeValue(
            chat_detail_view, kAXChildrenAttribute, None
        )
        if not children:
            return None

        for child in children:
            _, role = AXUIElementCopyAttributeValue(child, kAXRoleAttribute, None)
            print(f"child role: {role}")
            if isinstance(role, str) and "text" in role.lower():
                _, value = AXUIElementCopyAttributeValue(child, kAXValueAttribute, None)
                title = value
                break

        print("获取聊天消息列表")
        chat_message_view = find_element_by_role(chat_detail_view, "AXScrollArea")
        if not chat_message_view:
            print("未找到 AXScrollArea")
            return None

        messages = get_chat_messages(chat_message_view)

        return title, messages
    except Exception as e:
        print(f"获取聊天标题出错: {e}")
        return None


def get_chat_messages(view):
    messages = []
    try:
        _, children = AXUIElementCopyAttributeValue(view, kAXChildrenAttribute, None)
        if not children:
            print("未找到 chat_message_view 的子元素")
            return []

        table_view = find_element_by_role(view, "AXTable")
        if not table_view:
            print("未找到 AXTable")
            return []

        _, children = AXUIElementCopyAttributeValue(
            table_view, kAXChildrenAttribute, None
        )
        if not children:
            print("未找到 AXTable 的子元素")
            return []

        for child in children:
            _, role = AXUIElementCopyAttributeValue(child, kAXRoleAttribute, None)

            if role == "AXRow":
                _, children_ax_row = AXUIElementCopyAttributeValue(
                    child, kAXChildrenAttribute, None
                )
                if not children_ax_row:
                    print("未找到 AXRow 的子元素")
                    break
                for ax_row_child in children_ax_row:
                    _, role = AXUIElementCopyAttributeValue(
                        ax_row_child, kAXRoleAttribute, None
                    )
                    print(f"AXRow 的子元素 role: {role}")
                    if role == "AXCell":
                        _, value = AXUIElementCopyAttributeValue(
                            ax_row_child, kAXValueAttribute, None
                        )
                        print(f"AXRow 的子元素 value: {value}")
                        # 找AXCell的子元素
                        _, children_ax_cell = AXUIElementCopyAttributeValue(
                            ax_row_child, kAXChildrenAttribute, None
                        )
                        if not children_ax_cell:
                            print("未找到 AXRow 的子元素的子元素")
                            break
                        for ax_cell_child in children_ax_cell:
                            _, child_role = AXUIElementCopyAttributeValue(
                                ax_cell_child, kAXRoleAttribute, None
                            )
                            _, child_value = AXUIElementCopyAttributeValue(
                                ax_cell_child, kAXValueAttribute, None
                            )
                            _, child_desc = AXUIElementCopyAttributeValue(
                                ax_cell_child, kAXDescriptionAttribute, None
                            )
                            _, child_title = AXUIElementCopyAttributeValue(
                                ax_cell_child, kAXTitleAttribute, None
                            )

                            print(
                                f"消息组件 - Role: {child_role}, Description: {child_desc}, Value: {child_value}, Title: {child_title}"
                            )
                            if child_title:
                                messages.append(child_title)
                            # print_all_attributes(ax_cell_child)

        return messages
    except Exception as e:
        print(f"获取聊天消息出错: {e}")
        return []


def get_wechat_information():
    # 获取微信应用实例
    wechat_apps = NSRunningApplication.runningApplicationsWithBundleIdentifier_(
        "com.tencent.xinWeChat"
    )
    if not wechat_apps:
        print("微信未运行")
        return

    wechat = wechat_apps[0]
    pid = wechat.processIdentifier()

    # 创建 Accessibility 元素
    app_element = AXUIElementCreateApplication(pid)

    # 获取所有窗口
    windows = []
    try:
        err, windows = AXUIElementCopyAttributeValue(
            app_element, kAXWindowsAttribute, None
        )

    except Exception as e:
        print("无法获取窗口:", e)
        return

    # 遍历窗口查找聊天窗口
    target_window = None
    for window in windows:
        try:
            title = get_window_title(window)
            print(f"应用窗口标题: {title}")
            if title and ("微信" in title or "WeChat" in title):
                target_window = window
                break
        except Exception as e:
            print("遍历窗口出错:", e)
    chat_title, messages = get_chat_info(target_window)
    print(f"聊天标题(对象): {chat_title}")
    print(f"聊天消息(对象): {messages}")
    # 定位消息滚动区域（需根据实际 UI 调整）


if __name__ == "__main__":
    # wechat = MacWeChatAccessibility()
    # windows = wechat.get_wechat_windows()
    # print(windows)
    # content = wechat.get_chat_content()
    # print(f"当前聊天内容: {content}")

    get_wechat_information()
