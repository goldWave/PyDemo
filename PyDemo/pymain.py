# This Python file uses the following encoding: utf-8
import sys, os
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QMainWindow

class PyMain(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        #这里获取到formmain.ui 的绝对路径
        path = os.path.join(os.path.dirname(__file__), "formmain.ui")
        #将路径传入QUiLoader里面，第二个参数self代表是将PyMain作为ui文件的父控件来进行加载。
        self.myWidget = QUiLoader().load(path, self);

if __name__ == "__main__":
    app = QApplication([])
    window = PyMain()
    window.show()
    sys.exit(app.exec_())
