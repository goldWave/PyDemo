# coding = utf-8

import sys
import uiautomation as auto

auto.uiautomation.SetGlobalSearchTimeout(2)  # 设置全局搜索超时 15


if __name__ == '__main__':
    window=auto.WindowControl(searchDepth=1,Name='Prism Live Studio')
    window.SetActive()
    help_btn = window.Control(AutomationId='PLSMainView.body.rightArea.help')
    help_btn.Click()

    help_menu = auto.WindowControl(AutomationId='PLSMainView.helpMenu')
    print(help_menu)
    print("\n")
    web_button = help_menu.MenuItemControl(ClassName="QWidgetAction")
    print(web_button)
    auto.EnumAndLogControl(web_button)
  
    # web_button.Click()
    # help_menu.chileCoo