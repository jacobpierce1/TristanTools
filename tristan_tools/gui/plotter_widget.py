# widget that toggles between a mayavi plot and a matplotlib plot. 


import gui_config 
from mayavi_plot_container import MayaviPlotContainer
from mpl_plot_container import MPLPlotContainer
from plot_control_widget import PlotControlWidget


from tristan_tools.analysis import TristanDataPlotter

import numpy as np
import matplotlib.pyplot as plt



from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
from PyQt5 import QtCore
from PyQt5.QtCore import Qt



# these plots will use matplotlib. everything else uses mayavi. 
MPL_PLOT_TYPES = [ 'hist1d' ] 



class PlotterWidget( QWidget ) :

    def __init__( self , tristan_data_analyzer, plot_type, keys ) :
        super().__init__()

        
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        
        self.title_label = QLabel( '' )
        self.title_label.setAlignment( Qt.AlignCenter ) 
        layout.addWidget( self.title_label ) 

        self.tristan_data_plotter = TristanDataPlotter(
            tristan_data_analyzer, plot_type = plot_type, keys = keys ) 

        plot_container_class = _get_plot_container_class( plot_type ) 
        self.plot_container = plot_container_class( self.tristan_data_plotter )
        layout.addWidget( self.plot_container ) 
        
        self.plot_controller = PlotControlWidget( self.tristan_data_plotter, self )
        layout.addWidget( self.plot_controller )

        self.setLayout( layout )

        self.set_title() 
        


        
    def set_title( self, title = None ) :

        # default title 
        if title is None :

            plot_type = self.tristan_data_plotter.plot_type

            title = plot_type

            keys_str = ''
            keys = self.tristan_data_plotter.keys 
            for i in range( len( keys ) ) :

                keys_str += str( keys[i] )

                if i < len( keys ) - 1 :
                    keys_str += ', '
                            
            title += ': ' + keys_str 
                    
        self.title_label.setText( title ) 
        


        
    def update( self, timestep = None ) :
        
        if timestep is None :
            timestep = self.plot_controller.time_slider_widget.timestep  

        else :
            self.plot_controller.time_slider_widget.update( timestep ) 

        self.plot_container.update( timestep ) 


        

    def rebuild_plot_container( self ) :

        layout = self.layout() 
        
        # get rid of old plot container 
        self.plot_container.delete()

        self.plot_container.deleteLater()
        layout.removeWidget( self.plot_container )
        del self.plot_container 

        # add new plot container
        print( self.tristan_data_plotter.plot_type ) 
        
        plot_container_class = _get_plot_container_class( self.tristan_data_plotter.plot_type ) 
        self.plot_container = plot_container_class( self.tristan_data_plotter )
        layout.addWidget( self.plot_container ) 
        
        # self.plot_container = 


    
    def get_canvas( self ) :
        return self.plot_container.get_canvas() 

        
        

def _get_plot_container_class( plot_type ) :

    if plot_type in MPL_PLOT_TYPES :
        return MPLPlotContainer
    else :
        return MayaviPlotContainer 
