# this contains the class for the control panel at the bottom of the screen
# with slider, load next frame, set frame jump size, etc.

import numpy as np


from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
# from PyQt5 import QtCore
from PyQt5.QtCore import Qt 

from tristan_tools.analysis import TristanError, TristanCut


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

        self.set_cuts_button = QPushButton( 'Set Cuts' )
        self.set_cuts_button.clicked.connect( self.set_cuts_button_clicked ) 

        self.help_button = QPushButton( 'Help' )
        
        
        # self.set_plot_shape_button = QPushButton( 'Set Plot Shape' )
        # self.save_state_button = QPushButton( 'Save State' )
        # self.load_state_button = QPushButton( 'Load State' ) 

        # self.index = 0
        
        layout1.addWidget( self.time_slider_widget ) 
        layout1.addWidget( self.reload_button ) 
        layout1.addWidget( self.load_new_button ) 
        layout1.addWidget( self.set_cuts_button )
        layout1.addWidget( self.help_button ) 
        
        layout.addLayout( layout1  )
        
        param_names = [ 'time', 'num_electrons',
                        'num_ions', # 'num position-cut electrons', 'num position-cut ions',
                        'c', 'c_omp', 'mx0', 'my0', 'mz0' ] 

        self.param_name_to_idx_dict = dict( zip( param_names, range( len( param_names ) ) ) )

        nrows = 1
        ncols = len( param_names )  
        self.params_table = QTableWidget( nrows, ncols )

        self.params_table.setHorizontalHeaderLabels( param_names )
        # self.params_table.horizontalHeader().setStretchLastSection( 1 )
        # self.params_table.setWordWrap( 1 ) 
        
        self.params_table.horizontalHeader().setSectionResizeMode( QHeaderView.Stretch ) 
        tmp = self.params_table.verticalHeader()
        tmp.setSectionResizeMode( QHeaderView.Stretch )
        #tmp.setDefaultSectionSize( 12 ) 
        
        for i in range( ncols ) :
            self.params_table.setCellWidget( 0, i, QLabel() )

        layout.addWidget( self.params_table ) 
                        
        self.data_path_label = QLabel() 
        layout.addWidget( self.data_path_label )

        # self.time_label = QLabel() 
        # layout.addWidget( self.time_label )
        
        self.setLayout( layout ) 

        # init everything 
        self.update_plots() 
        self.update_data_path_label() 
        self.update_params_table( new_data_path = 1 )

        

    # this will be called whenever the timestep changes, either via the text field
    # or the slider in self.time_slider_widget. in this case we update the time
    # entries of all the other plots. 
    def update_plots( self, _reload = 0 ) :

        # print( 'calling data_loader.handle_timestep' )
        
        self.data_loader.handle_timestep( self.time_slider_widget.timestep,
                                          self.time_slider_widget.stride,
                                          self.time_slider_widget.max_timestep,
                                          _reload = _reload ) 

        # print( 'calling plot array update' ) 
        
        self.plot_array.update( self.time_slider_widget.timestep )

        self.update_params_table()

        # self.update_time_label() 



    # def update_time_label( self ) :
    #     # print( self.plot_array.analyzer.data.time )
    #     timestep = self.time_slider_widget.timestep
    #     # print( 'updating time label: ' + str( timestep ) ) 
    #     self.time_label.setText( 'Time: ' + '%f' % self.analyzer.data.time[ timestep ] )
    #     self.time_label.repaint() 

                                 

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
        # self.update_data_path_label() 
        self.update_params_table( new_data_path = 1 )
        self.update_data_path_label()
        


    def set_cuts_button_clicked( self ) :

        self.cuts_dialog = CutsDialog( self )
        self.cuts_dialog.show()




    def update_params_table( self, new_data_path = 0 ) :
                                            
        # for param_name, idx in self.param_name_to_idx_dict.items() :

        timestep = self.time_slider_widget.timestep
        table = self.params_table

        if timestep in self.analyzer.loaded_indices :

            idx = self.param_name_to_idx_dict[ 'num_electrons' ]
            table.cellWidget( 0, idx ).setText( str( len( self.analyzer.data.xe[ timestep ] ) ) )
                    
            idx = self.param_name_to_idx_dict[ 'num_ions' ]
            table.cellWidget( 0, idx ).setText( str( len( self.analyzer.data.xi[ timestep ] ) ) )

            idx = self.param_name_to_idx_dict[ 'time' ]
            table.cellWidget( 0, idx ).setText( str( self.analyzer.data.time[ timestep ] ) )
        
        
        # only set the rest of the params if the data path was changed 
        if not new_data_path : 
            return

        # idx = self.param_name_to_idx_dict[ 'data_path' ]
        # table.cellWidget( 0, idx ).setText( self.analyzer.data_path )
        
        idx = self.param_name_to_idx_dict[ 'c' ]
        table.cellWidget( 0, idx ).setText( '%.3f' % self.analyzer.params[ 'c' ] )

        idx = self.param_name_to_idx_dict[ 'c_omp' ]
        table.cellWidget( 0, idx ).setText( '%.3f' % self.analyzer.params[ 'c_omp' ] )

        idx = self.param_name_to_idx_dict[ 'mx0' ]
        table.cellWidget( 0, idx ).setText( str( self.analyzer.params[ 'mx0' ] ) )

        idx = self.param_name_to_idx_dict[ 'my0' ]
        table.cellWidget( 0, idx ).setText( str( self.analyzer.params[ 'my0' ] ) )

        idx = self.param_name_to_idx_dict[ 'mz0' ]
        table.cellWidget( 0, idx ).setText( str( self.analyzer.params[ 'mz0' ] ) )

        table.resizeRowsToContents()
        

        

