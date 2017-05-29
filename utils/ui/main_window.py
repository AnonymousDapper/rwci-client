# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'utils\ui\files\MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet("color: #EDEDED;\n"
"background-color: #212121;\n"
"line-height: 2;")
        self.MainWidget = QtWidgets.QWidget(MainWindow)
        self.MainWidget.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.MainWidget.setFont(font)
        self.MainWidget.setStyleSheet("")
        self.MainWidget.setObjectName("MainWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.MainWidget)
        self.gridLayout.setContentsMargins(2, 0, 2, 6)
        self.gridLayout.setObjectName("gridLayout")
        self.MessageField = QtWidgets.QLineEdit(self.MainWidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.MessageField.setFont(font)
        self.MessageField.setAcceptDrops(False)
        self.MessageField.setStyleSheet("color: #EDEDED;\n"
"background-color: #212121")
        self.MessageField.setFrame(False)
        self.MessageField.setObjectName("MessageField")
        self.gridLayout.addWidget(self.MessageField, 1, 0, 1, 1)
        self.MessageScroller = QtWidgets.QScrollArea(self.MainWidget)
        self.MessageScroller.setStyleSheet("QScrollBar:vertical {\n"
"    background: transparent;\n"
"    border: transparent;\n"
"    width: 15px;\n"
"    margin: 22px 0 22px 0;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical {\n"
"    background: #00bfa5;\n"
"    min-height: 20px;\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical {\n"
"    border: transparent;\n"
"    background: transparent;\n"
"    height: 20px;\n"
"    border-width: 2px 0 0 0;\n"
"    subcontrol-position: bottom;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::sub-line:vertical {\n"
"    border: transparent;\n"
"    background: transparent;\n"
"    height: 20px;\n"
"    border-width: 0 0 2px 0;\n"
"    subcontrol-position: top;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
"    border: transparent;\n"
"    width: 9px;\n"
"    height: 9px;\n"
"    background: transparent;\n"
"}\n"
"\n"
" QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"     background: #515151;\n"
" }")
        self.MessageScroller.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.MessageScroller.setFrameShadow(QtWidgets.QFrame.Plain)
        self.MessageScroller.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.MessageScroller.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.MessageScroller.setWidgetResizable(False)
        self.MessageScroller.setObjectName("MessageScroller")
        self.ScrollerContainer = QtWidgets.QWidget()
        self.ScrollerContainer.setGeometry(QtCore.QRect(0, 0, 796, 571))
        self.ScrollerContainer.setObjectName("ScrollerContainer")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.ScrollerContainer)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.MessageBrowser = QtWidgets.QTextBrowser(self.ScrollerContainer)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.MessageBrowser.setFont(font)
        self.MessageBrowser.setStyleSheet("color: #EDEDED;\n"
"background-color: #212121;\n"
"")
        self.MessageBrowser.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.MessageBrowser.setFrameShadow(QtWidgets.QFrame.Plain)
        self.MessageBrowser.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.MessageBrowser.setOpenExternalLinks(True)
        self.MessageBrowser.setObjectName("MessageBrowser")
        self.gridLayout_2.addWidget(self.MessageBrowser, 0, 0, 1, 1)
        self.MessageScroller.setWidget(self.ScrollerContainer)
        self.gridLayout.addWidget(self.MessageScroller, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.MainWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.MessageField.setPlaceholderText(_translate("MainWindow", ">"))
        self.MessageBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))

