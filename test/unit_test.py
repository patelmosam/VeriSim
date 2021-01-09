import sys
sys.path.insert(1, '/home/mosam/Matrix/Nutron/Dev/VeriSim/')

import unittest
from PySide2 import QtWidgets
from GUI.elements import *
# from Resource.database import Init_db
from app import VeriSimGUI

class InitTest(unittest.TestCase):
    
    def test_layout1(self):
        app = QtWidgets.QApplication()
        my_app = VeriSimGUI()
        my_app.setupUi(my_app)

        my_app.ed.elements.append(AndElement('m1'))
        my_app.ed.elements.append(OrElement('m2'))
        my_app.ed.elements.append(InputElement('m3',1))
        my_app.ed.elements.append(InputElement('m4',1))
        my_app.ed.elements.append(InputElement('m5',1))
        my_app.ed.elements.append(MonitorElement('m6',1))

        conn = connection(my_app.ed.elements[2],0,my_app.ed.elements[0],0)
        my_app.ed.wires.append(WireElement(conn, []))

        conn = connection(my_app.ed.elements[3],0,my_app.ed.elements[0],1)
        my_app.ed.wires.append(WireElement(conn, []))

        conn = connection(my_app.ed.elements[4],0,my_app.ed.elements[1],1)
        my_app.ed.wires.append(WireElement(conn, []))

        conn = connection(my_app.ed.elements[0],2,my_app.ed.elements[1],0)
        my_app.ed.wires.append(WireElement(conn, []))

        conn = connection(my_app.ed.elements[1],2,my_app.ed.elements[5],0)
        my_app.ed.wires.append(WireElement(conn, []))

        my_app.build()

        # my_app.show()
        # app.exec_()
        with open("test.v") as file:
            file1 = file.read()
        with open("test/sample.v") as file:
            file2 = file.read()
        self.assertEqual(file1, file2)
        

if __name__ == '__main__':
    unittest.main()
   