# implements the class TristanDataAnalyzer. this class subclasses
# TristanDataContainer and hence gives access to all the same functionality
# as the data container itself. it also includes functions for computing and
# storing derived
# quantities, such as field magnitudes, etc. 
# included is much functionality necessary for real


import numpy as np

from .tristan_data_container import TristanDataContainer
from .helper_classes import AttrDict, RecursiveAttrDict


class TristanDataAnalyzer( TristanDataContainer ) :
    
    def __init__( self, data_path = None ) :

        # store all computed quantities 
        self.computations = None 

        # call __init__ from TristanDataContainer 
        super().__init__( data_path )
        
        # dictionary containing the function to be called to compute
        # the given quantity. each key maps to a function which takes one
        # argument, the index, which computes the quantity from available
        # tristan data. note that the data will not be loaded prior to the function
        # call 
        # if you want to add more computation functions,
        # just append to the dictionary accordingly, and compute_idx will
        # work with the new key and function if you request the data to be
        # computed. the default values here are not hard-coded anywhere.
        # better yet, i would recommend subclassing the TristanDataAnalyzer
        # (e.g. class TristanShockAnalyzer( TristanDataAnalyzer ) and implement
        # the functions there.
        self.computation_dict = { 'BB' : self.compute_BB,
                                  'EE' : self.compute_EE,
                                  'JJ' : self.compute_JJ,
                                  'ExB' : self.compute_ExB }

        
        # return the requiremnents for each computation:
        # first the quantities required, then the indices. this is crucial
        # for real-time computation and data-loading: this way only the
        # necessary data can be loaded if you aren't able to load all the
        # available data at once. each key has a function where the input
        # is the index to be computed, and then the required keys and indices.
        # as expected, just update this dict if you subclass and add more
        # computable quantities.
        self.computation_requirements_dict = {
            'BB' : lambda x : ( [x], [ 'bx', 'by', 'bz' ] ),
            'EE' : lambda x : ( [x], [ 'ex', 'ey', 'ez' ] )
        }
        
        
        # put empty values in the computations RecursiveAttrDict 
        self.computations = RecursiveAttrDict.empty( self.computation_dict.keys(),
                                                     len( self.data ) ) 

        
        # this dict is accessed by the GUI to print the available quantities
        # in latex. ignore if using TristanDataAnalyzer for offline analysis.
        # make sure to append to this dict any new quantities you make if
        # you want to be able to visualize them in the GUI.
        self.computation_key_dict = { 'BB' : r'$|B|^2$',
                                      'EE' : r'$|E|^2$',
                                      'JJ' : r'$|J|^2$',
                                      'ExB' : r'$E\times B$' } 

        
    # analagous to the data-loading implementation of TristanDataContainer.
    # here we can compute quantities at given indices and keys instead of all.
    # if recompute is not 0, then the key will be computed even if already loaded.
    def compute_indices( self, indices = None, keys = None, recompute = 0 ) :

        if indices is None :
            indices = np.arange( len( self.computations ) )
            
        # check scalar 
        if not hasattr( indices, '__len__' ) :
            indices = [ indices ] 
        
        # default: compute everything. not recommended. 
        if keys is None :
            keys = self.computation_dict.keys()

        for idx in indices :
            # don't compute if already computed, else compute 
            for key in keys :
                if ( not recompute ) and self.computations[ key ][ idx ] :
                    continue
                self.computation_dict[ key ]( idx ) 


    # unload data
    # indices = None -> unload all indices 
    # keys = None -> unload all keys 
    def uncompute_indices( self, indices = None, keys = None ) : 

        if indices is None :
            indices = np.arange( len( self.computations ) ) 
        
        # check scalar 
        if not hasattr( indices, '__len__' ) :
            indices = [ indices ] 
        
        # default: compute everything. not recommended. 
        if keys is None :
            keys = self.computation_dict.keys()

        for idx in indices :
            for key in keys :
                self.computations[ idx ][ key ] = None

                

    ######################################################3
    # ANALYSIS FUNCTIONS

    def compute_BB( self, idx ) :
        self.computations.BB[ idx ] = vector_norm_squared( [ self.data.bx[idx],
                                                             self.data.by[idx],
                                                             self.data.bz[idx] ] ) 

        
    def compute_EE( self, idx ) :
        self.computations.EE[ idx ] = vector_norm_squared( [ self.data.ex[idx],
                                                             self.data.ey[idx],
                                                             self.data.ez[idx] ] ) 

        
    def compute_JJ( self, idx ) :
        self.computations.JJ[ idx ] = vector_norm_squared( [ self.data.jx[idx],
                                                             self.data.jy[idx],
                                                             self.data.jz[idx] ] ) 

    def compute_ExB( self, idx ) :
        pass     
        

    def clear( self ) :

        # call clear method from TristanDataContainer 
        super().clear()
        
        if self.computations : 
            self.computations.clear() 
    

            
# compute squared vector norm of vector field formed with components
# given in the list components (e.g. components = [ np.array(32,32), np.array(32,32) ] )
# see compute_BB e.g. for example 
def vector_norm_squared( components ) : 
    return np.sum( [ x**2 for x in components ], axis = 0 )







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
