# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'designerJACWKH.ui'
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
from src.database import query

class Ui_AddDialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(558, 344)
        self.catagory = 'Gates'
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.lineEdit = QLineEdit(Dialog)
        self.lineEdit.setObjectName(u"lineEdit")

        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)

        self.BrowseButton = QPushButton(Dialog)
        self.BrowseButton.setObjectName(u"BrowseButton")

        self.gridLayout.addWidget(self.BrowseButton, 0, 2, 1, 1)

        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.lineEdit_2 = QLineEdit(Dialog)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.gridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 1)

        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.comboBox = QComboBox(Dialog)
        self.comboBox.setObjectName(u"comboBox")
        category = list(dict.fromkeys(query('Elements', 'category')))
        category.append('Add new')
        self.comboBox.insertItems(0, category)

        self.gridLayout.addWidget(self.comboBox, 2, 1, 1, 1)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 2)

        self.BrowseButton.clicked.connect(lambda : self.openFileNameDialog())

        self.comboBox.currentIndexChanged.connect(self._get_catagory)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"File Path", None))
        self.BrowseButton.setText(QCoreApplication.translate("Dialog", u"Browse", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Name", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"category", None))
    # retranslateUi

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Open File", "","Verilog Files (*.v)", options=options)
        if fileName:
            if fileName is not None:
                self.lineEdit.insert(fileName)

    def _get_catagory(self, item):
        if self.comboBox.currentText() == 'Add new':
            self.get_new_category()
        self.catagory = self.comboBox.currentText()
        
    def get_new_category(self):
        text, ok = QInputDialog.getText(self, 'New Category', 'Enter the new category:')
        if ok:
            count = self.comboBox.count()
            self.comboBox.removeItem(count-1)
            self.comboBox.insertItem(count-1, str(text))   


            
