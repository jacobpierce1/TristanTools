import numpy as np
# from mayavi import mlab  
import sys


from .tristan_data_container import TristanDataContainer
from .helper_functions import check_spatial_dim 


# from .plotters import Plotter, VolumeSlicePlotter 

# these handle all the mlab functionality

# import sys                     
# sys.path.append( __file__ ) 

# import plotters 
from .plotters import * 


from collections import OrderedDict




# these are implemented in the directory plotters 
PLOTTERS_DICT = { 'volume_slice' : VolumeSlicePlotter,
                  'volume' : VolumePlotter, 
                  'vector_field' : VectorFieldPlotter,
                  'vector_cut_plane' : VectorCutPlanePlotter,
                  'hist1d' : Hist1dPlotter,
                  'flow' : FlowPlotter }




# store the keys for each type of data 
PLOT_NAME_TO_KEYS_DICT = OrderedDict( [
    ( 'B', [ 'bx', 'by', 'bz' ] ),
    ( 'E', [ 'ex', 'ey', 'ez' ] ),
    ( 'J', [ 'jx', 'jy', 'jz' ] ),
    ( 'V3', [ 'v3x', 'v3y', 'v3z' ] ),
    ( 'V3i', [ 'v3xi', 'v3yi', 'v3zi' ] )
] ) 

ALL_SCALARS = [ 'dens', 'densi',
                'bx', 'by', 'bz',
                'ex', 'ey', 'ez',
                'jx', 'jy', 'jz',
                'v3x', 'v3y', 'v3z',
                'v3xi', 'v3y', 'v3zi',
                'EE', 'BB', 'JJ', 'EB' ] 

ALL_VECTORS = [ 'E', 'B', 'J', 'V3', 'V3i' ]

# ALL_1D_SPECTRA_KEYS = [ 'PP_e_spec', 'PP_i_spec',
#                         'px_e_spec', 'py_e_spec', 'pz_e_spec',
#                         'px_i_spec', 'py_i_spec', 'pz_i_spec'   ] 


ALL_1D_SPECTRA_PLOT_NAMES = [ 'PP', 'px', 'py', 'pz' ] 


ALL_HISTS = []
ALL_HISTS.extend( ALL_1D_SPECTRA_PLOT_NAMES ) 



for x in ALL_SCALARS :
    PLOT_NAME_TO_KEYS_DICT[ x ] = [ x ] 

for x in ALL_HISTS :
    PLOT_NAME_TO_KEYS_DICT[ x ] = [ x + '_e_spec', x + '_i_spec' ]
    

# this is an orderedDict instead of regular dict so that the
# keys added are in the same order as they appear in the gui.
AVAILABLE_DATA_DICT = OrderedDict( [
    ( 'volume_slice', ALL_SCALARS ),
    ( 'volume', ALL_SCALARS ),
    ( 'vector_field', ALL_VECTORS ),
    ( 'vector_cut_plane', ALL_VECTORS ),
    ( 'hist1d', ALL_HISTS ),
    ( 'flow', ALL_VECTORS )
] )
    

    
# handle all the common functionality to 2d and 3d, such as saving
# images / movies, storing relevant variables such as data and plots,
# etc. the heavy lifting of plots is done in the plotter instance variable

