import numpy as np
import mayavi 

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
    def __init__( self, tristan_data_container, save_path = None ) :

        self.tristan_data = tristan_data_container
        self.save_path = save_path

        if save_path :
            print( 'INFO: creating directory: ' + save_path )
            os.makedirs( save_path, exist_ok = 1 )

        if self.tristan_data.dim == 2 :
            self.plotter = Plotter2D( tristan_data_container )
        elif self.tristan_data.dim == 3 :
            self.plotter = Plotter3D( tristan_data_container )
            
            
    # save plot to file 
    def save_plot( self ) :
        pass 


    # clear all active plots 
    def clear( self ) :
        pass

    def plot_field( self, field_name ) :
        pass
    
    def quiver_plot_3d( self, key1, key2, key3, mayavi_ax = None ) :
        pass # mayavi_ax = mlab.

        
    # def set_tristan_data( self, tristan_data_container ) :
    #     self.tristan_data = tristan_data_container 




    

# this class (as well as Plotter3D) provides all the functionality for
# making nice plots from the data, but does not have any functionality for saving plots
# and does not store any other variables that are generically handled in both the
# 2d and 3d cases. 

class Plotter2D( object ) :
            
    def __init__( self, tristan_data_container ) :
        self.tristan_data_container = tristan_data_container 

        
    # plot a single field component or scalar in the 2D simulation plane.
    # name: 'dens', 'bx', 'jz', etc. 
    def plot_scalar( self, name ) : 
        pass

    # create 2D quiver plot in the simulation plane of 
    def plot_quiver_2d( self, vector1_name, vector2_name ) :
        pass

    # create 3d quiver plot in simulation plane
    def plot_quiver_3d( self, v1, v2, v3 ) :
        pass     

    def phase_plot( self, name  ) :
        pass



    
# same idea as Plotter2D: handles specific plots for spatially 3D
# data, but nothing more general such as saving plots etc. 
class Plotter3D( object ) : 

    def __init__( self, tristan_data_container ) :
        self.tristan_data_container = tristan_data_container 

    # input: 3d array,
    def plot_slice( self, array_3d ) : 
        pass
