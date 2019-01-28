# this contains the class for the control panel at the bottom of the screen
# with slider, load next frame, set frame jump size, etc.

import unicode 

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QFont, QPixmap
# from PyQt5 import QtGui
from PyQt5 import QtCore



class ControlPanel( object ) :

    def __init__( self  ) :

        self.layout = QHBoxLayout() 

        self.slider = QSlider( QtCore.Qt.Horizontal )
        self.reload_button = QPushButton( 'Reload' ) 
        self.left_button = QPushButton( unicode.ULEFT_ARROW ) 
        self.right_button = QPushButton( unicode.URIGHT_ARROW )

        self.index_entry = QLineEdit( '0' ) 
        self.index_entry.setValidator( QIntValidator() )
        NUM_CHARS =  6   # 30 pixels per char
        self.index_entry.setFixedWidth( 10 * NUM_CHARS ) 

        self.index = 0
        
        self.layout.addWidget( self.left_button )
        self.layout.addWidget( self.right_button )
        self.layout.addWidget( self.index_entry ) 
        self.layout.addWidget( self.slider )
        self.layout.addWidget( self.reload_button ) 


    def update_slider( self, frac ) :
        pass

    def read_index_entry( self ) :
        # self.index = 0
        pass