class TristanDataPlotter( object ) :
    
    # inputs:
    # tristan_data_container: a TristanDataContainer object that will
    # be accessed for plotting the data. you are responsible for loading
    # the appropriate data as necessary in this object.
    # save_path (optional): directory in which to save files 
    def __init__( self, tristan_data_analyzer, plot_canvas = None,  save_path = None,
                  plot_type = None, plot_name = None, data_getter = None ) :


        self.available_data_dict = AVAILABLE_DATA_DICT

        self.plot_name_to_keys_dict = PLOT_NAME_TO_KEYS_DICT 


        # analyzer for accessing data and computations 
        self.analyzer = tristan_data_analyzer  

        # # mayavi plot for updating. a new one will be created if not supplied.
        # self.mayavi_scene = mayavi_scene
        # self.mayavi_plot = None 
        
        # path where movies and images can be saved. 
        self.save_path = save_path

        # the type of plot that will be plotted when self.plot() is called.
        # can always be changed later.
        self.plot_type = plot_type

        self.plot_name = plot_name

        # keys that will be used to access data in default data getter 
        if plot_name is not None : 
            self.keys = self.plot_name_to_keys_dict[ plot_name ] 


        # a new plot will be created if this is 1 and any function is called
        self.need_new_plot = 1
        
        
        # function that returns an array of the data given the index.
        # if manually specified, this allows enormous flexibility in
        # the plots that can be generated automatically.
        if data_getter :
            self.data_getter = data_getter
        else :
            self.data_getter = self.default_data_getter
        
        
        if save_path :
            print( 'INFO: creating directory: ' + save_path )
            os.makedirs( save_path, exist_ok = 1 )

            
        self.plotters_dict = PLOTTERS_DICT 


        # plot_canvas is either a mayavi_scene or a mpl axes. 
        self.plotter = self.plotters_dict[ self.plot_type ]( plot_canvas )

                
        
        self.timestep = None
        
            # self.plot_functions = { 'quiver3d' : self.quiver3d,
        #                         'volume_slice' : self.volume_slice }     

        # self.global_options = GlobalOptions( self.mayavi_scene ) 
        
            
        # if self.tristan_data.dim == 2 :
        #     self.plotter = Plotter2D( tristan_data_container )
        # elif self.tristan_data.dim == 3 :
        #     self.plotter = Plotter3D( tristan_data_container )


    # def change_plot_type( self, new_plot_type ) :
    #     self.plot_type = new_plot_type 
    #     self.plotter = self.plotters[ self.plot_type ]()
        
        
    # the data getter that is used if a custom one is not specified.
    # should be sufficient for pretty much all cases. please whatever you do,
    # don't put computations here, you should put them in the TristanDataAnalyzer
    # and then access here.
    def default_data_getter( self, timestep ) :
        return [ self.analyzer.data[key][timestep] for key in self.keys ]

    

    def set_plot_type( self, plot_type, plot_name ) :

        old_plot_type = self.plotter.get_type()
        old_canvas = self.plotter.get_canvas() 
        
        # self.plot_needs_clear = 1     
        self.plot_type = plot_type
        self.plot_name = plot_name 
        self.keys = self.plot_name_to_keys_dict[ plot_name ] 
            
        self.plotter.clear()

        self.plotter = self.plotters_dict[ self.plot_type ]( None ) 

        # if the plotter type has not changed, then use the old plotter canvas.
        # otherwise initialize the new plotter with no canvas.

        new_plot_type = self.plotter.get_type()

        if new_plot_type == old_plot_type :
            self.plotter.set_canvas( old_canvas ) 
        


    def set_plot_name( self, plot_name ) :
        self.plot_name = plot_name
        keys = self.plot_name_to_keys_dict[ plot_name ] 
        self.keys = keys 
        

            
    # change keys 
    def set_keys( self, keys ) :
        if len( keys ) != len( self.keys ) :
            print( 'ERROR: can\'nt change dimensionality of keys if plot type not changed.' )
            sys.exit( 0 ) 
                   
        self.keys = keys
    
        
    # def set_mayavi_scene( self, mayavi_scene ) :
    #     self.mayavi_scene = mayavi_scene
    #     self.plotter.mayavi_scene = mayavi_scene 

        
        
    def plot_timestep( self, timestep ) :
        # self.check_clear() 

        data = self.data_getter( timestep )

        # check for unloaded data. 
        for i in range( len( data ) ) :
            if data[i] is None : 
                print( 'ERROR: attempted to plot unloaded data: %s at timestep %d'
                       % ( self.keys[i], timestep ) )
                sys.exit( 1 )

        # self[ self.plot_type ]( data ) 
        # self.need_new_plot = 0

        # print( self.mayavi_scene ) 
        
        if timestep != self.timestep : 
            self.plotter.set_data( data ) 
            self.plotter.update() 
            
        self.timestep = timestep 


    # regenerate the existing plot if it has been cleared
    # should be called after the plot type is changed anad new
    # data has been set. 
    def refresh( self ) :

        # self.check_clear()
        data = self.data_getter( self.timestep )
        self.plotter.set_data( data ) 
        

    # def remove( self ) :
        # self.plotter.clear() 

        # if self.mayavi_scene : 
        #     self.mayavi_scene.remove()

        # if self.
        

    
    # save plot to file 
    def save_plot( self ) :
        pass 

    

    def get_plotter_type( self ) :
        return self.plotter.get_type()


    def get_plotter_canvas( self ) :
        return self.plotter.get_canvas() 


    def set_plotter_canvas( self, canvas ) :
        self.plotter.set_canvas( canvas ) 


    def clear( self ) :
        self.plotter.clear()


    def reset( self ) :
        self.clear() 
        self.refresh() 
