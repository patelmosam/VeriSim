from PySide2 import QtWidgets
from GUI.ui_mainWindow import Ui_MainWindow
from GUI.elements import *

class VeriSimGUI(Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(VeriSimGUI, self).__init__()
        self.setupUi(self)
        
if __name__=='__main__':
    app = QtWidgets.QApplication()
    my_app = VeriSimGUI()
    my_app.show()
    app.exec_()
