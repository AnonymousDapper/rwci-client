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
"line-height: 2;")
        self.MainWidget.setObjectName("MainWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.MainWidget)
        self.verticalLayout.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ViewWidget = QtWidgets.QWidget(self.MainWidget)
        self.ViewWidget.setObjectName("ViewWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.ViewWidget)
        self.horizontalLayout.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ViewSplitter = QtWidgets.QSplitter(self.ViewWidget)
        self.ViewSplitter.setOrientation(QtCore.Qt.Horizontal)
        self.ViewSplitter.setObjectName("ViewSplitter")
        self.MessageScroller = QtWidgets.QScrollArea(self.ViewSplitter)
        self.MessageScroller.setMaximumSize(QtCore.QSize(16777215, 16777215))
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
        self.MessageScroller.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.MessageScroller.setWidgetResizable(True)
        self.MessageScroller.setObjectName("MessageScroller")
        self.MessageScrollContainer = QtWidgets.QWidget()
        self.MessageScrollContainer.setGeometry(QtCore.QRect(0, 0, 566, 573))
        self.MessageScrollContainer.setObjectName("MessageScrollContainer")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.MessageScrollContainer)
        self.gridLayout_2.setContentsMargins(1, 1, 1, 1)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.MessageView = QtWidgets.QTextBrowser(self.MessageScrollContainer)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.MessageView.setFont(font)
        self.MessageView.setStyleSheet("color: #EDEDED;\n"
"background-color: #212121;\n"
"")
        self.MessageView.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.MessageView.setFrameShadow(QtWidgets.QFrame.Plain)
        self.MessageView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.MessageView.setOpenExternalLinks(True)
        self.MessageView.setObjectName("MessageView")
        self.gridLayout_2.addWidget(self.MessageView, 0, 0, 1, 1)
        self.MessageScroller.setWidget(self.MessageScrollContainer)
        self.ChannelScroller = QtWidgets.QScrollArea(self.ViewSplitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ChannelScroller.sizePolicy().hasHeightForWidth())
        self.ChannelScroller.setSizePolicy(sizePolicy)
        self.ChannelScroller.setMaximumSize(QtCore.QSize(225, 16777215))
        self.ChannelScroller.setStyleSheet("QScrollBar:vertical {\n"
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
        self.ChannelScroller.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.ChannelScroller.setFrameShadow(QtWidgets.QFrame.Plain)
        self.ChannelScroller.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.ChannelScroller.setWidgetResizable(True)
        self.ChannelScroller.setObjectName("ChannelScroller")
        self.ChannelScrollContainer = QtWidgets.QWidget()
        self.ChannelScrollContainer.setGeometry(QtCore.QRect(0, 0, 225, 573))
        self.ChannelScrollContainer.setObjectName("ChannelScrollContainer")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.ChannelScrollContainer)
        self.verticalLayout_2.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.OnlineUsersView = QtWidgets.QTextBrowser(self.ChannelScrollContainer)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.OnlineUsersView.setFont(font)
        self.OnlineUsersView.setStyleSheet("color: #EDEDED;\n"
"background-color: #212121;\n"
"")
        self.OnlineUsersView.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.OnlineUsersView.setFrameShadow(QtWidgets.QFrame.Plain)
        self.OnlineUsersView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.OnlineUsersView.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.OnlineUsersView.setOpenLinks(False)
        self.OnlineUsersView.setObjectName("OnlineUsersView")
        self.verticalLayout_2.addWidget(self.OnlineUsersView)
        self.ChannelView = QtWidgets.QTextBrowser(self.ChannelScrollContainer)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.ChannelView.setFont(font)
        self.ChannelView.setStyleSheet("color: #EDEDED;\n"
"background-color: #212121;\n"
"")
        self.ChannelView.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.ChannelView.setFrameShadow(QtWidgets.QFrame.Plain)
        self.ChannelView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.ChannelView.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.ChannelView.setOpenLinks(False)
        self.ChannelView.setObjectName("ChannelView")
        self.verticalLayout_2.addWidget(self.ChannelView)
        self.ChannelScroller.setWidget(self.ChannelScrollContainer)
        self.horizontalLayout.addWidget(self.ViewSplitter)
        self.verticalLayout.addWidget(self.ViewWidget)
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
        self.verticalLayout.addWidget(self.MessageField)
        self.MessageField.raise_()
        self.ViewWidget.raise_()
        MainWindow.setCentralWidget(self.MainWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.MessageView.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.ChannelView.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.MessageField.setPlaceholderText(_translate("MainWindow", ">"))

