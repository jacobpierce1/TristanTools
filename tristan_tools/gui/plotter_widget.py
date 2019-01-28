# this provides the system for controlling active plots, etc. no data loading
# in here. 
import gui_config 

import numpy as np
import matplotlib.pyplot as plt


from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QFont, QPixmap, QImage
# from PyQt5 import QtGui
from PyQt5 import QtCore


from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure



class PlotterWidget( object ) :

    def __init__( self, shape = None ) :

        if shape is None :
            shape = (gui_config.NUM_PLOT_ROWS, gui_config.NUM_PLOT_COLS ) 
        
        self.f, self.axarr = plt.subplots( * shape ) 

        self.canvas = FigureCanvas( self.f )
    

    # clear all plots. possibly change dimensions of the plot array.
    def reset( self ) : 
       pass  
