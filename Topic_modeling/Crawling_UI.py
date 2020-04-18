# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Crawling_UI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(643, 188)
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 90, 611, 81))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtWidgets.QSplitter(self.layoutWidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.label = QtWidgets.QLabel(self.splitter)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.le_keyword = QtWidgets.QLineEdit(self.splitter)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.le_keyword.setFont(font)
        self.le_keyword.setObjectName("le_keyword")
        self.btn_crawling = QtWidgets.QPushButton(self.splitter)
        self.btn_crawling.setObjectName("btn_crawling")
        self.verticalLayout.addWidget(self.splitter)
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(10, 10, 371, 63))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.le_clientId = QtWidgets.QLineEdit(self.widget)
        self.le_clientId.setObjectName("le_clientId")
        self.verticalLayout_3.addWidget(self.le_clientId)
        self.le_clientSecret = QtWidgets.QLineEdit(self.widget)
        self.le_clientSecret.setObjectName("le_clientSecret")
        self.verticalLayout_3.addWidget(self.le_clientSecret)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.widget1 = QtWidgets.QWidget(Dialog)
        self.widget1.setGeometry(QtCore.QRect(390, 40, 236, 28))
        self.widget1.setObjectName("widget1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_4 = QtWidgets.QLabel(self.widget1)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.le_pagecount = QtWidgets.QLineEdit(self.widget1)
        self.le_pagecount.setObjectName("le_pagecount")
        self.horizontalLayout_2.addWidget(self.le_pagecount)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "네이버기사수집"))
        self.label.setText(_translate("Dialog", "키워드"))
        self.btn_crawling.setText(_translate("Dialog", "수집시작"))
        self.label_2.setText(_translate("Dialog", "Client Id"))
        self.label_3.setText(_translate("Dialog", "Client Secret"))
        self.label_4.setText(_translate("Dialog", "검색페이지수"))

