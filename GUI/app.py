from PySide2 import QtWidgets
# from PySide2.QtCore import Qt
from ui_mainWindow import Ui_MainWindow
from elements import *

class VeriSimGUI(Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(VeriSimGUI, self).__init__()
        self.setupUi(self)
        self.ed.elements.append(OrElement())
        self.ed.elements.append(AndElement())
        self.ed.elements.append(NotElement())
        self.ed.elements.append(GeneralElement(4,4))
        # self.ed.elements.append(NotElement())
        # self.ed.wiring_mode = True
        # self.ed.paintEvent()
        # self.myStatus.showMessage("Status Bar Is Ready", 3000)

if __name__=='__main__':
    app = QtWidgets.QApplication()
    my_app = VeriSimGUI()
    # ed = SchematicEditor(my_app.frame)
    # my_app.setCentralWidget(ed)
    my_app.show()
    app.exec_()
