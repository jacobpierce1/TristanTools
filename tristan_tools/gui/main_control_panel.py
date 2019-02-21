# this contains the class for the control panel at the bottom of the screen
# with slider, load next frame, set frame jump size, etc.

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QFont, QPixmap
# from PyQt5 import QtGui
from PyQt5 import QtCore


from tristan_tools.analysis import TristanError


from time_slider_widget import TimeSliderWidget
from data_loader import DataLoader 







class MainControlPanel( QWidget ) :

    def __init__( self, plot_array  ) :
        super().__init__() 

        self.analyzer = plot_array.analyzer 
        
        num_timesteps = len( self.analyzer ) 
        self.plot_array = plot_array
        
        self.data_loader = DataLoader( self.analyzer ) 

        layout = QVBoxLayout() 

        layout1 = QHBoxLayout() 

        self.time_slider_widget = TimeSliderWidget( num_timesteps, updater = self.update_plots ) 

        self.reload_button = QPushButton( 'Reload' )
        self.reload_button.clicked.connect( self.reload_button_clicked ) 
        
        self.load_new_button = QPushButton( 'Load New' )
        self.load_new_button.clicked.connect( self.load_new_button_clicked ) 

        # self.set_plot_shape_button = QPushButton( 'Set Plot Shape' )
        # self.save_state_button = QPushButton( 'Save State' )
        # self.load_state_button = QPushButton( 'Load State' ) 

        # self.index = 0
        
        layout1.addWidget( self.time_slider_widget ) 
        layout1.addWidget( self.reload_button ) 
        layout1.addWidget( self.load_new_button ) 
        
        layout.addLayout( layout1  )


        self.data_path_label = QLabel() 
        layout.addWidget( self.data_path_label )
        
        self.time_label = QLabel() 
        layout.addWidget( self.time_label )
        
        self.setLayout( layout ) 

        # init everything 
        self.update_plots() 
        self.update_data_path_label() 
        self.update_time_label() 

                

    # this will be called whenever the timestep changes, either via the text field
    # or the slider in self.time_slider_widget. in this case we update the time
    # entries of all the other plots. 
    def update_plots( self ) :

        print( 'calling data_loader.handle_timestep' )
        
        self.data_loader.handle_timestep( self.time_slider_widget.timestep,
                                          self.time_slider_widget.stride,
                                          self.time_slider_widget.max_timestep ) 

        print( 'calling plot array update' ) 
        
        self.plot_array.update( self.time_slider_widget.timestep )

        self.update_time_label() 



    def update_time_label( self ) :
        # print( self.plot_array.analyzer.data.time )
        timestep = self.time_slider_widget.timestep
        # print( 'updating time label: ' + str( timestep ) ) 
        self.time_label.setText( 'Time: ' + '%f' % self.analyzer.data.time[ timestep ] )
        self.time_label.repaint() 

                                 

    def update_data_path_label( self ) :
        self.data_path_label.setText( 'Data path: ' + self.plot_array.analyzer.data_path ) 
        

    # when reloading data, we aren't actually loading any more data. we really just
    # tell the TristanDataContainer that there is more data now than there originally was.
    # new data only gets loaded if it would have been loaded anyway had the TristanDataContainer known it
    # was there. we also need to adjust the timestep controller max and min once it gets changed. 
    def reload_button_clicked( self ) :

        self.analyzer.reload_data_path()
        
        self.data_loader.handle_timestep( self.time_slider_widget.timestep,
                                          self.time_slider_widget.stride,
                                          self.time_slider_widget.max_timestep )
        
        self.time_slider_widget.set_num_timesteps( len( self.analyzer ) ) 
        
        # timesteps = self.data_loader.timesteps_loaded
        


        
    def load_new_button_clicked( self ) :

        new_data_path = str(QFileDialog.getExistingDirectory(self, "Select New Data"))
        new_data_path += '/'

        print( 'INFO: setting new_data_path: ', new_data_path ) 
        if not new_data_path :
            return 

        try : 
            self.analyzer.set_data_path( new_data_path )

        except TristanError :
            return

        self.data_loader.clear()
        self.data_loader.handle_timestep( self.time_slider_widget.timestep,
                                          self.time_slider_widget.stride,
                                          self.time_slider_widget.max_timestep )

        self.plot_array.reset() 
        self.plot_array.update( self.time_slider_widget.timestep )
        self.update_data_path_label() 
