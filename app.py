from PySide2 import QtWidgets
# from PySide2.QtCore import Qt
from GUI.ui_mainWindow import Ui_MainWindow
from GUI.elements import *

class VeriSimGUI(Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(VeriSimGUI, self).__init__()
        self.setupUi(self)
        
        self.ed.get_pins()
        # self.myStatus.showMessage("Status Bar Is Ready", 3000)
        # self.ed.elements(get_elem())
if __name__=='__main__':
    app = QtWidgets.QApplication()
    my_app = VeriSimGUI()
    my_app.show()
    app.exec_()