class CutEntry( QWidget ) :

    def __init__( self, title, size ) :
        super().__init__()

        self.title = title
        self.size = size 
        
        # self.cut = TristanCut( size = size ) 

        layout = QVBoxLayout()
        box = QGroupBox( title )
        layout.addWidget( box )
        self.setLayout( layout ) 
        
        boxlayout  = QVBoxLayout() 
        box.setLayout( boxlayout ) 
        
        validator = QDoubleValidator( 0, 1e8, 4 ) 
        
        self.cut_entries = np.zeros( ( size, 2 ), dtype = object )  
        for i in range( size ) :
            hlayout = QHBoxLayout()
                
            for j in range( 2 ) :
                self.cut_entries[i,j] = QLineEdit() 
                tmp = self.cut_entries[i,j]
                tmp.setValidator( validator ) 
                hlayout.addWidget( tmp )
            boxlayout.addLayout( hlayout ) 

            
        
    def get( self ) :

        cut_array = np.zeros( ( self.size, 2 ), dtype = object ) 

        for i in range( self.size ) :

            for j in range(2) :
                tmp = self.cut_entries[i,j].text()
                if tmp == '' : 
                    cut_array[i,j] = None
                else :
                    cut_array[i,j] = float( tmp ) 

        return cut_array 

    

    def set( self, cuts ) :
        for i in range( self.size ) :
            for j in range(2) :
                # print( cuts[i][j] ) 
                if cuts[i][j] is None :
                    self.cut_entries[i,j].setText( '' )
                else :
                    self.cut_entries[i,j].setText( '%.3f' % cuts[i,j] )

        
        

class CutsDialog( QDialog ) :

    def __init__( self, parent ) :
        super().__init__()

        self.parent = parent 
        analyzer = parent.analyzer 
        
        self.setWindowModality( Qt.NonModal )

        self.setWindowTitle( 'Cut Options' )

        layout = QVBoxLayout() 
        self.setLayout( layout )

        apply_button = QPushButton( 'apply' ) 
        apply_button.clicked.connect( self.apply_button_clicked ) 
        layout.addWidget( apply_button ) 

        # self.position_cut_entry = CutEntry( analyzer.position_cut )
        # self.momentum_cut_entry = CutEntry( analyzer.momentum_cut )
        # self.total_momentum_cut_entry = CutEntry( analyzer.total_momentum_cut )

        self.position_cut_entry = CutEntry( 'position', 3 )
        self.momentum_cut_entry = CutEntry( 'momentum', 3 )
        self.total_momentum_cut_entry = CutEntry( 'total momentum', 1 )

        self.position_cut_entry.set( analyzer.position_cut.cuts )
        self.momentum_cut_entry.set( analyzer.momentum_cut.cuts )
        self.total_momentum_cut_entry.set( analyzer.total_momentum_cut.cuts ) 
        
        layout.addWidget( self.position_cut_entry )
        layout.addWidget( self.momentum_cut_entry )
        layout.addWidget( self.total_momentum_cut_entry ) 

        

        
    def apply_button_clicked( self ) :

        names = [ 'position cut', 'momentum cut', 'total momentum cut' ]

        targets = [ self.parent.analyzer.position_cut,
                    self.parent.analyzer.momentum_cut,
                    self.parent.analyzer.total_momentum_cut ]

        getters = [ self.position_cut_entry.get, self.momentum_cut_entry.get, self.total_momentum_cut_entry.get ] 
        
        for i in range( len( targets ) ) :
            tmp = getters[i]()
            targets[i].set( tmp ) 
            # if tmp :
            #     targets[i].set( tmp )
            # else :
            #     print( 'WARNING: unable to set ' + names[i] + ', cut is invalid' ) 

        self.parent.update_plots( _reload = 1 )
            
        # self.parent.data_loader.handle_timestep( self.parent.time_slider_widget.timestep,
        #                                          self.parent.time_slider_widget.stride,
        #                                          self.parent.time_slider_widget.max_timestep,
        #                                          _reload = 1 )

        # self.parent.plot_array.update( self.parent.time_slider_widget.timestep )
        
        # self.parent.reload_button_clicked() 




    
