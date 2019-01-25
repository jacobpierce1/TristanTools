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
tristan_particles_prefix = 'prtl.tot'
tristan_fields_prefix = 'flds.tot'
tristan_spectra_prefix = 'spect'
tristan_params_prefix = 'param' 
                

                
class TristanDataContainer( object ) :

    def __init__( self, data_path ) :

        # stores all parameters. the parameter names are also set to be the names of attributes
        # for convenience.
        self.params = {} 

        if not os.path.exists( data_path ) :
            print( 'ERROR: data path %s not found' % data_path ) 
            sys.exit(0)
        
        self.data_path = data_path 

        # max index that the container will look to. note that you could manually set this
        # to cut off looking at higher-time data. 
        num_times = get_num_times( data_path )

        if num_times == 0 :
            print( 'WARNING: output directory %s is empty' % self.data_path ) 

        # stores time-dependent data in an array which will contain a bunch of TristanDataSlice's 
        # self.data = [ AttrDict() for i in range( self.num_times ) ]
        self.data = RecursiveAttrDict( size = num_times ) 
        self.params = AttrDict()

        self.load_keys() 
        self.load_params()

        self.set_dim() 
        
        
    # read all available data at once into the object
    # before calling this function, make sure you have the resources to
    # handle the amount of memory you are requesting.
    def load_all( self  ) :
        self.load_indices( None ) 

        
    # read all data from a particular index into the data structure 
    def load_indices( self, indices ) :
        self.load_fields( indices )
        self.load_particles( indices )
        self.load_spectra( indices )
        self.load_time( indices ) 

        
    def load_time( self, indices = None ) : 
        if indices is None :
            indices = range( self.num_times ) 
        for idx in indices :
            self.load_data_at_idx( tristan_params_prefix, idx, keys = [ 'time' ] ) 

        
    def load_fields( self, indices = None ) : 
        if indices is None :
            indices = range( self.num_times ) 
        for idx in indices :
            self.load_data_at_idx( tristan_fields_prefix, idx ) 

            
    def load_particles( self, indices = None ) :
        if indices is None :
            indices = range( self.num_times ) 
        for idx in indices :
            self.load_data_at_idx( tristan_particles_prefix, idx ) 

            
    def load_spectra( self, indices = None ) :
        if indices is None :
            indices = range( self.num_times ) 
        for idx in indices : 
            self.load_data_at_idx( tristan_spectra_prefix, idx ) 

        
    # def load_time_at_idx( self, idx, init = 0 ) :
    #     fname = '%s/%s.%s' % ( self.data_path, tristan_params_prefix, idx_to_str( idx ) )
    #     try:
    #         with h5py.File( fname ) as f:
    #             self.data[ 'time' ][ idx ] = f[ 'time' ][:] 
    #     except:
    #         print( 'ERROR: file not found: %s' % fname ) 
    #         sys.exit(1)

    
    
    # load all available keys for time-dependent data (not params)
    # checks the file of index 0 (string = 000) for all the keys 
    def load_keys( self ) :
        self.data.set_key( 'time' ) 

        idx = 0
        for prefix in [ tristan_spectra_prefix, tristan_particles_prefix, tristan_fields_prefix ] :
        
            fname = '%s/%s.%s' % ( self.data_path, prefix, idx_to_str( idx ) )
            try:
                with h5py.File( fname ) as f:
                    for key in f.keys() :
                        self.data.set_key( key )

            except OSError : 
                print( 'ERROR: file not found: %s' % fname ) 
                sys.exit(1)

    

    # init = 1 will create an empty array in self.data to store future data
    # keys = [ ... ] will loop through the specified keys instead of loading all
    def load_data_at_idx( self, prefix, idx, keys = None ) :

        # print( prefix ) 
        # print(idx)
                
        fname = '%s/%s.%s' % ( self.data_path, prefix, idx_to_str( idx ) )
        try:
            with h5py.File( fname ) as f:

                # default: loop through all keys
                if keys is None :
                    keys = f.keys() 
                
                for key in keys:
                    self.data[ key ][ idx ] = f[ key ][:] 

        except OSError :
            print( 'ERROR: file not found: %s' % fname ) 
            sys.exit(1)

                            
    def load_params( self ) :
        fname = '%s/%s.%s' % ( self.data_path, tristan_params_prefix, '000' )
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

    def reload( self ) :
        pass 

    def clear( self ) :
        pass

    # check memory usage stats 
    def memory_usage( self ) :
        pass

    def print_keys( self ) :
        print( '***** PARAMS KEYS ***** ' )
        for key in self.params.keys() :
            print( key )
            
        print( '\n\n***** DATA KEYS ***** ' )
        for key in self.data.keys() :
            print( key ) 
        
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

    
# note: this will fail if any other files are added to the output directory! 
def get_num_times( output_path ) :
    # print( os.listdir( output_path ) )
    
    num_files = len([name for name in os.listdir( output_path )])
    return num_files // 4 

                                   

# def _get_fname(var, path):
#     _fnames = {'param' : os.path.join(path, 'output/param.{}'),
#                'field' : os.path.join(path, 'output/flds.tot.{}'),
#                'parts' : os.path.join(path, 'output/prtl.tot.{}'),
#                'spect' : os.path.join(path, 'output/spect.{}')}
#     return _fnames[var]


    

# def load_trist(vars='all', path='./', num=None, verbose=False):
#     if type(vars) == str:
#         if vars == 'all':
#             _ftypes = ['param', 'field', 'parts', 'spect']
#         else:
#             _ftypes = vars.split()
#         else:
#             _ftypes = vars

#     if 'param' not in _ftypes:
#         _ftypes.append('param')

#     ad = {}

#     choices = get_output_times(path)
#     while num not in choices:
#         _ =  'Select from the following possible movie numbers: '\
#              '\n{0} '.format(choices)
#         num = int(raw_input(_))

#     num = '{:03d}'.format(num)

    

    # ad['xx'] = np.arange(ad['mx0'][0])/(ad['c_omp'][0])
    # ad['yy'] = np.arange(ad['my0'][0])/(ad['c_omp'][0])
    # #print ad['v3x'].shape[2]
    # #print ad['xx']
    # #print ad['c_omp']

    # return ad

#======================================================================

# def get_output_times(path='./', var='field'):
    
#     #dpath = os.path.join(path, _get_fname(var, path).format('*'))
#     dpath = _get_fname(var, path).format('*')
#     choices = glob.glob(dpath)
#     choices = [int(c[-3:]) for c in choices]
#     choices.sort()
#     return np.array(choices)


# def odp(d, v, ax=None, **kwargs):
#     if ax is None:
#         import matplotlib.pyplot as plt
#         ax = plt.gca()
#         if type(v) ==  str:
#             v = d[v]

#     return ax.plot(d['xx'], np.mean(np.squeeze(v), axis=0), **kwargs)


    
def calc_psi(f):
    """ Calculated the magnetic scaler potential for a 2D simulation
    Args:
        d (dict): Dictionary containing the fields of the simulation
            d must contain bx, by, xx and yy
    Retruns:
        psi (numpy.array(len(d['xx'], len(d['yy']))) ): Magnetic scaler
            potential
    """

    bx = np.squeeze(f['bx'])
    by = np.squeeze(f['by'])
    dx = dy = 1./f['c_omp']

    psi = 0.0*bx
    psi[1:,0] = np.cumsum(bx[1:,0])*dy
    psi[:,1:] = (psi[:,0] - np.cumsum(by[:,1:], axis=1).T*dx).T

    return psi.T


