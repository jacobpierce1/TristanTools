
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt


from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure




class MPLPlotContainer( QWidget ) :

    
    def __init__(self, tristan_data_plotter ):
        super().__init__()

        self.tristan_data_plotter = tristan_data_plotter
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)


        self.figure = Figure()
        self.ax = self.figure.add_subplot( 111 ) 
        self.canvas = FigureCanvas( self.figure )

        layout.addWidget( self.canvas ) 

        self.tristan_data_plotter.plotter.set_mpl_axes( self.ax ) 

        self.setLayout( layout ) 


        
    def update( self, timestep ) :
        # self.figure.clf() 
        print( 'called update' ) 
        self.tristan_data_plotter.plot_timestep( timestep )
        print( 'drawing' ) 
        self.canvas.draw()
        print( 'finished drawing' ) 


        
    def get_canvas( self ) :
        return self.ax

    

    def delet( self ) :
        pass 
