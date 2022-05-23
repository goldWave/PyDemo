# coding = utf-8

import sys
import uiautomation as auto

auto.uiautomation.SetGlobalSearchTimeout(2)  # 设置全局搜索超时 15

_dir = r'C:\Users\Administrator\AppData\Local\PRISMLiveStudio\PRISMLauncher.exe'

# 循环打开关闭prism
def oepnAndClosePrism

    index = 0
    while True:
        print("index", index)
        _root = auto.GetRootControl()
        vsWindow=_root.WindowControl(searchDepth=1,AutomationId='VisualStudioMainWindow')
        vsWindow.SetActive()
        a = vsWindow.PaneControl(Name="ToolBarDockTop").ToolBarControl(ClassName="ToolBar")
        _runBtn =  a.SplitButtonControl(AutomationId="PART_FocusTarget", Name="调试目标")

        isOk = False
        for x in range(10):
            print("check run btn index: ", x)
            if (_runBtn.IsEnabled):
                isOk = True
                break
            time.sleep(6)

        print("click run btn isOk:", isOk)
        _runBtn.Click()

        
        window=_root.WindowControl(searchDepth=1,Name='Prism Live Studio')
        
        window.Exists(60,5)
        time.sleep(3)
        window.Refind()
        btn = window.ButtonControl(AutomationId="PLSMainView.titleBar.close")
        btn.Click(simulateMove=True)
        # isOk = False
        # for x in range(10):
        #     window.Refind()
        #     if (btn.Exists(0,0)):
        #         isOk = True
        #         break
        #     time.sleep(6)

        # print("click close btn isOk:", isOk)
        # btn.Refind()
        # btn.Click()

        index += 1



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