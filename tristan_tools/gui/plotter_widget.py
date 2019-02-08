# this provides the system for controlling active plots, etc. no data loading
# in here. 
import gui_config 
from mayavi_qwidget import MayaviQWidget

import numpy as np
import matplotlib.pyplot as plt




from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QFont, QPixmap, QImage
# from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import Qt


from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure





class PlotterWidget( QWidget ) :

    def __init__( self, tristan_data_analyzer, state_handler, shape = None ) :
        super().__init__()

        # store inputs 
        self.analyzer = tristan_data_analyzer 
        self.state_handler = state_handler 

        self.reset()


    def reset( self ) :
            
        # store all the qwidgets
        shape = self.state_handler.shape
        self.mayavi_plots = np.zeros( shape, dtype = object ) 
        
        layout = QGridLayout()
        
        # add array of mayavi plots 

        shape = self.state_handler.shape
        # for i in reversed( range( shape[0] ) ):
        #     for j in reversed( range( shape[1]  ) ):
        for i in range( shape[0] ) :
            for j in range( shape[1] ) : 

                # if (i,j) != (0,0) :
                #     continue
                
                print( (i,j) )
                print( self.state_handler.plot_types[i,j] )
                print( self.state_handler.keys[i,j] )

                self.mayavi_plots[i,j] = MayaviQWidget( self.analyzer,
                                                        self.state_handler.plot_types[i,j],
                                                        self.state_handler.keys[i,j] )
            
                layout.addWidget( self.mayavi_plots[i,j], i, j)
                
        self.setLayout( layout )         

        
    # clear all plots. possibly change dimensions of the plot array.
    def clear( self ) : 
       pass  


    # update all plots 
    def update( self, timestep ) :
        print( 'in update' ) 
        shape = self.state_handler.shape 
        for i in range( shape[0] ) :
            for j in range( shape[1] ) :
                print( (i,j) )
                print( self.mayavi_plots[i,j].tristan_data_plotter.keys )
                print( self.mayavi_plots[i,j].tristan_data_plotter.plot_type )
                self.mayavi_plots[i,j].update( timestep ) 
