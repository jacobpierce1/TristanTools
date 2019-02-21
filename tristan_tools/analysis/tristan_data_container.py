# provides a class for reading tristan output data into a TristanData object
# functionality is provided for enhancing data analaysis speed by ignoring
# data that is not wished to be processed. for example, you can chooso to load
# just the fields (TristanDataContainer.load_fields() ) instead of loading all the
# data. same goes for particles or spectra. all h5py processing is handled here,
# it should not be necessary to use h5py anywhere else. 

import numpy as np
import os 
import glob
import sys
import h5py
import collections 

from pprint import pprint 

# from .helper_classes import AttrDictSeries, AttrDict
from .helper_classes import RecursiveAttrDict, AttrDict


# these are the file name prefixes in the tristan output. change these if you modify the
# names in tristan output. if you add a new category of tristan output then it should
# be trivial to mimic the current setup in TristanDataSlice and TristanDataContainer.

particles_prefix = 'prtl.tot'
fields_prefix = 'flds.tot'
spectra_prefix = 'spect'
params_prefix = 'param' 

all_prefixes = [ particles_prefix, fields_prefix, spectra_prefix, params_prefix ] 



class TristanError( Exception ) :
    pass 



                
class TristanDataContainer( object ) :

    def __init__( self, data_path = None ) :

        self.data_path = data_path 
        
        # stores time-dependent data: 
        self.data = RecursiveAttrDict() 

        # stores time-independent data: 
        self.params = AttrDict()

        if data_path :
            data_path += '/'
            self.set_data_path( data_path ) 

        # track all the indices that have data loaded 
        self.indices_with_data = set()
        # self._keys_at_prefix = {} 

        
        
    # set the data path and load parameters  
    def set_data_path( self, data_path ) : 
        
        # self.data_path = data_path

        if not os.path.exists( data_path ) :
            raise OSError( 'ERROR: data path %s not found' % data_path ) 
        
        # max index that the container will look to. note that you could manually set this
        # to cut off looking at higher-time data. 
        num_times = get_num_times( data_path )

        if num_times == 0 :
            raise TristanError( 'ERROR: data directory %s is empty' % data_path ) 
            
        self.clear()
        self.data.set_size( num_times ) 
            
        self.data_path = data_path

        self.load_params()
        self.load_keys() 


    
    # don't remove any of the data that is currently loaded, but resize
    # all the arrays appropriately. this is mainly useful in the gui when
    # you start a session before data collection has ended. 
    def reload_data_path( self ) :
        num_timesteps = get_num_times( self.data_path )
        self.data.set_size( num_timesteps ) 


        
        
    # # read all available data at once into the object
    # # before calling this function, make sure you have the resources to
    # # handle the amount of memory you are requesting.
    # def load_all( self  ) :
    #     self.load_indices( None ) 

        
    # # read all data from a particular index into the data structure 
    # def load_indices( self, indices ) :
    #     self.load_fields( indices )
    #     self.load_particles( indices )
    #     self.load_spectra( indices )
    #     self.load_time( indices ) 

        
    def load_times( self, indices = None, _reload = 0 ) : 
        self.load_indices( indices, params_prefix, [ 'time' ], _reload )
        
        
    def load_fields( self, indices = None, keys = None, _reload = 0 ) : 
        self.load_indices( indices, fields_prefix, keys, _reload ) 

        
    def load_particles( self, indices = None, keys = None, _reload = 0 ) :
        self.load_indices( indices, fields_prefix, keys, _reload ) 
        

    def load_spectra( self, indices = None, keys = None, _reload = 0 ) :
        self.load_indices( indices, spectra_prefix, keys, _reload ) 
        
            
    
    # load all available keys for time-dependent data (not params)
    # checks the file of index 0 (string = 000) for all the keys 
    def load_keys( self ) :

        print( 'INFO: loading keys' ) 
        
        # track the keys that belong to each of the time dependent data files
        self._keys_at_prefix = { spectra_prefix : set(),
                                 particles_prefix : set(),
                                 fields_prefix : set(),
                                 params_prefix : set() } 

        # set all time indices to None
        # note that by construction, self.data.time = None will not properly set all times to None,
        # it will actually delete the list and replace it with None.
        self.data[ 'time' ] = None  

        idx = 0
        for prefix in all_prefixes :
        
            fname = '%s/%s.%s' % ( self.data_path, prefix, idx_to_str( idx ) )
            try:
                with h5py.File( fname ) as f:
                    for key in f.keys() :

                        # set all indices to None
                        if prefix != params_prefix : 
                            self.data[ key ] = None
                        self._keys_at_prefix[ prefix ].add( key ) 
                        
            except OSError : 
                print( 'ERROR: file not found: %s' % fname ) 
                sys.exit(1)

        # in Tristan, the time is output in both particles and params. here we only use
        # the one from params.
        self._keys_at_prefix[ particles_prefix ].discard( 'time' )
                
        print( 'INFO: found keys in the following files:' )
        for key, val in self._keys_at_prefix.items() :
            print( '\t\t' + key + str( ' : ' ) + str( val ) )

            

        
    # note that reload is already a built in python funciton
    def load_indices( self, indices = None, prefixes = None, keys = None, _reload = 0 ) :
        
        if indices is None :
            indices = np.arange( len( self.data ) ) 
        
        # check scalar 
        if not hasattr( indices, '__len__' ) :
            indices = [ indices ] 

        if prefixes is None :
            prefixes = all_prefixes

        if not hasattr( prefixes, '__len__' ) :
            indices = [ prefixes ] 
            
        # default: loop through all keys
        if keys is None :
            keys = self.data.keys() 

        for prefix in prefixes : 
            _keys = set( keys ).intersection( self._keys_at_prefix[ prefix ] ) 
            
            for idx in indices : 

                self.indices_with_data.add( idx )
                
                fname = '%s/%s.%s' % ( self.data_path, prefix, idx_to_str( idx ) )

                # 1 for each key if it is to be reloaded.
                reload_statuses = {}
                for key in _keys :
                    reload_statuses[ key ] = _reload or ( self.data[key][idx] is None )

                # if all keys loaded then don't open file.
                if not any( reload_statuses ) :
                    # print( 'skipping, no keys'  ) 
                    continue

                # otherwise proceed to open and load the necessary keys.
                try:
                    with h5py.File( fname, 'r' ) as f:
                        for key in _keys :        
                            if reload_statuses[ key ] :
                                # print( 'set data: %s %d' % (key, idx ) )
                                self.data[ key ][ idx ] = f[ key ][:].T 
                                # print( key + ': ' + str( self.data[ key ][ idx ].shape ) ) 
                                
                except OSError :
                    print( 'ERROR: file not found: %s' % fname ) 
                    sys.exit(1)
                    
        # if 'time' in keys : 
        #     self.load_times( indices ) 


        

    def unload_indices( self, indices = None, keys = None ) :

        if indices is None : 
            indices = np.arange( len( self.data ) ) 
            
        if not hasattr( indices, '__len__' ) :
            indices = [ indices ] 
        
        if keys is None :
            keys = self.data.keys()

        for idx in indices : 
            for key in keys :
                self.data[ idx ][ key ] = None


                
    # load time-independent data 
    def load_params( self ) :
        fname = '%s/%s.%s' % ( self.data_path, params_prefix, '000' )
        # print( fname ) 
        try:
            with h5py.File( fname ) as f:
                for key in f.keys():
                    tmp = f[ key ][:]
                    try :
                        tmp = np.asscalar( tmp ) 
                        # print( key )
                    except :
                        pass
                    self.params[ key ] = tmp 
                    # print( self.params[key].shape )
                    # print( self.params ) 
        except OSError :
            print( 'ERROR: file not found: %s' % fname ) 
            sys.exit(1)


            
    def clear( self ) :
        self.params.clear()
        self.data.clear()
        self.data_path = None
        

        
    # check memory usage stats 
    def memory_usage( self ) :
        pass

    
        
    def print_keys( self ) :
        print( '***** PARAMS KEYS ***** ' )
        for key in sorted( self.params.keys() ) :
            print( key )
            
        print( '\n\n***** DATA KEYS ***** ' )
        for key in sorted( self.data.keys() ) :
            print( key ) 

            
    
    # print the shape of every key in params and data. 
    def print_shapes( self, idx ) :
        
        print( '***** PARAMS KEYS ***** ' )
        for key in sorted( self.params.keys() ) :
            try :
                shape = self.params[key].shape
                print( str( key ) + ': ' + str( shape )  )
            except : 
                print( str( key ) + ': scalar' )
                
        print( '\n\n***** DATA KEYS ***** ' )
        for key in sorted( self.data.keys() ) : 
            try :
                shape = self.data[key][idx].shape
                print( str( key ) + ': ' + str( shape ) )
            except : 
                print( str( key ) + ': scalar' )

                
            
    def __len__( self  ) :
        return len( self.data )

    
        
    def __repr__( self ) :
        return repr( self.data )


    
    def __str__( self ) :
        return str( self.data )

    
        
    # todo 
    def set_dim( self ) :
        self.dim = 3 

        
            
# helper functions
def idx_to_str( idx ) :
    return '%03d' % idx 



def get_num_times( output_path ) :    
    num_files = len( glob.glob( output_path + 'spect.*' ) ) 
    return num_files

                                   
