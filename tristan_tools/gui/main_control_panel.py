# this contains the class for the control panel at the bottom of the screen
# with slider, load next frame, set frame jump size, etc.

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QFont, QPixmap
# from PyQt5 import QtGui
from PyQt5 import QtCore

from time_slider_widget import TimeSliderWidget

class MainControlPanel( QWidget ) :

    def __init__( self, plotter_widget  ) :
        super().__init__() 
        
        num_timesteps = len( plotter_widget.analyzer ) 
        self.plotter_widget = plotter_widget

        layout = QHBoxLayout() 

        self.time_slider_widget = TimeSliderWidget( num_timesteps, updater = self.updater ) 
        self.reload_button = QPushButton( 'Reload' ) 
        self.load_new_button = QPushButton( 'Load New' )
        
        # self.set_plot_shape_button = QPushButton( 'Set Plot Shape' )
        # self.save_state_button = QPushButton( 'Save State' )
        # self.load_state_button = QPushButton( 'Load State' ) 

        # self.index = 0
        
        layout.addWidget( self.time_slider_widget ) 
        layout.addWidget( self.reload_button ) 
        layout.addWidget( self.load_new_button ) 

        self.setLayout( layout ) 


    # this will be called whenever the timestep changes, either via the text field
    # or the slider in self.time_slider_widget. in this case we update the time
    # entries of all the other plots. 
    def updater( self ) :
        self.plotter_widget.update( self.time_slider_widget.timestep )

                
        
        
