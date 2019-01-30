# implements PlotControlWidget. this is the buttons and slider below each plot

from time_slider_widget import TimeSliderWidget 

from PyQt5.QtWidgets import *
from PyQt5 import QtCore


PLOT_TYPES = [ 'scalar slice', 'quiver3d', 'quiver slice' ] 


class PlotControlWidget( QWidget ) :

    def __init__( self ) :
        super().__init__() 
    
        # layout = QVBoxLayout()

        # self.save_plot_button = QPushButton( 'Save Plot' )
        # self.save_gif_button = QPushButton( 'Save GIF' )
        # self.change_plot_button = QPushButton( 'Change Plot' )

        # tmplayout = QHBoxLayout()
        # tmplayout.addWidget( self.save_plot_button )
        # tmplayout.addWidget( self.save_gif_button )
        # tmplayout.addWidget( self.change_plot_button ) 

        self.options_button = QPushButton( 'Options' )
        self.actions_button = QPushButton( 'Actions' )

        self.options_button.clicked.connect( self.launch_options_window ) 
        
        
        # layout.addLayout( tmplayout )

        layout = QHBoxLayout()

        # self.options_button = QPushButton( 'Options' ) 
        # self.options_button.clicked.connect( self.options_button_clicked )

        
        layout.addWidget( self.options_button ) 
        layout.addWidget( self.actions_button ) 
        
        self.time_slider_widget = TimeSliderWidget()
        layout.addWidget( self.time_slider_widget ) 

        self.setLayout( layout ) 


    def launch_options_window( self ) :
        self.options_window = PlotOptionsWindow()
        print( 'reached1' ) 

        self.options_window.show()

        print( 'reached2' ) 


    def launch_actions_window( self ) :
        actions_window = PlotActionsWindow()
        actions_window.show() 




        
class PlotOptionsWindow( QWidget ) :

    def __init__( self, parent = None ) :
        super().__init__( parent ) 

        self.setWindowTitle( 'Plot Options' ) 
        
        self.plot_type_combobox = QComboBox()
        self.plot_type_combobox.setObjectName( 'test' )

        for plot_type in PLOT_TYPES :
            self.plot_type_combobox.addItem( plot_type ) 

        layout = QVBoxLayout() 
        
        toplayout = QHBoxLayout() 
        toplayout.addWidget( self.plot_type_combobox ) 


        layout.addLayout( toplayout ) 
        
        self.setLayout( layout ) 



        
        
class PlotActionsWindow( QMainWindow ) :

    def __init__( self ) :
        super().__init__() 

        self.setWindowTitle( 'Plot Actions' ) 
        

def callback_factory(k, v):
    return lambda: button.setText('{0}_{1}'.format(k, v))

