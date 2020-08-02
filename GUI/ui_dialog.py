# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialogDWKaOD.ui'
##
## Created by: Qt User Interface Compiler version 5.15.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *
from Resource.database import query

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(854, 655)
        self.selection = None
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(257, 201))
        self.frame.setMaximumSize(QSize(257, 201))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)

        self.gridLayout.addWidget(self.frame, 0, 2, 1, 2)

        self.frame_4 = QFrame(Dialog)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(257, 381))
        self.frame_4.setMaximumSize(QSize(257, 381))
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)

        self.gridLayout.addWidget(self.frame_4, 1, 2, 1, 2)

        self.pushButton = QPushButton(Dialog)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMaximumSize(QSize(114, 36))

        self.gridLayout.addWidget(self.pushButton, 2, 2, 1, 1)

        self.pushButton_2 = QPushButton(Dialog)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setMaximumSize(QSize(114, 36))
        self.pushButton_2.clicked.connect(lambda:self.get_selection())

        self.gridLayout.addWidget(self.pushButton_2, 2, 3, 1, 1)

        self.listWidget = QListWidget(Dialog)
        # QListWidgetItem(self.listWidget)
        # QListWidgetItem(self.listWidget)
        # QListWidgetItem(self.listWidget)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setMinimumSize(QSize(284, 630)) 

        # itemG, widget, GateButton = self.get_item('Gates')
        # self.listWidget.addItem(itemG)
        # self.listWidget.setItemWidget(itemG, widget)
        # GateButton.clicked.connect(lambda : self.set_gates_list())

        # itemI, widget, InputButton = self.get_item('Inputs')
        # self.listWidget.addItem(itemI)
        # self.listWidget.setItemWidget(itemI, widget)

        # itemO, widget, OutputButton = self.get_item('Output')
        # self.listWidget.addItem(itemO)
        # self.listWidget.setItemWidget(itemO, widget)

        self.gridLayout.addWidget(self.listWidget, 0, 0, 3, 1)

        self.listWidget_2 = QListWidget(Dialog)
        self.listWidget_2.setObjectName(u"listWidget_2")
        self.listWidget_2.setMinimumSize(QSize(283, 630))

        self.gridLayout.addWidget(self.listWidget_2, 0, 1, 3, 1)

        self.listWidget.itemClicked.connect(self._handleClick)

        self.listWidget_2.itemClicked.connect(self._get_selection)
        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.pushButton.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
        self.pushButton_2.setText(QCoreApplication.translate("Dialog", u"OK", None))

        self.listWidget.addItems(list(dict.fromkeys(query('Elements', 'category'))))

        # __sortingEnabled = self.listWidget.isSortingEnabled()
        # self.listWidget.setSortingEnabled(False)
        # ___qlistwidgetitem = self.listWidget.item(0)
        # ___qlistwidgetitem.setText(QCoreApplication.translate("Dialog", u"Gates", None));
        # ___qlistwidgetitem1 = self.listWidget.item(1)
        # ___qlistwidgetitem1.setText(QCoreApplication.translate("Dialog", u"Inputs", None));
        # ___qlistwidgetitem2 = self.listWidget.item(2)
        # ___qlistwidgetitem2.setText(QCoreApplication.translate("Dialog", u"Outputs", None));
        # self.listWidget.setSortingEnabled(__sortingEnabled)

    # retranslateUi

    def _handleClick(self, item):
        components = query('Elements','*')
        types = list(dict.fromkeys(query('Elements', 'category'))) 
        elements_data = {}

        for _type in types:
            elements_data[_type] = query('Elements', 'name', 'category', _type)

        self.clear_items()
        self.listWidget_2.addItems(elements_data[item.text()])
        

    def clear_items(self):
        item = 1
        while item is not None:
            item = self.listWidget_2.takeItem(0)

    def _get_selection(self, item):
        self.selection = item.text()

    def get_selection(self):
        # print(self.selection)
        self.close()
        

