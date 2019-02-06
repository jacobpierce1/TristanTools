# implements PlotControlWidget. this is the buttons and slider below each plot

from time_slider_widget import TimeSliderWidget
from plot_options_widgets import * 

from PyQt5.QtWidgets import *
from PyQt5 import QtCore


PLOT_TYPES = [ 'scalar slice', 'quiver3d', 'quiver slice', '2D image' ] 

MOVIE_TYPES = [ 'GIF', 'mp4', 'mov' ] 


_plot_options_widgets = { 'volume_slice' : VolumeSliceOptionsWidget } 



class PlotControlWidget( QWidget ) :

    def __init__( self, tristan_data_plotter ) :
        super().__init__() 

        self.tristan_data_plotter = tristan_data_plotter

        reset_button = QPushButton( 'Reset' ) 
        options_button = QPushButton( 'Options' )
        actions_button = QPushButton( 'Actions' )

        reset_button.clicked.connect( self.reset ) 
        options_button.clicked.connect( self.launch_options_window ) 
        actions_button.clicked.connect( self.launch_actions_window ) 
        
        # layout.addLayout( tmplayout )

        layout = QHBoxLayout()

        layout.addWidget( reset_button ) 
        layout.addWidget( options_button ) 
        layout.addWidget( actions_button ) 
        
        self.time_slider_widget = TimeSliderWidget( len( self.tristan_data_plotter.analyzer ),
                                                    use_slider = 0 )
        layout.addWidget( self.time_slider_widget ) 

        self.setLayout( layout ) 


        
    def reset( self ) :
        self.tristan_data_plotter.plotter.reset() 
        

        
    def launch_options_window( self ) :
        options_dialog = PlotOptionsDialog( self.tristan_data_plotter )

        options_dialog.exec_()

        self.plot_type = options_dialog.plot_type
        # self.plot_quantity = options_dialog.plot_quantity
        
        print( 'plot type: ' + str( self.plot_type ) )

            


    def launch_actions_window( self ) :
        actions_dialog = PlotActionsDialog()
        actions_dialog.exec_() 



        
        
class PlotOptionsDialog( QDialog ) :

    def __init__( self, tristan_data_plotter ) :
        super().__init__() 

        self.plot_type = tristan_data_plotter.plot_type
        # self.plot_quantity = None
        # self.plot_options = None
        
        self.setWindowTitle( 'Plot Options' ) 
        
        self.plot_type_combobox = QComboBox()
        # self.plot_type_combobox.setObjectName( 'test' )

        for plot_type in PLOT_TYPES :
            self.plot_type_combobox.addItem( plot_type ) 

        self.plot_quantity_combobox = QComboBox()

        ok_button = QPushButton( 'OK' )         
        ok_button.clicked.connect( self.close )
        
        layout = QVBoxLayout() 
        self.setLayout( layout )
        
        toplayout = QHBoxLayout() 
        toplayout.addWidget( self.plot_type_combobox ) 
        toplayout.addWidget( self.plot_quantity_combobox ) 
        toplayout.addWidget( ok_button ) 
        
        layout.addLayout( toplayout )

        plot_options_widget = _plot_options_widgets[ self.plot_type ]( tristan_data_plotter.plotter ) 
        layout.addWidget( plot_options_widget ) 
        



        
        
class PlotActionsDialog( QDialog ) :

    def __init__( self ) :
        super().__init__() 

        self.setWindowTitle( 'Plot Actions' ) 

        layout = QVBoxLayout()

        save_plot_button = QPushButton( 'Save Plot' ) 
        # todo 
        layout.addWidget( save_plot_button ) 

        # save gif / movie interface 
        tmplayout = QHBoxLayout()

        movie_type_combobox = QComboBox()
        for movie_type in MOVIE_TYPES :
            movie_type_combobox.addItem( movie_type ) 
            tmplayout.addWidget( movie_type_combobox )
        
        start_frame_entry = QLineEdit( '' )
        start_frame_entry.setPlaceholderText( 'Start Frame' ) 
        start_frame_entry.setToolTip( 'Start Frame' ) 
        tmplayout.addWidget( start_frame_entry ) 
        
        stop_frame_entry = QLineEdit() 
        stop_frame_entry.setToolTip( 'stop frame' )
        stop_frame_entry.setPlaceholderText( 'stop frame' ) 
        tmplayout.addWidget( stop_frame_entry )

        frame_stride_entry = QLineEdit()
        frame_stride_entry.setToolTip( 'Frame stride' ) 
        frame_stride_entry.setPlaceholderText( 'Frame stride' ) 
        tmplayout.addWidget( frame_stride_entry ) 
        
        frame_rate_entry = QLineEdit( str(1) )
        frame_rate_entry.setToolTip( 'Frame Rate in Hz' ) 
        tmplayout.addWidget( frame_rate_entry ) 
        
        save_movie_button = QPushButton( 'Save' )
        tmplayout.addWidget( save_movie_button  )
        
        layout.addLayout( tmplayout  )  

        self.setLayout( layout ) 
        





# # class for tracking the current plot options and interacting with a plotter to change them. 
# class PlotOptionsController( object ) :

#     def __init__( self, plotter ) :
#         self.plotter = plotter 





# class VolumeSliceOptionsController( PlotOptionsController ) :

#     def __init__( self, plotter ) :
#         supr().__init__( plotter ) 

        



        
