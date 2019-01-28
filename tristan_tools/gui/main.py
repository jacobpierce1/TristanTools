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

# from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QFont, QPixmap, QIcon
# from PyQt5 import QtGui
from PyQt5 import QtCore



from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import matplotlib.pyplot as plt

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)




def main():
    # app = QApplication(sys.argv)
    # app.setStyleSheet( 'QGroupBox { font-weight: bold; }' ) 
    # ex = gui()
    # ex.show()
    # sys.exit( app.exec_() )

    app = QApplication(sys.argv)
    app.setStyleSheet( 'QGroupBox { font-weight: bold; }' ) 
    ex = App()
    ex.show()
    sys.exit( app.exec_() )
    


    
class App( QWidget ) :

    # set_tabor_params_signal = QtCore.pyqtSignal( cpt_tools.TaborParams )
    # set_batch_data_signal = QtCore.pyqtSignal( list ) 

    def __init__(self ):
        super().__init__()

        self.setWindowTitle( 'TristanPlotter' )
        self.resize( gui_config.WINDOW_WIDTH, gui_config.WINDOW_HEIGHT )
        
        layout = QVBoxLayout()
        self.setLayout( layout ) 
        
        self.plotter_widget = plotter_widget.PlotterWidget()
        layout.addWidget( self.plotter_widget.canvas )
        
        self.control_panel = control_panel.ControlPanel()
        layout.addLayout( self.control_panel.layout ) 

        self.init_menubar() 
        

        
    def init_menubar( self ) :
        menu_bar = QMenuBar(self)

        options_menu = menu_bar.addMenu( 'Options' ) 

        options_menu_strings = [ 'Load Directory', 'Set Plot Dimensions',
                                 'Save State', 'Load State' ]

        options_menu_actions = [ self.load_directory, self.set_plot_dimensions,
                                 self.save_state, self.load_state ] 

        for i in range( len( options_menu_strings ) ) :
            action = options_menu.addAction( options_menu_strings[i] ) 
            action.triggered.connect( options_menu_actions[i] ) 


            
    def load_directory( self ) :
        dir_path = str( QFileDialog.getExistingDirectory(
            self, "Select Output Directory") )
        # self.tristan_data.clear()
        self.tristan_data.set_data_path( dir_path ) 


    def set_plot_dimensions( self ) :
        pass

    def save_state( self ) :
        pass

    def load_state( self ) :
        pass
        
      

# enter program 
if __name__ == '__main__':  
    main()



