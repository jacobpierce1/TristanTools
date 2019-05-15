
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt


from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import matplotlib.pyplot as plt 



# rm 
from PyQt5 import QtWidgets
import random 


        

class MPLPlotContainer( QWidget ) :

    
    def __init__(self, tristan_data_plotter ):
        super().__init__()

        self.tristan_data_plotter = tristan_data_plotter
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)


        self.figure = Figure()
        self.ax = self.figure.add_subplot( 111 ) 

        # self.figure, self.ax = plt.subplots( 1, 1 )

        self.canvas = FigureCanvas( self.figure )

        self.figure.set_canvas( self.canvas ) 

        layout.addWidget( self.canvas ) 

        self.tristan_data_plotter.plotter.set_mpl_axes( self.ax ) 

        self.setLayout( layout ) 


        
    def update( self, timestep ) :
        # self.figure.clf() 
        # print( 'called update' ) 
        self.tristan_data_plotter.plot_timestep( timestep )
        # print( 'drawing' )

        # print( self.ax.lines[0].get_xydata() ) 
        
        self.canvas.draw()
        self.repaint() 
        # self.SetSize((self.Size[0],self.figurecanvas.Size[1]))



        
    def get_canvas( self ) :
        return self.ax

    

    def delete( self ) :
        pass 


    def clear( self ) :
        self.tristan_data_plotter.clear() 

    def reset( self ) :
        self.tristan_data_plotter.reset() 
