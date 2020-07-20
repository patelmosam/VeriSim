from PySide2 import QtWidgets
# from PySide2.QtCore import Qt
from GUI.ui_mainWindow import Ui_MainWindow
from GUI.elements import *
from GUI.component_dialog import *

class VeriSimGUI(Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(VeriSimGUI, self).__init__()
        self.setupUi(self)
        self.ed.elements.append(OrElement('or'))
        self.ed.elements.append(AndElement('and'))
        self.ed.elements.append(NotElement('not'))
        # self.ed.elements.append(GeneralElement('example/verilog/ALU/add_sub.v', 'add_sub'))
        self.ed.elements.append(InputElement('i1', 1))
        self.ed.elements.append(InputElement('i2', 1))
        self.ed.elements.append(InputElement('i3', 1))
        self.ed.elements.append(MonitorElement('m1', 1))
        self.ed.elements.append(MonitorElement('m2', 1))
        self.ed.get_pins()
        # self.myStatus.showMessage("Status Bar Is Ready", 3000)
        # self.ed.elements(get_elem())
if __name__=='__main__':
    app = QtWidgets.QApplication()
    my_app = VeriSimGUI()
    # ed = SchematicEditor(my_app.frame)
    # my_app.setCentralWidget(ed)
    my_app.show()
    app.exec_()
