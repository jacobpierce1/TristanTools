# provides a class for reading TristanData into a TristanData object

import numpy as np
import os 
import glob
import sys
import h5py



class TristanData( object ) :

    def __init__( data_path ) :

        if not os.path.exists( data_path ) :
            print( 'ERROR: data path %s not found' % data_path ) 
            sys.exit(0)
        
        self.data_path = data_path 
        self.max_index = get_max_index( data_path ) 
        
    
    # read all data from a particular index into the data structure 
    def read_index( idx ) :
        for file_type in ['param', 'field', 'parts', 'spect'] : 
            fname = '%s.%s.%s' % ( self.data_path, file_type, idx_to_str( idx )
            try:
                with h5py.File( fname ) as f:
                    for key in f.keys():
                        ad[k] = f[k][:]
            except:
                print( 'ERROR: file not found: %s' % fname ) 
                            
                            
    # read all available data at once into the object
    # before calling this function, make sure you have the resources to
    # handle the amount of memory you are requesting.
    def read_all( self  ) :
        for i in range( self.max_index ) :
            self.read_index( idx ) 
            
            
    def reload( self ) :
        pass 

    def clear( self ) :
        pass

        
            
# helper functions
def idx_to_str( idx ) :
    return '%03d' % idx 



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

def get_output_times(path='./', var='field'):
    
    #dpath = os.path.join(path, _get_fname(var, path).format('*'))
    dpath = _get_fname(var, path).format('*')
    choices = glob.glob(dpath)
    choices = [int(c[-3:]) for c in choices]
    choices.sort()
    return np.array(choices)


def odp(d, v, ax=None, **kwargs):
    if ax is None:
        import matplotlib.pyplot as plt
        ax = plt.gca()
        if type(v) ==  str:
            v = d[v]

    return ax.plot(d['xx'], np.mean(np.squeeze(v), axis=0), **kwargs)


    
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


