import sys
 
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton, QVBoxLayout 
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore


 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
 
import random
 
class App( QWidget ):
 
    def __init__(self):
        super().__init__()
        # self.left = 10
        # self.top = 10
        # self.title = 'PyQt5 matplotlib example - pythonspot.com'
        # self.width = 640
        # self.height = 400
        self.initUI()
 
    def initUI(self):
        # self.setWindowTitle(self.title)
        # self.setGeometry(self.left, self.top, self.width, self.height)
 
        # m = PlotCanvas(self, width=5, height=4)
        # m.move(0,0)

        layout = QVBoxLayout()


        figure = Figure()
        ax = figure.add_subplot( 111 )
        data = [random.random() for i in range(25)]
        ax.plot(data, 'r-')
        ax.set_title('PyQt Matplotlib Example')
        # self.draw()
        
        # m = FixedAspectFigureCanvas( figure ) 
        m = FigureCanvas( figure ) 
        m.draw() 
        
        button = QPushButton('PyQt5 button' )
        button.setToolTip('This s an example button')
        # button.move(500,0)
        button.resize(140,100)

        layout.addWidget( m )
        layout.addWidget( button )

        self.setLayout( layout ) 
        
        
        self.show()



def adjustFigAspect(fig,aspect=1):
    '''
    Adjust the subplot parameters so that the figure has the correct
    aspect ratio.
    '''
    xsize,ysize = fig.get_size_inches()
    minsize = min(xsize,ysize)
    xlim = .4*minsize/xsize
    ylim = .4*minsize/ysize
    if aspect < 1:
        xlim *= aspect
    else:
        ylim /= aspect
    fig.subplots_adjust(left=.5-xlim,
                        right=.5+xlim,
                        bottom=.5-ylim,
                        top=.5+ylim)


    
class FixedAspectFigureCanvas( FigureCanvas ) :

    def __init__( self, figure ) :
        super().__init__( figure )
        # sizePolicy = QSizePolicy( QSizePolicy.Preferred, QSizePolicy.Preferred )
        sizePolicy = QSizePolicy( QSizePolicy.Maximum, QSizePolicy.Maximum )
        sizePolicy.setHeightForWidth( True )
        self.setSizePolicy(sizePolicy)

    def heightForWidth( self, width ) :
        print( 'computing width' )
        return width 

    def sizeHint( self ) :
        return QtCore.QSize( 700, 700 ) 



    
# # class PlotCanvas(FigureCanvas):
# class PlotCanvas( FixedAspectFigureCanvas ) :

#     def __init__(self, parent=None ) : # , width=5, height=4, dpi=100):

#         fig = Figure(figsize=(3, 3))

#         self.axes = fig.add_subplot(111)
 
#         FigureCanvas.__init__(self, fig)

#         self.setParent(parent)
 
#         FigureCanvas.setSizePolicy(self,
#                 QSizePolicy.Expanding,
#                 QSizePolicy.Expanding)

#         FigureCanvas.updateGeometry(self)

#         self.plot()
 
 
#     def plot(self):
#         data = [random.random() for i in range(25)]
#         # ax = self.figure.add_subplot(111)
#         self.axes.plot(data, 'r-')
#         self.axes.set_title('PyQt Matplotlib Example')
#         self.draw()
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
