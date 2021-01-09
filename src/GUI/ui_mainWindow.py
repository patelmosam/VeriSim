# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainWindowdEqrqx.ui'
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
from src.GUI.schematicWindow import SchematicEditor
import src.GUI.icons_rc
from src.GUI.ui_dialog import Ui_Dialog
from src.GUI.add_component import Ui_AddDialog
from src.GUI.ui_new_component import Ui_NewDialog
import sys
from src.GUI.backend import *
from src.engine.engine import *
from src.database import add_to_db, query

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1106, 863)
        self.actionNew = QAction(MainWindow)
        self.actionNew.setObjectName(u"actionNew")
        icon = QIcon()
        icon.addFile(u":/images/images/disk.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionNew.setIcon(icon)
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        icon1 = QIcon()
        icon1.addFile(u":/images/images/printer.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionOpen.setIcon(icon1)
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionSave_As = QAction(MainWindow)
        self.actionSave_As.setObjectName(u"actionSave_As")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionUndo = QAction(MainWindow)
        self.actionUndo.setObjectName(u"actionUndo")
        self.actionRedo = QAction(MainWindow)
        self.actionRedo.setObjectName(u"actionRedo")
        self.actionCopy = QAction(MainWindow)
        self.actionCopy.setObjectName(u"actionCopy")
        self.actionPaste = QAction(MainWindow)
        self.actionPaste.setObjectName(u"actionPaste")
        self.actionCut = QAction(MainWindow)
        self.actionCut.setObjectName(u"actionCut")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionRun = QAction(MainWindow)
        self.actionRun.setObjectName(u"actionRun")
        icon2 = QIcon()
        icon2.addFile(u":/images/images/arrow-curve.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionRun.setIcon(icon2)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(5, 5, 5, 5)
        # self.textEdit = QTextEdit(self.frame)
        # self.textEdit.setObjectName(u"textEdit")
        self.ed = SchematicEditor(self.frame)
        self.ed.setObjectName(u"SchemanticEdit")

        self.gridLayout_3.addWidget(self.ed, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1106, 33))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        self.menuForm = QMenu(self.menubar)
        self.menuForm.setObjectName(u"menuForm")
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        self.menuSettings = QMenu(self.menubar)
        self.menuSettings.setObjectName(u"menuSettings")
        self.menuWindow = QMenu(self.menubar)
        self.menuWindow.setObjectName(u"menuWindow")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget_3 = QDockWidget(MainWindow)
        self.dockWidget_3.setObjectName(u"dockWidget_3")
        self.dockWidget_3.setAllowedAreas(Qt.AllDockWidgetAreas)
        self.dockWidgetContents_4 = QWidget()
        self.dockWidgetContents_4.setObjectName(u"dockWidgetContents_4")
        self.dockWidget_3.setWidget(self.dockWidgetContents_4)
        MainWindow.addDockWidget(Qt.LeftDockWidgetArea, self.dockWidget_3)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuForm.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuWindow.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addAction(self.actionExit)
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionRedo)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menuEdit.addAction(self.actionCut)
        self.menuHelp.addAction(self.actionAbout)
        self.toolBar.addAction(self.actionNew)
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addAction(self.actionRun)

        self.myStatus = QStatusBar()
        # self.myStatus.showMessage("Status Bar Is Ready", 3000)
        self.setStatusBar(self.myStatus)

        # self.actionWire = QAction(MainWindow)
        # self.actionWire.setObjectName(u"actionWire")
        # icon1 = QIcon()
        # icon1.addFile(u":/images/images/scissors.png", QSize(), QIcon.Normal, QIcon.Off)
        # self.actionWire.setIcon(icon1)
        # icon2 = QIcon()
        # icon2.addFile(u":/images/images/question.png", QSize(), QIcon.Normal, QIcon.Off)
        
        # self.toolBar.addAction(self.actionWire)

        self.actionDialog = QAction(MainWindow)
        self.actionDialog.setObjectName(u"components")
        icon3 = QIcon()
        icon3.addFile(u":/images/images/disk.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionDialog.setIcon(icon3)

        self.toolBar.addAction(self.actionDialog)

        self.actionDialog2 = QAction(MainWindow)
        self.actionDialog2.setObjectName(u"Addcomponents")
        icon4 = QIcon()
        icon4.addFile(u":/images/images/disk--pencil.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionDialog2.setIcon(icon4)

        self.toolBar.addAction(self.actionDialog2)

        self.actionBuild = QAction(MainWindow)
        self.actionBuild.setObjectName(u"Build")
        icon4 = QIcon()
        icon4.addFile(u":/images/images/ui-tab--plus.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionBuild.setIcon(icon4)

        self.toolBar.addAction(self.actionBuild)

        self.actionNewComponent = QAction(MainWindow)
        self.actionNewComponent.setObjectName(u"NewComponent")
        icon5 = QIcon()
        icon5.addFile(u":/images/images/edit-color.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionNewComponent.setIcon(icon5)

        self.toolBar.addAction(self.actionNewComponent)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

        # self.actionWire.triggered.connect(lambda : self.wire_mode(icon1, icon2))
        self.actionDialog.triggered.connect(lambda : self.startComponentDialog())
        self.actionDialog2.triggered.connect(lambda : self.startAddComponentDialog())
        self.actionBuild.triggered.connect(lambda : self.build())
        self.actionNewComponent.triggered.connect(lambda : self.startAddNewComponentDialog())
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionNew.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.actionSave_As.setText(QCoreApplication.translate("MainWindow", u"Save As", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.actionUndo.setText(QCoreApplication.translate("MainWindow", u"Undo", None))
        self.actionRedo.setText(QCoreApplication.translate("MainWindow", u"Redo", None))
        self.actionCopy.setText(QCoreApplication.translate("MainWindow", u"Copy", None))
        self.actionPaste.setText(QCoreApplication.translate("MainWindow", u"Paste", None))
        self.actionCut.setText(QCoreApplication.translate("MainWindow", u"Cut", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.actionRun.setText(QCoreApplication.translate("MainWindow", u"Run", None))
#if QT_CONFIG(tooltip)
        self.actionRun.setToolTip(QCoreApplication.translate("MainWindow", u"Run", None))
#endif // QT_CONFIG(tooltip)
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.menuForm.setTitle(QCoreApplication.translate("MainWindow", u"Form", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
        self.menuSettings.setTitle(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.menuWindow.setTitle(QCoreApplication.translate("MainWindow", u"Window", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

    # def wire_mode(self, icon1, icon2):
    #     if self.ed.wiring_mode:
    #         self.ed.wiring_mode = False
    #         self.actionWire.setIcon(icon1)
    #     else:
    #         self.ed.wiring_mode = True
    #         self.actionWire.setIcon(icon2)

    def startComponentDialog(self):
        dlg = ComponentDialog(self)
        dlg.exec_()
        element = get_module(dlg.selection,len(self.ed.elements)+1)
        if element is not None:
            self.ed.elements.append(element)
        else:
            file_path = query('Elements', 'file_path', 'name', dlg.selection)[0]
            element = make_module(file_path, len(self.ed.elements)+1)
            self.ed.elements.append(element)
        
    def startAddComponentDialog(self):
        dlg = AddComponentDialog(self)
        dlg.exec_()
        file_path = dlg.lineEdit.text()
        name = dlg.lineEdit_2.text()
        category = dlg.catagory
        if not file_path == '' and not name == '':
            add_to_db("Resource/elements.sqlite", name, file_path, category)
        
    def startAddNewComponentDialog(self):
        dlg = AddNewComponentDialog(self)
        dlg.exec_()
        file_path = dlg.lineEdit.text()
        element = make_module(file_path, len(self.ed.elements)+1)
        self.ed.elements.append(element)

    def build(self):
        elements, io_elements = get_elements(self.ed.elements)
        wires = get_wires(self.ed.wires)
        buses = get_buses(self.ed.buses)
        layout = Layout(elements, wires, buses, io_elements)
        e = engine(layout,None)
        e.create_module('test.v')
        self.myStatus.showMessage("Build sucessful", 3000)


class ComponentDialog(QDialog, Ui_Dialog):
    def __init__(self,parent):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Components")

class AddComponentDialog(QDialog, Ui_AddDialog):
    def __init__(self,parent):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Add Component")
        
class AddNewComponentDialog(QDialog, Ui_NewDialog):
    def __init__(self,parent):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("New Component")
