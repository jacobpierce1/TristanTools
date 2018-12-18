import gui_config 
import control_panel 
import plotter_widget


import sys 
import scipy.stats as st
import struct 
import threading
import datetime
import os
import numpy as np
import scipy
import time
from functools import partial

# import gui_helpers


from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QFont, QPixmap
# from PyQt5 import QtGui
from PyQt5 import QtCore



from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import matplotlib.pyplot as plt

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)




def main():
   app = QApplication(sys.argv)
   app.setStyleSheet( 'QGroupBox { font-weight: bold; }' ) 
   ex = gui()
   ex.show()
   sys.exit( app.exec_() )



class gui( QWidget ) :

    # set_tabor_params_signal = QtCore.pyqtSignal( cpt_tools.TaborParams )
    # set_batch_data_signal = QtCore.pyqtSignal( list ) 

    
    def __init__(self, parent = None):
        super( gui, self ).__init__( parent )

        self.setWindowTitle("TristanPlotter")
        self.resize( gui_config.WINDOW_WIDTH, gui_config.WINDOW_HEIGHT )

        layout = QVBoxLayout()
        self.setLayout( layout ) 

        self.plotter_widget = plotter_widget.PlotterWidget()
        layout.addWidget( self.plotter_widget.canvas )
        
        self.control_panel = control_panel.ControlPanel()
        layout.addLayout( self.control_panel.layout ) 
        
        

# enter program 
if __name__ == '__main__':  
    main()



