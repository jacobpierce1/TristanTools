# #!/usr/bin/env python
# #-*- coding: utf-8 -*-

# import sys

# from PyQt5.QtWidgets import *
# from PyQt5 import QtCore


# class MyPopup(QWidget):
#     def __init__(self):
#         QWidget.__init__(self)

#     def paintEvent(self, e):
#         dc = QPainter(self)
#         dc.drawLine(0, 0, 100, 100)
#         dc.drawLine(100, 0, 0, 100)

# class MainWindow(QMainWindow):
#     def __init__(self, *args):
#         QMainWindow.__init__(self, *args)
#         self.cw = QWidget(self)
#         self.setCentralWidget(self.cw)
#         self.btn1 = QPushButton("Click me", self.cw)
#         self.btn1.setGeometry(QRect(0, 0, 100, 30))
#         self.connect(self.btn1, SIGNAL("clicked()"), self.doit)
#         self.w = None

#     def doit(self):
#         print( "Opening a new popup window..." )
#         self.w = MyPopup()
#         self.w.setGeometry(QRect(100, 100, 400, 200))
#         self.w.show()

# class App(QApplication):
#     def __init__(self, *args):
#         QApplication.__init__(self, *args)
#         self.main = MainWindow()
#         self.connect(self, SIGNAL("lastWindowClosed()"), self.byebye )
#         self.main.show()

#     def byebye( self ):
#         self.exit(0)

# def main(args):
#     global app
#     app = App(args)
#     app.exec_()

# if __name__ == "__main__":
#     main(sys.argv)



from PyQt5.QtWidgets import * 

class MainWindow( QWidget ):
    def __init__(self):
        super(MainWindow, self).__init__()

        btn = QPushButton('Click me!', self)
        btn.clicked.connect(self.onClick)

    def onClick(self):
        self.SW = SecondWindow()
        self.SW.show()

        # tmp = SecondWindow()
        # tmp.show() 
        
class SecondWindow( QWidget ):
    def __init__(self):
        super(SecondWindow, self).__init__()
        # lbl = QLabel('Second Window', self)

        layout = QHBoxLayout() 
        self.setLayout( layout ) 

        button = QPushButton( 'Test' ) 
        layout.addWidget( button ) 
        
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    MW = MainWindow()
    MW.show()
    sys.exit(app.exec_())
