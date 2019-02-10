#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtWidgets


class LoginDlg(QtWidgets.QDialog):

    def __init__(self):
        super(LoginDlg, self).__init__()

        self.password = QtWidgets.QLineEdit()
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        layout = QtWidgets.QFormLayout()
        layout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        layout.addRow('Password', self.password)
        layout.addWidget(self.button_box)

        self.setLayout(layout)
        self.setWindowTitle("Login")
        self.setMinimumWidth(350)


class MyWindow(QtWidgets.QWidget):

    def __init__(self):
        super(MyWindow, self).__init__()

        self.edit = QtWidgets.QLineEdit()
        button = QtWidgets.QPushButton("Get input from dialog")
        button.clicked.connect(self.get_login)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.edit)
        layout.addWidget(button)
        self.setLayout(layout)

    def get_login(self):
        login = LoginDlg()
        if login.exec_():
            self.edit.setText(login.password.text())


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
