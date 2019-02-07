# implements PlotControlWidget. this is the buttons and slider below each plot

from time_slider_widget import TimeSliderWidget
from plot_options_widgets import * 

from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt 


# PLOT_TYPES = [ 'scalar slice', 'quiver3d', 'quiver slice', '2D image' ] 

MOVIE_TYPES = [ 'GIF', 'mp4', 'mov' ] 


_plot_options_widgets = { 'volume_slice' : VolumeSliceOptionsWidget,
                          'volume' : VolumeOptionsWidget, 
                          'vector_field' : VectorFieldOptionsWidget,
                          'vector_cut_plane' : VectorCutPlaneOptionsWidget } 



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

        num_times = len( self.tristan_data_plotter.analyzer )
        self.time_slider_widget = TimeSliderWidget( num_times, use_slider = 0 )

        layout.addWidget( self.time_slider_widget ) 

        self.setLayout( layout ) 


        
    def reset( self ) :
        self.tristan_data_plotter.plotter.reset() 
        

        
    def launch_options_window( self ) :
        self.options_dialog = PlotOptionsDialog( self.tristan_data_plotter )
        
        # options_dialog.exec_()
        self.options_dialog.show() 
        
        # self.plot_type = options_dialog.plot_type
        # self.plot_quantity = options_dialog.plot_quantity
        
        # print( 'plot type: ' + str( self.plot_type ) )

            


    def launch_actions_window( self ) :
        self.actions_dialog = PlotActionsDialog()
        self.actions_dialog.show() 



        
        
class PlotOptionsDialog( QDialog ) :

    def __init__( self, tristan_data_plotter ) :
        super().__init__()
        
        self.plot_type_changed_status = 0
        
        # disable blocking of the main application
        self.setWindowModality( Qt.NonModal )
        
        self.tristan_data_plotter = tristan_data_plotter 
        
        self.plot_type = tristan_data_plotter.plot_type
        
        self.setWindowTitle( 'Plot Options' ) 
        
        self.plot_type_combobox = QComboBox()

        for key in self.tristan_data_plotter.available_data_dict.keys() :
            self.plot_type_combobox.addItem( key )  

        # activated signal is when the user selects a new index
        # but not when the index is changed via a setter 
        self.plot_type_combobox.activated.connect( self.plot_type_changed ) 
            
        self.data_selection_combobox = QComboBox()
        self.data_selection_combobox.activated.connect( self.data_selection_changed ) 
        self.reset_data_selection_combobox()

        print( tristan_data_plotter.analyzer.data.keys() )

        # ok_button = QPushButton( 'OK' )         
        # ok_button.clicked.connect( self.ok_button_clicked )

        
        layout = QVBoxLayout() 
        self.setLayout( layout )
        
        toplayout = QHBoxLayout() 
        toplayout.addWidget( self.plot_type_combobox ) 
        toplayout.addWidget( self.data_selection_combobox ) 
        # toplayout.addWidget( ok_button ) 
        
        layout.addLayout( toplayout )

        self.plot_options_widget = None
        self.update_plot_options_widget()

        # self.accept() 
        
        # init_data =
        # self.plot_options_widget = None
        # self.update_plot_options_widget()
        # layout.addWidget( self.plot_options_widget )
        

    def update_plot_options_widget( self ) :
        layout = self.layout()
        if self.plot_options_widget is not None :
            # self.plot_options_widget.delete()
            self.plot_options_widget.deleteLater()
            layout.removeWidget( self.plot_options_widget )
            del self.plot_options_widget 
        self.plot_options_widget = _plot_options_widgets[ self.plot_type ]( self.tristan_data_plotter.plotter )
        layout.addWidget( self.plot_options_widget ) 
        
        
        
    def reset_data_selection_combobox( self ) :
        print( 'resetting data selection' ) 
        self.data_selection_combobox.clear()
        available_data = self.tristan_data_plotter.available_data_dict[ self.plot_type ]
        for i in range( len( available_data ) ) :
            self.data_selection_combobox.addItem( available_data[i] ) 
                        

        
        
    def data_selection_changed( self ) :

        self.data_name = self.data_selection_combobox.currentText()
        keys = self.tristan_data_plotter.data_name_to_keys_dict[ self.data_name ] 

        # if the plot type has been changed, then change the plot type and set the new keys
        if self.plot_type_changed_status :
            self.tristan_data_plotter.set_plot_type( self.plot_type, keys ) 
            self.tristan_data_plotter.refresh()
            self.update_plot_options_widget() 
            self.plot_type_changed_status = 0
            
        
        # otherwise update the data immediately 
        else :
            print( 'setting new keys' ) 
            self.tristan_data_plotter.set_keys( keys )
            self.tristan_data_plotter.refresh() 



    def plot_type_changed( self ) :
        print( 'called plot type changed' ) 
        self.plot_type = self.plot_type_combobox.currentText()
        self.plot_type_changed_status = 1 
        self.reset_data_selection_combobox()
        


    def ok_button_clicked( self ) :

        # if self.plot_type_changed_status :
        #     keys = self.tristan_data_plotter.data_name_to_keys_dict[ self.data_name ] 
        #     self.tristan_data_plotter.set_plot_type( self.plot_type, keys )
        pass 
        # self.close() 






        
        
        
class PlotActionsDialog( QDialog ) :

    def __init__( self ) :
        super().__init__() 

        # disable blocking of main app 
        self.setWindowModality( Qt.NonModal )
        
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

        



        
