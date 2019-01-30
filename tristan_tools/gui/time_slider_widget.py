# this is the slider linked to a text field which occurs in several places
# in the gui

from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtGui import QIntValidator 


class TimeSliderWidget( QWidget ) :

    def __init__( self ) :
        super().__init__()

        layout = QHBoxLayout()

        self.number_entry = QLineEdit( '0' )         
        self.number_entry.setValidator( QIntValidator() )
        NUM_CHARS =  6   # 30 pixels per char
        self.number_entry.setFixedWidth( 10 * NUM_CHARS ) 

        self.slider = QSlider( QtCore.Qt.Horizontal )
        
        layout.addWidget( self.number_entry ) 
        layout.addWidget( self.slider ) 
        
        self.setLayout( layout ) 


    def set_number_entry_from_slider( self ) :
        pass


    def set_slider_from_number_entry( self ) :
        pass 
            
