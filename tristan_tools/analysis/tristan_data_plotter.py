import numpy as np
from mayavi import mlab  

from .tristan_data_container import TristanDataContainer
from .helper_functions import check_spatial_dim 


# from .plotters import Plotter, VolumeSlicePlotter 

# these handle all the mlab functionality

# import sys                     
# sys.path.append( __file__ ) 

# import plotters 
from .plotters import * 


from collections import OrderedDict



# store the keys for each type of data 
DATA_NAME_TO_KEYS_DICT = OrderedDict( [
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
                'EE', 'BB', 'JJ' ] 

ALL_VECTORS = [ 'E', 'B', 'J', 'V3', 'V3i' ] 


# these are implemented in the directory plotters 
PLOTTERS_DICT = { 'volume_slice' : VolumeSlicePlotter,
                  'volume' : VolumePlotter, 
                  'vector_field' : VectorFieldPlotter,
                  'vector_cut_plane' : VectorCutPlanePlotter }



for x in ALL_SCALARS :
    DATA_NAME_TO_KEYS_DICT[ x ] = [ x ] 


# this is an orderedDict instead of regular dict so that the
# keys added are in the same order as they appear in the gui.
AVAILABLE_DATA_DICT = OrderedDict( [
    ( 'volume_slice', ALL_SCALARS ),
    ( 'volume', ALL_SCALARS ),
    ( 'vector_field', ALL_VECTORS ),
    ( 'vector_cut_plane', ALL_VECTORS )
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
    def __init__( self, tristan_data_analyzer, keys = None, mayavi_scene = None,
                  save_path = None, plot_type = None, data_getter = None ) :

        # analyzer for accessing data and computations 
        self.analyzer = tristan_data_analyzer  

        # keys that will be used to access data 
        self.keys = keys

        # mayavi plot for updating. a new one will be created if not supplied.
        self.mayavi_scene = mayavi_scene
        self.mayavi_plot = None 
        
        # path where movies and images can be saved. 
        self.save_path = save_path

        # the type of plot that will be plotted when self.plot() is called.
        # can always be changed later.
        self.plot_type = plot_type

        # will be called by plot() if the plot needs to be cleared
        self.plot_needs_clear = 0 

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


        self.plotter = self.plotters_dict[ self.plot_type ]( self.mayavi_scene )


        self.available_data_dict = AVAILABLE_DATA_DICT

        self.data_name_to_keys_dict = DATA_NAME_TO_KEYS_DICT 
                
        
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

    

    def set_plot_type( self, plot_type, keys ) :
        self.plot_needs_clear = 1     
        self.plot_type = plot_type
        self.keys = keys
        self.plotter.clear() 
        self.plotter = self.plotters_dict[ self.plot_type ]( self.mayavi_scene ) 
        

    # change keys 
    def set_keys( self, keys ) :
        if len( keys ) != len( self.keys ) :
            print( 'ERROR: can\'nt change dimensionality of keys if plot type not changed.' )
            sys.exit( 0 ) 
                   
        self.keys = keys
    
        
    # def check_clear( self ) :
    #     if self.plot_needs_clear :
    #         self.clear() 


            
    # def clear( self ) :
    #     self.mayavi_plot.clear()
    #     self.need_new_plot = 1 

        
        
    def plot_timestep( self, timestep ) :
        # self.check_clear() 
        data = self.data_getter( timestep )
        # self[ self.plot_type ]( data ) 
        # self.need_new_plot = 0
            
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
        

        
    # # used to access the plotting functions
    # # e.g. self[ 'quiver3d' ] is the same as self.quiver3d
    # def __getitem__( self, item ) :
    #     return self.plot_functions[ item ]      
        

    
    # save plot to file 
    def save_plot( self ) :
        pass 

    

    # def plot_field( self, field_name ) :
    #     pass
    
    # def quiver_plot_3d( self, key1, key2, key3, mayavi_ax = None ) :
    #     pass # mayavi_ax = mlab.

    # def volume_slice( self, data ) :
    #     if self.need_new_plot :
    #         self.mayavi_plot = mlab.volume_slice( data[0], plane_orientation = 'z_axes',
    #                                               figure = self.mayavi_scene )
    #         mlab.outline( figure = self.mayavi_scene ) 
    #     else :
    #         self.mayavi_plot.mlab_source.trait_set( scalars = data[0] )             


            
    # def quiver3d( self, data ) :
    #     if self.need_new_plot :
    #         self.mayavi_plot = mlab.quiver3d( *data, figure = self.mayavi_scene ) 
    #         mlab.outline( figure = self.mayavi_scene ) 
    #     else :
    #         self.mayavi_plot.mlab_source.trait_set( u=data[0], v=data[1], w=data[2] )






    

        



# class 



        
            
    # def set_tristan_data( self, tristan_data_container ) :
    #     self.tristan_data = tristan_data_container 




    

# # this class (as well as Plotter3D) provides all the functionality for
# # making nice plots from the data, but does not have any functionality for saving plots
# # and does not store any other variables that are generically handled in both the
# # 2d and 3d cases. 

# class Plotter2D( object ) :
            
#     def __init__( self, tristan_data_container ) :
#         self.tristan_data_container = tristan_data_container 

        
#     # plot a single field component or scalar in the 2D simulation plane.
#     # name: 'dens', 'bx', 'jz', etc. 
#     def plot_scalar( self, name ) : 
#         pass

#     # create 2D quiver plot in the simulation plane of 
#     def plot_quiver_2d( self, vector1_name, vector2_name ) :
#         pass

#     # create 3d quiver plot in simulation plane
#     def plot_quiver_3d( self, v1, v2, v3 ) :
#         pass     

#     def phase_plot( self, name  ) :
#         pass



    
# # same idea as Plotter2D: handles specific plots for spatially 3D
# # data, but nothing more general such as saving plots etc. 
# class Plotter3D( object ) : 

#     def __init__( self, tristan_data_container ) :
#         self.tristan_data_container = tristan_data_container 

#     # input: 3d array,
#     def plot_slice( self, array_3d ) : 
#         pass
