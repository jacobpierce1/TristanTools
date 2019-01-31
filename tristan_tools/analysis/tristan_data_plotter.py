import numpy as np
from mayavi import mlab  

from .tristan_data_container import TristanDataContainer
from .helper_functions import check_spatial_dim 


    

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

        self.plot_functions = { 'quiver3d' : self.quiver3d,
                                'volume_slice' : self.volume_slice }     
             
            
        # if self.tristan_data.dim == 2 :
        #     self.plotter = Plotter2D( tristan_data_container )
        # elif self.tristan_data.dim == 3 :
        #     self.plotter = Plotter3D( tristan_data_container )

        
    # the data getter that is used if a custom one is not specified.
    # should be sufficient for pretty much all cases. please whatever you do,
    # don't put computations here, you should put them in the TristanDataAnalyzer
    # and then access here.
    def default_data_getter( self, timestep ) :
        return [ self.analyzer.data[key][timestep] for key in self.keys ]


    def set_plot_type( self, plot_type ) :
        self.plot_needs_clear = 1     
        self.plot_type = plot_type


    def check_clear( self ) :
        if self.plot_needs_clear :
            self.clear() 


    def clear( self ) :
        self.mayavi_plot.clear()
        self.need_new_plot = 1 
        
        
    def plot_timestep( self, timestep ) :
        self.check_clear() 
        data = self.data_getter( timestep )
        self[ self.plot_type ]( data ) 
        self.need_new_plot = 0
        self.timestep = timestep 

        
    # used to access the plotting functions
    # e.g. self[ 'quiver3d' ] is the same as self.quiver3d
    def __getitem__( self, item ) :
        return self.plot_functions[ item ]      
        
            
    # save plot to file 
    def save_plot( self ) :
        pass 


    # def plot_field( self, field_name ) :
    #     pass
    
    # def quiver_plot_3d( self, key1, key2, key3, mayavi_ax = None ) :
    #     pass # mayavi_ax = mlab.

    def volume_slice( self, data ) :
        if self.need_new_plot :
            self.mayavi_plot = mlab.volume_slice( data[0], plane_orientation = 'z_axes',
                                                  figure = self.mayavi_scene )
            mlab.outline( figure = self.mayavi_scene ) 
        else :
            self.mayavi_plot.mlab_source.trait_set( scalars = data[0] )             

    def quiver3d( self, data ) :
        if self.need_new_plot :
            self.mayavi_plot = mlab.quiver3d( *data, figure = self.mayavi_scene ) 
            mlab.outline( figure = self.mayavi_scene ) 
        else :
            self.mayavi_plot.mlab_source.trait_set( u=data[0], v=data[1], w=data[2] )

        
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
