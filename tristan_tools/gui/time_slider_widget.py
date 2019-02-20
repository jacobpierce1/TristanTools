# this is the slider linked to a text field which occurs in several places
# in the gui

from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtGui import QIntValidator 

import unicode_shortcuts 

TEXTFIELD_WIDTH_CHARS =  6   # 30 pixels per char




# updater is a function that is called whenever the timestep changes
# for the timesliderwidget in the MainControlPanel, this is update_plots which updates all the plots.
class TimeSliderWidget( QWidget ) :

    def __init__( self, num_timesteps, use_slider = 1, updater = None ) :
        super().__init__()

        # variables we will track
        self.num_timesteps = num_timesteps
        self.max_timestep = num_timesteps - 1 
        self.use_slider = use_slider
        self.stride = 1 
        self.timestep = 0

        # function given by user to be called when self.update is called.
        # will not be called if set to None 
        self.updater = updater 
        
        # init the UI
        
        layout = QHBoxLayout()

        self.left_button = QPushButton( unicode_shortcuts.ULEFT_ARROW ) 
        self.right_button = QPushButton( unicode_shortcuts.URIGHT_ARROW )

        self.left_button.clicked.connect( self.left_button_clicked )
        self.right_button.clicked.connect( self.right_button_clicked )
        
        layout.addWidget( self.left_button ) 
        layout.addWidget( self.right_button ) 
        
        self.timestep_entry = QLineEdit( str( self.timestep ) )
        self.timestep_entry.returnPressed.connect( self.timestep_entry_returnPressed ) 
        
        self.stride_entry = QLineEdit( str( self.stride ) ) 
        self.stride_entry.returnPressed.connect( self.stride_entry_returnPressed ) 
        
        entries = [ self.timestep_entry, self.stride_entry ]
        tooltips = [ 'timestep', 'stride' ]

        for i in range( len( entries ) ) :
            entries[i].setValidator( QIntValidator() )
            entries[i].setFixedWidth( 10 * TEXTFIELD_WIDTH_CHARS ) 
            entries[i].setToolTip( tooltips[i] ) 
            layout.addWidget( entries[i] ) 
            
        if self.use_slider : 
            self.slider = QSlider( QtCore.Qt.Horizontal )
            self.slider.setMaximum( self.max_timestep )
            self.slider.sliderMoved.connect( self.slider_moved ) 
            self.slider.sliderReleased.connect( self.slider_released ) 
            layout.addWidget( self.slider )

        self.setLayout( layout ) 

        
    def slider_moved( self ) :
        timestep = self.slider.value() 
        self.set_timestep_entry( timestep ) 

        
    def slider_released( self ) :
        self.slider_moved()
        self.handle_new_timestep( self.slider.value() )

        
    def timestep_entry_returnPressed( self ) :
        tmp = int( self.timestep_entry.text() ) 
        timestep = min( self.num_timesteps, max( 0, tmp ) )
            
        self.handle_new_timestep( timestep )

        # correct the value if the user supplies one out of bounds 
        if timestep != tmp :
            self.set_timestep_entry() 
            
        self.set_slider() 
            

    def stride_entry_returnPressed( self ) :
        newstride = int( self.stride_entry.text() )
        self.stride = newstride

        
    def left_button_clicked( self ) :
        timestep = max( 0, self.timestep - self.stride ) 
        self.handle_new_timestep( timestep )
        self.update() 
        
        
    def right_button_clicked( self ) :
        timestep = min( self.num_timesteps - 1, self.timestep + self.stride ) 
        self.handle_new_timestep( timestep ) 
        self.update()


    # update both the slider and the timestep_entry 
    def update( self, timestep = None ) :
        
        if timestep is None :
            timestep = self.timestep 
            
        self.set_slider( timestep ) 
        self.set_timestep_entry( timestep ) 

        
    def set_slider( self, timestep = None ) :

        if timestep is None :
            timestep = self.timestep 
        
        if self.use_slider :
            self.slider.setValue( timestep )            

            
    def set_timestep_entry( self, timestep = None ) :

        if timestep is None :
            timestep = self.timestep 
        
        self.timestep_entry.setText( str( timestep ) )
            
            
    # do something if the timestep is ever changed
    def handle_new_timestep( self, timestep ) :
        
        if timestep != self.timestep :

            # the updater accesses this variable, so it needs to be set first 
            self.timestep = timestep

            if self.updater : 
                self.updater() 


