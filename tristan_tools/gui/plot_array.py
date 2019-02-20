# this provides the system for controlling active plots, etc. no data loading
# in here. 
import gui_config 
from plotter_widget import PlotterWidget


import numpy as np
import matplotlib.pyplot as plt




from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QFont, QPixmap, QImage
# from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import Qt








class PlotArray( QWidget ) :

    def __init__( self, tristan_data_analyzer, state_handler, shape = None ) :
        super().__init__()

        # store inputs 
        self.analyzer = tristan_data_analyzer 
        self.state_handler = state_handler

        # self.timestep = 0 
        
        self.reset()


        
    def reset( self ) :
            
        # store all the qwidgets
        shape = self.state_handler.shape
        self.plots = np.zeros( shape, dtype = object ) 
        
        layout = QGridLayout()
        
        shape = self.state_handler.shape

        for i in range( shape[0] ) :
            for j in range( shape[1] ) : 

                self.plots[i,j] = PlotterWidget( self.analyzer,
                                                 self.state_handler.plot_types[i,j],
                                                 self.state_handler.keys[i,j] )
            
                layout.addWidget( self.plots[i,j], i, j)
                
        self.setLayout( layout )         

        
        
    # clear all plots. possibly change dimensions of the plot array.
    def clear( self ) : 
       pass  

   

    # update all plots 
    def update( self, timestep ) :

        # self.timestep = timestep 
        
        shape = self.state_handler.shape 
        for i in range( shape[0] ) :
            for j in range( shape[1] ) :
                print( (i,j) )
                print( self.plots[i,j].tristan_data_plotter.keys )
                print( self.plots[i,j].tristan_data_plotter.plot_type )
                self.plots[i,j].update( timestep ) 
