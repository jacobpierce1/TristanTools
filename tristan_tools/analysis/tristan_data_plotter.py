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

            
        self.plotters = { 'volume_slice' : VolumeSlice,
                          'quiver3d' : Quiver3D }


        self.plotter = self.plotters[ self.plot_type ]( self.mayavi_scene ) 

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
        self.plotter = self.plotters[ self.plot_type ]( self.mayavi_scene ) 
        

    # change keys 
    def set_keys( self, keys ) :
        if len( keys ) != len( self.keys ) :
            print( 'ERROR: can\'nt change dimensionality of keys if plot type not changed.' )
            sys.exit( 0 ) 
                   
        self.keys = keys
    
        
    def check_clear( self ) :
        if self.plot_needs_clear :
            self.clear() 


            
    def clear( self ) :
        self.mayavi_plot.clear()
        self.need_new_plot = 1 

        
        
    def plot_timestep( self, timestep ) :
        self.check_clear() 
        data = self.data_getter( timestep )
        # self[ self.plot_type ]( data ) 
        # self.need_new_plot = 0
            
        if timestep != self.timestep : 
            self.plotter.set_data( data ) 
            self.plotter.update() 
            
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






    


# this class and its subclasses handle all mayavi plotting functionality
# divorced from the TristanDataContainer 
# here is the functionality that will be used by all the plotters. 

class Plotter( object ) :

    def __init__( self, mayavi_scene ) : 
        self.mayavi_scene = mayavi_scene
        # self.mayavi_plot = None
        self.needs_update = 1 

        self.orientation_axes = None
        
        
        self.orientation_axes_state = 0
        self.outline_state = 0 
        
        # self.actions = [ self.toggle_orientation_axes ]
        # self.actions_descriptions = [ 'toggle orientation axes' ] 


    def set_orientation_axes( self, state ) :

        if state :

            # already exists x
            if self.orientation_axes_state :
                return 
            
            self.orientation_axes = mlab.orientation_axes( figure = self.mayavi_scene ) 
            self.orientation_axes_state = 1 
            
        # remove 
        else :

            #already removed 
            if not self.orientation_axes_state :
                return
            
            self.orientation_axes.remove() 
            self.orientation_axes_state = 0 
            


            
    def set_outline( self, state ) :

        if state :

            # already exists x
            if self.outline_state :
                return 
            
            self.outline = mlab.outline( figure = self.mayavi_scene ) 
            self.outline_state = 1 
            
        # remove 
        else :

            #already removed 
            if not self.outline_state :
                return
            
            self.outline.remove() 
            self.outline_state = 0 
            


    def clear( self ) :
        mlab.clf( figure = self.mayavi_scene ) 
            
        
    # to be implemented by subclasses 
    def update( self ) :
        pass


    # def set_title( self, title ) :

    #     # if not title :
    #     #     title = self.plot_type 

    #     print( self.mayavi_scene ) 
    #     mlab.title( title, figure = self.mayavi_scene )

        
    
    # # does not need to be reimplemented for subclasses
    # def reset( self ) :
    #     # self.mayavi_scene.clear()
    #     mlab.clf( figure = self.mayavi_scene ) 
    #     self.__init__( self.mayavi_scene ) 
    #     # self.set_data( self.data ) 
        
    # def set_data( data ) :
    #     self.data = data 


    
        

# allows you to control up to 3 volume slices 
class VolumeSlice( Plotter ) :

    def __init__( self, mayavi_scene, data = None ) :
        super().__init__( mayavi_scene ) 

        self.data = data
        
        # variable storing each of the 3 addable /removable slices 
        self.mayavi_plots = [ None, None, None ]

        # these slices are added on the next
        # set defaults here 
        self.slices_to_add = [ 1, 0, 0 ] 

        # add default slices if possible. only works if data already is loaded,
        # which means that this only goes through if reset is called 
        for i in range( 3 ) :
            if self.slices_to_add[i] :
                self.add_slice( i )

                
    def reset( self ) :
        mlab.clf( figure = self.mayavi_scene ) 
        self.__init__( self.mayavi_scene, data = self.data ) 
        
        
    # axis can be 0, 1, or 2 
    def add_slice( self, axis ) :

        # if we don't have data yet, then just add the slice next time we receive data.
        if self.data is None :
            self.slices_to_add[ axis ] = 1
            return 
        
        # do nothing if axis already created. 
        if self.mayavi_plots[ axis ] :
            return 

        try :
            tmp = [ 'x', 'y', 'z' ][ axis ] + '_axes' 
        except : 
            print( 'ERROR: axis must be 0, 1, or 2' )
            sys.exit(1)

        self.mayavi_plots[ axis ] = mlab.volume_slice( self.data, plane_orientation = tmp,
                                                       slice_index = self.data.shape[ axis ] / 2 )
        
        
    def remove_slice( self, axis ) :
        if self.mayavi_plots[ axis ] :
            self.mayavi_plots[ axis ].remove()
            self.mayavi_plots[ axis ] = None
            
        
    def set_data( self, data ) :


        # init is 1 if the data has not been set yet 
        init = 0
        if self.data is None :
            init = 1 
        
        self.data = data[0]

        # add any slices that couldn't be added before we had data
        # once there is data, they can just be added automatically without using slices_to_add.
        if init :
            for i in range(3) :
                if self.slices_to_add[i] :
                    self.add_slice( i ) 
        
        for mayavi_plot in self.mayavi_plots : 
            if mayavi_plot : 
                mayavi_plot.mlab_source.trait_set( scalars = self.data )

                # self.data = 

                
    # def update( self, data ) :
    #     super().update( data )
    #     for i in range( 3 ) :
            

    def encode( self ) :
        return

    
    @classmethod 
    def decode( cls, self ) :
        return 
            
# # functions to modify quiver3d plots 
# class Quiver3dOptions( object ) :
#     pass
        


class Quiver3D( Plotter ) :

    pass 


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
