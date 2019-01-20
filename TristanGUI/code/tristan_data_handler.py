import numpy as np




class TristanData( object ) :

    # size = number of timesteps that the container will store
    # by default not all data is loaded. the data is loaded only if load_index
    # or load_all is called. this way you don't load any data that you don't need.
    # path is the directory of the tristan output data 
    def __init__( self, size, dim, path  ) :

        pass

        
    # extend all arrays to have the new length. since numpy arrays
    # are used, this is computationally inefficient. this is only called
    # when the user requests to load new data into an existing TristanData.
    def extend( self, newsize ) :
        pass

        
    # load data at the requested index 
    def load_index( self, index ) :
        pass


    # load all data. never called by GUI
    def load_all( self )  :
        pass     

        
    # clear all data 
    def clear( self ) :
        pass 
