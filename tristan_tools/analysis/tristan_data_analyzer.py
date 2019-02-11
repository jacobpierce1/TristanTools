# implements the class TristanDataAnalyzer. this class subclasses
# TristanDataContainer and hence gives access to all the same functionality
# as the data container itself. it also includes functions for computing and
# storing derived
# quantities, such as field magnitudes, etc. 
# included is much functionality necessary for real


import numpy as np
import sys
import os
import h5py



from .tristan_data_container import TristanDataContainer
# from .helper_classes import AttrDict, RecursiveAttrDict





class TristanDataAnalyzer( TristanDataContainer ) :
    
    def __init__( self, data_path = None, computations_path = None, spectra_nbins = 1000 ) :

        # store all computed quantities 
        # self.computations = None 

        # call __init__ from TristanDataContainer 
        super().__init__( data_path )

        if computations_path is None :
            computations_path = self.data_path + '../computations/'

        self.computations_path = computations_path 

        if os.path.exists( computations_path ) :
            print( 'INFO: found computations directory: ' + computations_path ) 

        else : 
            try : 
                print( 'INFO: creating computations directory: ' + computations_path )
                os.makedirs( self.computations_path, exist_ok = 1 )

            except OSError : 
                print( 'ERROR: unable to create computations directory: %s' % self.computations_path )
                sys.exit( 1 ) 
                
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
        # (e.g. class TristanShockAnalyzer( TristanDataAnalyzer ) or
        # class JetAnalyzer( Analyzer ) and implement specific functions there.
        self.computation_callbacks = { 'BB' : self.compute_BB,
                                       'EE' : self.compute_EE,
                                       'JJ' : self.compute_JJ,
                                       'ExB' : self.compute_ExB } 
                                       # 'momentum_spectra' : self.compute_momentum_spectra }
                                       
        # add momentum spectrum computers:
        components = 'xyz'
        for particle_type in 'ei' :
            for i in range(3) :
                key = 'p' + components[i] + '_' + particle_type + '_spec' 
                self.computation_callbacks[ key ] = (
                    lambda idx, p = particle_type, i = i :
                    self.compute_momentum_component_spectrum( idx, p, i ) )

            # total momentum computer
            key = 'PP_' + particle_type + '_spec'
            self.computation_callbacks[ key ] = (
                lambda idx, p = particle_type : self.compute_total_momentum_spectrum( idx, p ) )
                                                                                                  
                                       
        self.computation_keys = set( self.computation_callbacks.keys() )
        
        
        # # return the requiremnents for each computation:
        # # first the quantities required, then the indices. this is crucial
        # # for real-time computation and data-loading: this way only the
        # # necessary data can be loaded if you aren't able to load all the
        # # available data at once. each key has a function where the input
        # # is the index to be computed, and then the required keys and indices.
        # # as expected, just update this dict if you subclass and add more
        # # computable quantities.
        # self.computation_requirements_dict = {
        #     'BB' : lambda x : ( [x], [ 'bx', 'by', 'bz' ] ),
        #     'EE' : lambda x : ( [x], [ 'ex', 'ey', 'ez' ] )
        # }

        
        # we store all computations in the same RecursiveAttrDict as created in the parent
        # TristanDataContainer.
        for key in self.computation_keys :
            self.data[ key ] = None
        

        # # this allocates space for more keys 
        # self.compute_momentum_spectra( 0, init = 1 )     
            
        # this dict is accessed by the GUI to print the available quantities
        # in latex. ignore if using TristanDataAnalyzer for offline analysis.
        # make sure to append to this dict any new quantities you make if
        # you want to be able to visualize them in the GUI.
        self.computation_key_descriptions_dict = { 'BB' : r'$|B|^2$',
                                                   'EE' : r'$|E|^2$',
                                                   'JJ' : r'$|J|^2$',
                                                   'ExB' : r'$E\times B$' } 
        



    def get_computations_file( self, idx ) :
        return ( self.computations_path + 'computations.%d' % idx )

        
    # analagous to the data-loading implementation of TristanDataContainer.
    # here we can compute quantities at given indices and keys instead of all.
    # if recompute is not 0, then the key will be computed even if already loaded.
    def compute_indices( self, indices = None, keys = None, recompute = 0, save = 1 ) :

        if indices is None :
            indices = np.arange( len( self ) )
            
        # check scalar 
        if not hasattr( indices, '__len__' ) :
            indices = [ indices ] 
        
        # default: compute everything. not recommended. 
        if keys is None :
            _keys = self.computation_keys
        else :
            _keys = self.computation_keys & set( keys ) 
        
        for idx in indices :
            
            # we need access to the file if we are either saving or loading from memory.
            if ( not recompute ) or save : 
        
                # append mode: Read/write if exists, create otherwise (default)
                with h5py.File( self.get_computations_file( idx ), 'a' ) as f : 

                    # keys that are already in the dataset
                    existing_keys = set( f.keys() )
                    # print( 'existing keys: ' + str( existing_keys ) )
                    
                    if not recompute : 
                        keys_to_compute = _keys - existing_keys  
                        

                        for key in existing_keys :
                            self.data[ key ][ idx ] = np.array( f[ key ] ) 

                    # otherwise declare that no keys have been computed
                    else :
                        keys_to_compute = _keys

                    # print( 'keys_to_compute: ' + str( keys_to_compute ) ) 
                        
                    # compute keys that were not in the file, then write them. 
                    for key in keys_to_compute :

                        # the callback returns a list of all the keys it computed
                        # if it isn't just the name of the key used to call the callback.
                        computed_keys = self.computation_callbacks[ key ]( idx ) 

                        # print( computed_key ) 
                        
                        # if computed_keys is None :
                        #     computed_keys = [ key ]

                        # for computed_key in computed_keys : 

                        if save :
                            print( 'saving key: ' + str( key ) ) 
                            tmp_data = self.data[ key ][ idx ]

                            # print( key )
                            # print( tmp_data ) 

                            # the dataset did not exist before, hence why it wasnt in the keys
                            # thus create it and insert the data. 
                            if key not in existing_keys : 
                                f.create_dataset( key, data = tmp_data )

                            # otherwise overwrite the existing key if already in the file.
                            else :
                                dset = f[ key ]
                                dset[ ... ] = tmp_data
                            
            # if recomputing and not saving: just go ahead and compute everything. 
            else :
                for key in _keys :             
                    self.computation_callbacks[ key ]( idx )  
                

    
    def compute_BB( self, idx ) :
        return self._compute_norm_squared( 'BB', [ 'bx', 'by', 'bz' ], idx )

    
    
    def compute_EE( self, idx ) :
        return self._compute_norm_squared( 'EE', [ 'ex', 'ey', 'ez' ], idx )

    
    
    def compute_JJ( self, idx ) :
        return self._compute_norm_squared( 'JJ', [ 'jx', 'jy', 'jz' ], idx )


    
    # helper function for EE, BB, JJ
    def _compute_norm_squared( self, data_name, keys, idx ) :
        x = np.zeros( self.data[ keys[0] ][idx].shape )
        for key in keys :
            x += self.data[ key ][ idx ] ** 2 

        self.data[ data_name ][idx ]  = x

        
            
    def compute_ExB( self, idx ) :

        # print( 'computing ExB' )
        
        E = [ self.data[ key ][ idx ] for key in [ 'ex', 'ey', 'ez' ] ]
        B = [ self.data[ key ][ idx ] for key in [ 'bx', 'by', 'bz' ] ]
        
        tmp  = np.cross( E, B, axis = 0 ) 
        # print( 'cross product shape: ' + str(  tmp.shape ) )
        self.data[ 'ExB' ][ idx ] = tmp



    def compute_momentum_component_spectrum( self, idx, particle_type, i,
                                             alternate_name = None, boundaries = None ) :
        # construct tristan key name
        tristan_component_names = 'uvw'
        new_component_names = 'xyz' 
        
        tristan_key = tristan_component_names[ i ] + particle_type 
                  
        # construct our key name 
        key = 'p' + new_component_names[i] + '_' + particle_type + '_spec'
        
        momentum = self.data[ tristan_key ][ idx ]

        # len( bins ) == len( hist ) + 1
        # https://astropy.readthedocs.io/en/latest/visualization/histogram.html#bayesian-models
        # could use the above histograms for better optimized bins instead 
        hist, bins = np.histogram( momentum, bins = 'rice', density = 1 )
        
        data = np.zeros( ( 2, len( bins ) ) )
        data[0,:-1] = hist
        data[1,:] = bins
        
        self.data[ key ][ idx ] = data

        # print( key )
        # print( self.data[ key ][ idx ] )
        

        
    def compute_total_momentum_spectrum( self, idx, particle_type,
                                         alternate_name = None, boundaries = None ) :

        tristan_component_names = 'uvw'

        new_component_names = 'xyz' 
                        
        key = 'PP' + '_' + particle_type + '_spec'
            
        for i in range(3) :
        
            tristan_key = tristan_component_names[ i ] + particle_type 

            momentum = self.data[ tristan_key ][ idx ] 
            
            if i == 0 :
                total_momentum_sq = np.zeros( momentum.shape ) 
            
            total_momentum_sq += momentum ** 2 
                
        # now compute total momentum distribution.
        hist, bins = np.histogram(  np.sqrt( total_momentum_sq ), bins = 'rice' )

        data = np.zeros( ( 2, len( bins ) ) )
        data[0,:-1] = hist
        data[1,:] = bins

        # convert from f(p) to p^2 f(p) and normalize
        data[0,:] *= bins
        data[0,:] /= np.amax( data[0,:] ) 

        self.data[ key ][ idx ] = data


    
    
    def rebin_hist( self, hist, new_dim ) :
        
        pass 
        
                
            
# # compute squared vector norm of vector field formed with components
# # given in the list components (e.g. components = [ np.array(32,32), np.array(32,32) ] )
# # see compute_BB e.g. for example 
# def vector_norm_squared( components ) : 
#     return np.sum( [ x**2 for x in components ], axis = 0 )







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
