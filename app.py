from PySide2 import QtWidgets
from src.GUI.ui_mainWindow import Ui_MainWindow
from src.database import Init_db

class VeriSimGUI(Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(VeriSimGUI, self).__init__()
        self.setupUi(self)
        Init_db("Resource/elements.sql", "Resource/elements.sqlite")
        
if __name__=='__main__':
    app = QtWidgets.QApplication()
    my_app = VeriSimGUI()
    my_app.show()
    app.exec_()
