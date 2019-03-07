from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QFont, QPixmap
# from PyQt5 import QtGui
from PyQt5 import QtCore


# First, and before importing any Enthought packages, set the ETS_TOOLKIT
# environment variable to qt4, to tell Traits that we will use Qt.
import os
os.environ['ETS_TOOLKIT'] = 'qt4'
os.environ['QT_API'] = 'pyqt5'


import gui_config 
from main_control_panel import MainControlPanel 
from plot_array import PlotArray
from state_handler import StateHandler, LoadPolicy 


import tristan_tools.analysis as analysis 

import sys 
import struct 
import threading
import datetime
import os
import numpy as np
import scipy
import time


# from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QFont, QPixmap, QIcon
# from PyQt5 import QtGui
from PyQt5 import QtCore

# from pyface.qt import QtGui, QtCore


# from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
# from matplotlib.figure import Figure

# import matplotlib.pyplot as plt

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)




    
class App( QWidget ) :

    # set_tabor_params_signal = QtCore.pyqtSignal( cpt_tools.TaborParams )
    # set_batch_data_signal = QtCore.pyqtSignal( list ) 

    def __init__(self ):
        super().__init__()

        self.state_handler = StateHandler()

        # attempt to initialize an analyzer from the current directory.
        # if not possible, it will maintain the value None 
        self.analyzer = None 
        self.init_analyzer()
        
        self.init_menubar() 

        # self.closeButton.clicked.connect( lambda : sys.exit(0) )
        
        self.setWindowTitle( 'TristanGUI' )
        self.resize( gui_config.WINDOW_WIDTH, gui_config.WINDOW_HEIGHT )
        
        layout = QVBoxLayout()
        self.setLayout( layout ) 
        
        self.plot_array = PlotArray( self.analyzer, self.state_handler )
        layout.addWidget( self.plot_array ) 
        # layout.addWidget( self.plotter_widget.canvas )
        
        self.control_panel = MainControlPanel( self.plot_array )
        layout.addWidget( self.control_panel ) 

        # plot data at timestep 0
        # self.plotter_widget.update( 0 ) 
        # self.control_panel.update_plots() 
        

    def closeEvent( self, event ) :
        sys.exit(0)
        
        
        
    def init_analyzer( self ) :
        cwd = os.getcwd()
    
        # check if cwd is the output directory 
        if os.path.basename( cwd ) == 'output' :
            data_path = cwd

        # check if there's a directory called 'output' in cwd
        else :
            tmp = os.path.join( cwd, 'output' )
            if os.path.exists( tmp ) :
                data_path = tmp
            else :
                data_path = None 

        if data_path :
            print( 'INFO: found data at path: %s' % data_path )
        else : 
            print( 'WARNING: did not find tristan output data path' ) 

        # set the type of analyzer to be used in the gui_config.py
        self.analyzer = gui_config.analyzer( data_path ) 

        
        # if self.state_handler.data_load_policy == LoadPolicy.LOAD_ALL :

        #     if gui_config.DEVELOPER_MODE :
        #         indices = range(10)
        #     else :
        #         indices = None
            
        #     self.analyzer.load_indices( indices ) 

        # print( 'in main. indices are loaded: ' + str( self.analyzer.indices_with_data )  )

        
        
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
        dir_path = str( QFileDialog.getExistingDirectory( self, "Select Output Directory") )
        # self.analyzer.clear()
        self.analyzer.set_data_path( dir_path ) 


        
    def set_plot_dimensions( self ) :
        pass



    
    def save_state( self ) :
        pass



    
    def load_state( self ) :
        pass
        
    
    
# enter program 
if __name__ == '__main__':  
    app = QApplication(sys.argv)
    app.setStyleSheet( 'QGroupBox { font-weight: bold; }' ) 
    ex = App()
    ex.show()
    sys.exit( app.exec_() )
    



