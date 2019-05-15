# import sys
# from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction
# from PyQt5.QtGui import QIcon
# from PyQt5.QtCore import pyqtSlot

# class App(QMainWindow):

#     def __init__(self):
#     super().__init__()
#     self.title = 'PyQt5 menu - pythonspot.com'
#     self.left = 10
#     self.top = 10
#     self.width = 640
#     self.height = 400
#     self.initUI()
    
#     def initUI(self):
#         self.setWindowTitle(self.title)
#         self.setGeometry(self.left, self.top, self.width, self.height)

#         mainMenu = self.menuBar()
#         fileMenu = mainMenu.addMenu('File')
# editMenu = mainMenu.addMenu('Edit')
# viewMenu = mainMenu.addMenu('View')
# searchMenu = mainMenu.addMenu('Search')
# toolsMenu = mainMenu.addMenu('Tools')
# helpMenu = mainMenu.addMenu('Help')

# exitButton = QAction(QIcon('exit24.png'), 'Exit', self)
# exitButton.setShortcut('Ctrl+Q')
# exitButton.setStatusTip('Exit application')
# exitButton.triggered.connect(self.close)
# fileMenu.addAction(exitButton)

# self.show()

# if __name__ == '__main__':
# app = QApplication(sys.argv)
# ex = App()
# sys.exit(app.exec_())


from PyQt5 import QtWidgets

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, databaseFilePath, userFilePath):
        super(MainWindow,self).__init__()
        self.databaseFilePath = databaseFilePath
        self.userFilePath = userFilePath
        self.createUI()

    def changeFilePath(self):
        print('changeFilePath')
        # self.userFilePath = functions_classes.changeFilePath()
        # functions_classes.storeFilePath(self.userFilePath, 1)

    def createUI(self):
        self.setWindowTitle('Equipment Manager 0.3')
        menu = self.menuBar().addMenu('File')
        action = menu.addAction('Change File Path')
        action.triggered.connect(self.changeFilePath)   

if __name__ == '__main__':

    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow('some/path', 'some/other/path')
    window.show()
    window.setGeometry(500, 300, 300, 300)
    sys.exit(app.exec_())
