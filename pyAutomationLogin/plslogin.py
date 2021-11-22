# This Python file uses the following encoding: utf-8
import sys, os
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QSize, Slot,QProcess,QMetaObject
from PySide2 import QtCore
from PySide2.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QWidget,
    QTextEdit,
    QPushButton,
)
import time
import json
# import click_window_login_page_test
# import login_by_selenium
from pynput import keyboard

#pyside2-uic mainwindow.ui -o MainWindow.py
#pyside2-rcc resources.qrc -o resources_rc.py
#pyinstaller -w plslogin.py click_window_login_page_test.py --upx-dir="C:\Users\Administrator\Documents\pyAutomationLogin\upx-3.96-win64" --add-data="main.ui;." --add-data="id_pw.json;." --add-data="click_window_login_page_test.py;." --add-data="C:\Users\Administrator\packenv\Scripts\python.exe;."

#python -m venv packenv
#call packenv\scripts\activate.bat
# pip install PySide2 PyInstaller selenium uiautomation pynput
# pyinstaller -w plslogin.py click_window_login_page_test.py --add-data="main.ui;." --add-data="id_pw.json;." --add-data="click_window_login_page_test.py;." --add-data="C:\Users\Administrator\packenv\Scripts\python.exe;."

def getDefultJson():
    _path = os.path.join(os.path.dirname(__file__), "id_pw_user.json")
    if not os.path.exists(_path):
        _path = os.path.join(os.path.dirname(__file__), "id_pw.json")
    _str = ""
    if not os.path.exists(_path):
        return _str

    with open(_path, 'r', encoding='utf-8') as f:
        allLines = f.readlines()
        for s in allLines:
            _str += s
    return _str


class PLSLogin(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.p = None
        self.setDefaultConfig()
        self.isWillExit = False
        self._dict = json.dumps({})
        path = os.path.join(os.path.dirname(__file__), "main.ui")
        self.myWidget = QUiLoader().load(path, self);
#        self.myWidget = QUiLoader().load("main.ui", self);
        self.myWidget.textEdit_json.setPlainText(getDefultJson())
        self.myWidget.textEdit_log.setPlainText("点击start按钮，开始监听。停止按钮的快捷键是<F8>\n")
        self.myWidget.pushButton_start.clicked.connect(self.start_button_was_clicked)
        self.myWidget.pushButton_stop.clicked.connect(self.test_click)
        self.myWidget.pushButton_apply.clicked.connect(self.jsonApply)
        self.myWidget.pushButton_clear.clicked.connect(self.log_clear_click)
        self.processState(False)
        self.message(path)
        self.listener = keyboard.GlobalHotKeys({'<f8>': self.function_shortcut})
        self.listener.start() 
        self.start_button_was_clicked()

    def function_shortcut(self):
        self.message('stop shortkey <F8> clicked')
        QMetaObject.invokeMethod(self, 'test_click', QtCore.Qt.QueuedConnection)


    def processState(self, isStarted: bool):
        self.myWidget.pushButton_start.setEnabled(bool(1-isStarted))
        self.myWidget.pushButton_stop.setEnabled(isStarted)

    @Slot(str)
    def log_clear_click(self):
        self.myWidget.textEdit_log.setPlainText("")

    @Slot(str)
    def jsonApply(self):
        _path = os.path.join(os.path.dirname(__file__), "id_pw_user.json")
        self.message('写入路径' + _path)
        with open(_path, 'w') as f:
            f.write(self.myWidget.textEdit_json.toPlainText())

        if self.p is not None:
            self.test_click()
            self.start_button_was_clicked()

    def message(self, logs):
        self.myWidget.textEdit_log.append(logs)

#    @Slot(str)
    def test_click(self):
        if self.p is not None:
            self.p.close()

    @Slot(str)
    def start_button_was_clicked(self):
        if len(self._dict) == 0:
            self.message('id passord is empty, please click apply button')
            return

        if self.p is None:  # No process running.
            self.message("Executing process")
            self.p = QProcess()  # Keep a reference to the QProcess (e.g. on self) while it's running.
            self.p.readyReadStandardOutput.connect(self.handle_stdout)
            self.p.readyReadStandardError.connect(self.handle_stderr)
            self.p.stateChanged.connect(self.handle_state)
            self.p.finished.connect(self.process_finished)

            _path = os.path.join(os.path.dirname(__file__), "click_window_login_page_test.py")
            # _path = os.path.join(os.path.dirname(__file__), "login_by_selenium.py")
            # self.message('script path:%s' % _path)
            _p = os.path.join(os.path.dirname(__file__), "python.exe")
            # _p_e = os.path.join(os.path.dirname(__file__), "click_window_login_page_test.exe")
            _p_e = os.path.join(os.path.dirname(__file__), "login_by_selenium.exe")
            self.p.errorOccurred.connect(self.handle_err)
            self.message('exe:' + _p_e)
            self.message('py:' + _path)
            
            if os.path.exists(_p_e):
                self.message('运行 exe 文件')
                self.p.start(_p_e)
            elif os.path.exists(_path):
                self.message('运行 python 文件')
                self.p.start('python', [_path])
            else:
                self.message("退出进程，因为执行路径没有找到")

            self.processState(True)

        else:
            self.message("已经在查找中，忽略ing")

    def handle_err(self, err):
        # self.message(err)
        # err.Value()
        # print(type(err))
        # self.message(type(err))
        print(err)
        self.message('error occurred')
        self.process_finished()

    def handle_stderr(self):
        data = self.p.readAllStandardError()
        try:
            stderr = bytes(data).decode("utf8")
        except:
            stderr = bytes(data).decode("gbk")
        finally:
            self.message("err:" + stderr)

    def handle_stdout(self):
        data = self.p.readAllStandardOutput()
        try:
            stdout = bytes(data).decode("utf8")
        except:
            stdout = bytes(data).decode("gbk")
        finally:
            self.message(stdout)

    def handle_state(self, state):
        states = {
            QProcess.NotRunning: 'Not running',
            QProcess.Starting: 'Starting',
            QProcess.Running: 'Running',
        }
        state_name = states[state]
        self.message(f"State changed: {state_name}")


    def process_finished(self):
        self.message("Process finished.\n---------------\n")
        self.p = None
        self.processState(False)


    def setDefaultConfig(self):
        self.setWindowTitle("jimb My App")
        desktop = QApplication.desktop()
        self.setMinimumSize(QSize(600, 200))
        self.screenWidth = desktop.width() * 0.4
        self.screenHeight = desktop.height() * 0.6
        self.setGeometry(0, 0, self.screenWidth, self.screenHeight)


if __name__ == "__main__":
    app = QApplication([])
    window = PLSLogin()
    window.show()
    sys.exit(app.exec_())
