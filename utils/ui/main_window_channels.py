# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'utils\ui\files\MainWindow_Channels.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setDocumentMode(False)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.MainWidget = QtWidgets.QWidget(MainWindow)
        self.MainWidget.setStyleSheet("color: #EDEDED;\n"
"background-color: #212121;\n"
"line-height: 2;\n"
"")
        self.MainWidget.setObjectName("MainWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.MainWidget)
        self.gridLayout.setContentsMargins(1, 1, 1, 1)
        self.gridLayout.setObjectName("gridLayout")
        self.MessageField = QtWidgets.QLineEdit(self.MainWidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.MessageField.setFont(font)
        self.MessageField.setStyleSheet("color: #EDEDED;\n"
"background-color: #212121")
        self.MessageField.setFrame(False)
        self.MessageField.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.MessageField.setObjectName("MessageField")
        self.gridLayout.addWidget(self.MessageField, 1, 0, 1, 1)
        self.ViewWidget = QtWidgets.QWidget(self.MainWidget)
        self.ViewWidget.setObjectName("ViewWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.ViewWidget)
        self.horizontalLayout.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitter_2 = QtWidgets.QSplitter(self.ViewWidget)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.MessageView = QtWidgets.QTextBrowser(self.splitter_2)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.MessageView.setFont(font)
        self.MessageView.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.MessageView.setStyleSheet("")
        self.MessageView.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.MessageView.setFrameShadow(QtWidgets.QFrame.Plain)
        self.MessageView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.MessageView.setOpenExternalLinks(True)
        self.MessageView.setObjectName("MessageView")
        self.InfoPanel = QtWidgets.QWidget(self.splitter_2)
        self.InfoPanel.setMaximumSize(QtCore.QSize(200, 16777215))
        self.InfoPanel.setStyleSheet("")
        self.InfoPanel.setObjectName("InfoPanel")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.InfoPanel)
        self.verticalLayout.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtWidgets.QSplitter(self.InfoPanel)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.OnlineUsersView = QtWidgets.QTextBrowser(self.splitter)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.OnlineUsersView.setFont(font)
        self.OnlineUsersView.setFocusPolicy(QtCore.Qt.NoFocus)
        self.OnlineUsersView.setStyleSheet("")
        self.OnlineUsersView.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.OnlineUsersView.setFrameShadow(QtWidgets.QFrame.Plain)
        self.OnlineUsersView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.OnlineUsersView.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.OnlineUsersView.setOpenLinks(False)
        self.OnlineUsersView.setObjectName("OnlineUsersView")
        self.ChannelView = QtWidgets.QTextBrowser(self.splitter)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.ChannelView.setFont(font)
        self.ChannelView.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ChannelView.setStyleSheet("")
        self.ChannelView.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.ChannelView.setFrameShadow(QtWidgets.QFrame.Plain)
        self.ChannelView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.ChannelView.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.ChannelView.setOpenLinks(False)
        self.ChannelView.setObjectName("ChannelView")
        self.verticalLayout.addWidget(self.splitter)
        self.horizontalLayout.addWidget(self.splitter_2)
        self.gridLayout.addWidget(self.ViewWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.MainWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.MessageField.setPlaceholderText(_translate("MainWindow", ">"))
        self.MessageView.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.OnlineUsersView.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.ChannelView.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))

