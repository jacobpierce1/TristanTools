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
        left_button = QPushButton( unicode.ULEFT_ARROW ) 
        right_button = QPushButton( unicode.URIGHT_ARROW )

        self.layout.addWidget( left_button )
        self.layout.addWidget( right_button ) 
        self.layout.addWidget( self.slider )
        self.layout.addWidget( self.reload_button ) 
        
