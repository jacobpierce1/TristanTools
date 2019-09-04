# implements the class TristanDataAnalyzer. this class subclasses
# TristanDataContainer and hence gives access to all the same functionality
# as the data container itself. it also includes functions for computing and
# storing derived
# quantities, such as field magnitudes, etc. 
# included is much functionality necessary for real

import gc 
import numpy as np
import sys
import os
import h5py
from collections import OrderedDict
from scipy import sparse


from sortedcontainers import SortedSet 

try :
    from numba import jit
    USING_NUMBA = 1
    print( 'INFO: using numba' ) 
except :
    print( 'INFO: unable to import numba.' )
    USING_NUMBA = 0 

from .tristan_data_container import TristanDataContainer
from .tristan_cut import TristanCut 

# from .helper_classes import AttrDict, RecursiveAttrDict



DEBUG_SAVE = 0
# BENCHMARK = 1 


# POSITION_CUT_AVAILABLE = ALL_SPECTRA


ALL_SPECTRA = []
ALL_CUT_SPECTRA = [] 


components = 'xyz'
for particle_type in 'ei' :
    for i in range(3) :
          
        ALL_SPECTRA.append( 'p' + components[i] + '_' + particle_type + '_spec' )
        ALL_CUT_SPECTRA.append( 'p' + components[i] + '_cut_' + particle_type + '_spec' ) 

    ALL_SPECTRA.append( 'PP_' + particle_type + '_spec' )
    ALL_CUT_SPECTRA.append( 'PP_cut_' + particle_type + '_spec' ) 

ALL_SPECTRA.extend( [ 'gammae_spec', 'gammai_spec' ] ) 

# hack 
OTHER_COMPUTATION_KEYS = [ 'gammae_max', 'gammae_mean',
                           'gammai_max', 'gammai_mean' ]



MOMENTUM_CUTTABLE_KEYS = [ 'dens_cut', 'densi_cut', 'dense_cut', 'charge_dens_cut' ] 
POSITION_CUTTABLE_KEYS = [ ]


class TristanDataAnalyzer( TristanDataContainer ) :
    
    def __init__( self, data_path = None, computations_path = None, spectra_nbins = 1000 ) :
                
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
        self.callbacks = { 'BB' : self.compute_BB,
                           'EE' : self.compute_EE,
                           'JJ' : self.compute_JJ,
                           'E_parallel' : self.compute_E_parallel, 
                           'ExB' : self.compute_ExB,
                           'charge_dens' : self.compute_charge_dens,
                           'dense' : self.compute_dense,
                           'spectra' : self.compute_spectra,
                           'position_cuttable_keys' : self.compute_position_cuttable_keys,
                           'momentum_cuttable_keys' : self.compute_momentum_cuttable_keys }

        
        
        # store what keys (stored in self.data) are computed by each callback: 
        self.callback_to_computations = OrderedDict( [ ( 'BB', [ 'BB' ] ),
                                                       ( 'EE', [ 'EE' ] ),
                                                       ( 'JJ', [ 'JJ' ] ),
                                                       ( 'E_parallel', [ 'E_parallel' ] ),
                                                       ( 'ExB', [ 'ExB' ] ),
                                                       ( 'charge_dens', [ 'charge_dens' ] ),
                                                       ( 'dense', [ 'dense' ] ),
                                                       ( 'spectra', ALL_SPECTRA ),
                                                       ( 'momentum_cuttable_keys',
                                                         [ 'dense_cut',
                                                           'densi_cut' ] ),
                                                       ( 'position_cuttable_keys',
                                                         ALL_CUT_SPECTRA ) ] )
                                                     

        self.computation_to_callback = {}
        for callback, computations in self.callback_to_computations.items() :
            for computation in computations : 
                self.computation_to_callback[ computation ] = callback 
        

        # particle-derived quantities that a position or momentum cut can be applied to
        self.position_cut = TristanCut( None, 3 )
        self.momentum_cut = TristanCut( None, 3 )
        self.total_momentum_cut = TristanCut( None, 1 )

        
        # self.position_cuttable_keys = set( POSITION_CUTTABLE_KEYS ) 
        # self.momentum_cuttable_keys = set( MOMENTUM_CUTTABLE_KEYS )
        # self.total_momentum_cuttable_keys = self.momentum_cuttable_keys 

                                 
                                       
        self.callback_keys = SortedSet( self.callbacks.keys() )
        self.computation_keys = SortedSet( self.computation_to_callback.keys() )

        # call __init__ from TristanDataContainer. only call it after the computation keys
        # have been created so that the load_keys function will work correctly 
        super( TristanDataAnalyzer, self ).__init__( data_path )

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
        # print( 'calling load keys ' ) 
        self.load_keys( 0 )
        
        self.load_cuts() 
        

        
    def load_cuts( self ) :
        pass # ...
        

    def load_keys( self, load_data_keys = 1 ) :

        if load_data_keys : 
            super( TristanDataAnalyzer, self ).load_keys()
        
        for key in self.computation_keys : 
            self.data[ key ] = None
            
        for key in OTHER_COMPUTATION_KEYS :
            self.data[ key ] = None
            
        # # this allocates space for more keys 
        # self.compute_momentum_spectra( 0, init = 1 )     
            
        # # this dict is accessed by the GUI to print the available quantities
        # # in latex. ignore if using TristanDataAnalyzer for offline analysis.
        # # make sure to append to this dict any new quantities you make if
        # # you want to be able to visualize them in the GUI.
        # self.computation_key_descriptions_dict = { 'BB' : r'$|B|^2$',
        #                                            'EE' : r'$|E|^2$',
        #                                            'JJ' : r'$|J|^2$',
        #                                            'ExB' : r'$E\times B$' } 



    def open_computations_file( self, timestep ) :
        return h5py.File( self.get_computations_file( timestep ) )
        

    def get_computations_file( self, idx ) :
        return ( self.computations_path + 'computations.%d' % idx )

        
    # analagous to the data-loading implementation of TristanDataContainer.
    # here we can compute quantities at given indices and keys instead of all.
    # if recompute is not 0, then the key will be computed even if already loaded.
    def compute_indices( self, indices = None, keys = None, recompute = 0, save = 1,
                         skip_save = None ) :

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

            if idx not in self.loaded_indices :
                continue
            
            # we need access to the file if we are either saving or loading from memory.
            if ( not recompute ) or save : 
        
                # append mode: Read/write if exists, create otherwise (default)
                with h5py.File( self.get_computations_file( idx ), 'a' ) as f : 

                    # keys that are already in the dataset
                    existing_keys = set( f.keys() )
                    # print( 'existing keys: ' + str( existing_keys ) )
                    
                    if not recompute : 
                        keys_to_compute = _keys - existing_keys  
                        
                        # load it in
                        for key in existing_keys - set( [ 'position_cut', 'momentum_cut', 'total_momentum_cut' ] ) :

                            # current implementation: if the key was previous saved and we no longer recognize it,
                            # then it will be loaded (unless of course that key was not requested. but if a call
                            # for all keys was made, then a previously saved key that is no longer in the analyzer
                            # will be detected).
                            if key not in self.data.keys()  :
                                print( 'INFO: key not in self.data: %s' % key ) 
                                # print( self.data.keys() )
                                self.data[ key ] = None

                            self.data[ key ][ idx ] = np.array( f[ key ] )

                        # # check if cut quantities need to be recomputed 
                        # # if 'position_cut' in existing_keys :
                        # position_cut = TristanCut.decode( np.array( f[ 'position_cut' ] ) )
                        # if self.position_cut != position_cut :
                        #     keys_to_compute += self.position_cuttable_keys

                        # # if 'momentum_cut' in existing_keys :
                        # momentum_cut = TristanCut.decode( np.array( f[ 'momentum_cut' ] ) )
                        # total_momentum_cut = TristanCut.decode( np.array( f[ 'total_momentum_cut' ] ) )
                        # if ( ( momentum_cut != self.momentum_cut )
                        #      or ( total_momentum_cut != self.total_momentum_cut ) )  :
                        #     keys_to_compute += self.momentum_cuttable_keys
                            
                                

                    # otherwise declare that no keys have been computed
                    else :
                        keys_to_compute = _keys

                    # print( 'keys_to_compute: ' + str( keys_to_compute ) ) 
                        
                    # compute keys that were not in the file, then write them.
                    callbacks_needed = SortedSet( [ self.computation_to_callback[ key ] for key in keys_to_compute ] )
                    for callback_key in callbacks_needed :

                        if DEBUG_SAVE : 
                            print( 'INFO: calling: ' + callback_key )

                        self.callbacks[ callback_key ]( idx ) 


                        if save :
                            # print( 'saving key: ' + str( key ) )
                            for key in self.callback_to_computations[ callback_key ] :
                                tmp_data = self.data[ key ][ idx ]

                                # the dataset did not exist before, hence why it wasnt in the keys
                                # thus create it and insert the data. 
                                if key not in existing_keys :

                                    if DEBUG_SAVE :
                                        print( 'DEBUG: saving key: ' + str( key ) )
                                        try :
                                            print( tmp_data.shape )
                                        except :
                                            pass

                                    f.create_dataset( key, data = tmp_data, compression = 'lzf', shuffle = 1 )

                                # otherwise overwrite the existing key if already in the file.
                                else :
                                    dset = f[ key ]
                                    dset[ ... ] = tmp_data
                            
            # if recomputing and not saving: just go ahead and compute everything. 
            else :
                callbacks_needed = SortedSet( [ self.computation_to_callback[ key ] for key in _keys ] )

                for callback_key in callbacks_needed :             
                    self.callbacks[ callback_key ]( idx )  

        # # comupte any cuts that are defined 
        # self.compute_cut_masks( idx )



        
    # def compute_cut_masks( self ) :

    #     self.position_masks = self.position_cut.apply( 

        

    
    def compute_BB( self, idx ) :
        x = self._compute_norm_squared( [ 'bx', 'by', 'bz' ], idx )
        self.data[ 'BB' ][idx ]  = x
    
    
    def compute_EE( self, idx ) :
        x = self._compute_norm_squared( [ 'ex', 'ey', 'ez' ], idx )
        self.data[ 'EE' ][idx ]  = x
    
    
    def compute_JJ( self, idx ) :
        x = self._compute_norm_squared( [ 'jx', 'jy', 'jz' ], idx )
        self.data[ 'JJ' ][idx ]  = x


    # believe or not this is much faster than np.sum( np.square( [x,y,z] ) )
    # helper function for EE, BB, JJ
    def _compute_norm_squared( self, keys, idx ) :
        x = np.zeros( self.data[ keys[0] ][idx].shape )
        for key in keys :
            x += self.data[ key ][ idx ] ** 2 
        return x 
        


    # def compute_EB( self, idx ) :
        
    #     E = [ self.data[ key ][ idx ] for key in [ 'ex', 'ey', 'ez' ] ]
    #     B = [ self.data[ key ][ idx ] for key in [ 'bx', 'by', 'bz' ] ]

    #     # compute dot product along first axis (if you don't believe me,
    #     # play around with the function einsum. it is awesome.)
    #     tmp =  np.einsum( 'a...,a...', E, B )

    #     if self.data[ 'BB' ][ idx ] is not None :
    #         B_mag = np.sqrt( self.data[ 'BB' ][ idx ] )
    #     else :
    #         B_mag = np.sqrt( self._compute_norm_squared( ['bx','by','bz'], idx) )

    #     # normalize by B, so that what we see is the electric field component parallel to B
    #     self.data[ 'EB' ][ idx ] = tmp / B_mag


        
    def compute_E_parallel( self, idx ) :
        
        E = np.array( [ self.data[ key ][ idx ] for key in [ 'ex', 'ey', 'ez' ] ] ) 
        B = np.array( [ self.data[ key ][ idx ] for key in [ 'bx', 'by', 'bz' ] ] )

        # compute dot product along first axis (if you don't believe me,
        # play around with the function einsum. it is awesome.)
        EB =  np.einsum( 'a...,a...', E, B )

        if self.data[ 'BB' ][ idx ] is None :
            self.compute_BB( idx )
            
        BB = self.data[ 'BB' ][ idx ]   

        
        
        # normalize by B, so that what we see is the electric field component parallel to B
        self.data[ 'E_parallel' ][ idx ] = B * EB / BB


        # print( self.data[ 'E_parallel' ][ idx ].shape ) 

        
    def compute_ExB( self, idx ) :

        # print( 'computing ExB' )
        
        E = [ self.data[ key ][ idx ] for key in [ 'ex', 'ey', 'ez' ] ]
        B = [ self.data[ key ][ idx ] for key in [ 'bx', 'by', 'bz' ] ]
        
        tmp  = np.cross( E, B, axis = 0 ) 
        # print( 'cross product shape: ' + str(  tmp.shape ) )
        self.data[ 'ExB' ][ idx ] = tmp



        
    def compute_spectra( self, idx, masks = None ) :

        if masks is None :
            masks = [ None, None ] 
        
        # add momentum spectrum computers:
        components = 'xyz'

        particle_types = 'ei'
        for j in range( 2 ) :

            for i in range(3) :
                self.compute_momentum_component_spectrum( idx, particle_types[j], i, masks[j] ) 

            # self.compute_total_momentum_spectrum( idx, particle_types[j], masks[j] ) 
            self.compute_gamma_spectrum( idx, particle_types[j], masks[j] ) 

        
    def compute_momentum_component_spectrum( self, idx, particle_type, i, mask = None ) :

        # construct tristan key name
        tristan_component_names = 'uvw'
        new_component_names = 'xyz' 
        
        tristan_key = tristan_component_names[ i ] + particle_type 
        momentum = self.data[ tristan_key ][ idx ]
        
        # construct our key name 
        key = 'p' + new_component_names[i]

        if mask is not None :
            key += '_cut' 
            momentum =  momentum[ mask ]
            
        key += '_' + particle_type + '_spec'
                    

        # note that len( bins ) == len( hist ) + 1
        # https://astropy.readthedocs.io/en/latest/visualization/histogram.html#bayesian-models
        # could use the above histograms for better optimized bins instead

        # if mask is None :
        #     tmp = momentum
        # else :
        #     print( len( masks ) )
        #     print( len( momentum )  )
        #     tmp = momentum[ mask ] 
        
        hist, bins = np.histogram( momentum, bins = 'rice', density = 1 )
        
        data = np.zeros( ( 2, len( bins ) ) )
        data[0,:-1] = hist
        data[1,:] = bins
        
        self.data[ key ][ idx ] = data

        

        
    def compute_total_momentum_spectrum( self, idx, particle_type, mask = None ) :

        tristan_component_names = 'uvw'

        new_component_names = 'xyz' 
                        
        key = 'PP'

        if mask is not None :
            key += '_cut'
            
        key += '_' + particle_type + '_spec'
        
        for i in range(3) :
        
            tristan_key = tristan_component_names[ i ] + particle_type 

            momentum = self.data[ tristan_key ][ idx ]

            if mask is not None :
                momentum = momentum[ mask ] 
            
            if i == 0 :
                total_momentum_sq = np.zeros( momentum.shape ) 
            
            total_momentum_sq += momentum ** 2

        total_momentum = np.sqrt( total_momentum_sq ) 
            
        # if mask is not None :
        #     # mask &= self.total_momentum_cut.apply( [ total_momentum ] ) 
        #     tmp = total_momentum[ mask ] 
        # else :
        #     tmp = total_momentum
        # # now compute total momentum distribution.
        
        hist, bins = np.histogram(  total_momentum, bins = 'rice' )

        data = np.zeros( ( 2, len( bins ) ) )
        data[0,:-1] = hist
        data[1,:] = bins

        # convert from f(p) to p^2 f(p) and normalize
        data[0,:] *= bins
        data[0,:] /= np.amax( data[0,:] ) 

        self.data[ key ][ idx ] = data



    # note: this actually computes a histogram of beta * gamma. 
    def compute_gamma_spectrum( self, timestep, particle_type, mask = None,
                                save = 1, load = 1 ) :
        
        if particle_type == 'e' :
            data_key = 'gammae'
        elif particle_type == 'i' :
            data_key = 'gammai'
        else :
            print( 'ERROR: invalid particle type.' )
            sys.exit( 1 ) 

        
        computation_key = 'gamma' + particle_type + '_spec'

        with self.open_computations_file( timestep ) as f :
            
            if computation_key in f.keys() :
                if load : 
                    self.data[ computation_key ][ timestep ] = f[ computation_key ][:]
                    return

                else :
                    del f[ computation_key ] 

                    
        with self.open_data_file( timestep, 'prtl.tot' ) as f : 

            gammas = f[ data_key ] 
            total_particles = len( gammas ) 
            
            batch_size = int( 1e8 )
                              
            # first compute the max and min for this data 

            min_gamma = np.inf
            max_gamma = 1.0

            
            for i in range( 0, total_particles, batch_size ) :
                
                end = min( i + batch_size, total_particles )

                tmp = gammas[ i : end ] 

                min_gamma = min( min_gamma, np.amin( tmp ) )
                max_gamma = max( max_gamma, np.amax( tmp ) ) 

                gc.collect()

                
            # now compute the histograms
            # use sturges bins 
            nbins = min( 1000, int( total_particles ** ( 1 / 3 ) ) ) 

            if min_gamma < 1 :
                min_gamma = 1.
                
            if max_gamma < 1 :
                max_gamma = 1.
            
            min_beta_gamma = min_gamma * ( 1 - 1 / min_gamma ** 2 ) ** 0.5
            max_beta_gamma = max_gamma * ( 1 - 1 / max_gamma ** 2 ) ** 0.5

            print( 'min_beta_gamma = ' + str( min_beta_gamma ) ) 
            
            bins = np.linspace( min_beta_gamma, max_beta_gamma + 1, nbins )
            hist = np.zeros( bins.size - 1 ) 
            
            for i in range( 0, total_particles, batch_size ) :
                end = min( i + batch_size, total_particles )

                tmp = gammas[ i : end ] 
                tmp[ tmp < 1 ] = 1 
                tmp *= ( 1 - 1 / tmp ** 2 ) ** 0.5

                cur_hist, cur_bins = np.histogram( tmp, bins = bins )
                hist += cur_hist

                gc.collect()
                                
            hist /= np.sum( hist ) * ( bins[1] - bins[0] ) 
                
        data = np.zeros( ( 2, len( hist ) ) )
        data[0,:] = hist
        data[1,:] = bins[:-1]

        print( 'min hist = ' + str( min( bins ) ) ) 
        
        self.data[ computation_key ][ timestep ] = data

        
        if save :
            with self.open_computations_file( timestep ) as f :

                if computation_key not in f.keys() : 
                    f.create_dataset( computation_key, data = data,
                                      compression = 'lzf', shuffle = 1 )

                else :
                    f[ computation_key ][ ... ] = data 





                    
    def compute_binned_particle_statistic( self, timestep, data_key, op,
                                           load = 1, save = 1 ) :
        
        if data_key in [ 'gammae', 'ue', 've', 'we' ] :
            coords_keys = [ 'xe', 'ye', 'ze' ]

        elif data_key in [ 'gammai', 'ui', 'vi', 'wi' ] :
            coords_keys = [ 'xi', 'yi', 'zi' ]

        else :
            print( 'ERROR: invalid key' )
            sys.exit( 0 )

        if op not in [ 'max', 'mean' ] :
            print( 'ERROR: invalid operation' )
            sys.exit( 1 )

        computation_key = data_key + '_' + op

            
        # load data if possible 
        with self.open_computations_file( timestep ) as f :
            
            if computation_key in f.keys() :

                if load : 
                    self.data[ computation_key ][ timestep ] = f[ computation_key ][:]
                    return

                else :
                    del f[ computation_key ] 

        batch_size = int( 1e8 ) 

        shape = ( self.params.mx0,
                  self.params.my0,
                  self.params.mz0 ) 

        binned_statistic = np.zeros( shape ) 

        # print( data_key )
        # print( coords_keys ) 
        
        with self.open_data_file( timestep, 'prtl.tot' ) as f :
            total_particles = len( f[ data_key ] )

            for i in range( 0, total_particles, batch_size ) :
                # print( i ) 

                end = min( i + batch_size, total_particles )

                data = f[ data_key ][ i : end ]
                coords = np.vstack( [ f[ key ][ i : end ] for key in coords_keys ] ).T

                if op == 'max' :
                    binned_statistic = np.maximum( binned_statistic,
                                                   compute_binned_statistic( data, coords,
                                                                             shape, op ) )
                elif op == 'mean' : 
                    binned_statistic += ( ( (end - i)/total_particles)
                                          * compute_binned_statistic( data, coords, shape, op ) )


        gc.collect() 

        # print( binned_statistic.shape ) 
        
        self.data[ computation_key ][ timestep ] = binned_statistic

        
        if save :
            with self.open_computations_file( timestep ) as f :

                if computation_key not in f.keys() : 
                    f.create_dataset( computation_key, data = binned_statistic,
                                      compression = 'lzf', shuffle = 1 )

                else :
                    f[ computation_key ][ ... ] = binned_statistic 
                    
                    


        
    def compute_momentum_cuttable_keys( self, idx ) :

        epositions = np.array( [ self.data[ s ][ idx ] for s in [ 'xe', 'ye', 'ze' ] ] ).T
        ipositions = np.array( [ self.data[ s ][ idx ] for s in [ 'xi', 'yi', 'zi' ] ] ).T
        emomenta = np.array( [ self.data[ s ][ idx ] for s in [ 'ue', 've', 'we' ] ] )
        imomenta = np.array( [ self.data[ s ][ idx ] for s in [ 'ui', 'vi', 'wi' ] ] ) 

        masks = [ self.momentum_cut.apply( x )
                  # & self.total_momentum_cut.apply( x )
                  for x in [ emomenta, imomenta ] ]
        
        epositions = epositions[ masks[0] ]
        ipositions = ipositions[ masks[1] ]
        
        shape = self.data.dense[ idx ].shape
        
        bins = [ np.arange( x ) for x in shape ]
        
        self.data.dense_cut[ idx ]  = np.histogramdd( np.array( epositions ), bins = bins )[0]
        self.data.densi_cut[ idx ]  = np.histogramdd( np.array( ipositions ), bins = bins )[0]

        


        
    def compute_position_cuttable_keys( self, idx ) :
        epositions = np.array( [ self.data[ s ][ idx ] for s in [ 'xe', 'ye', 'ze' ] ] )
        ipositions = np.array( [ self.data[ s ][ idx ] for s in [ 'xi', 'yi', 'zi' ] ] )
        # emomenta = np.array( [ self.data[ s ][ idx ] for s in [ 'ue', 've', 'we' ] ] )
        # imomenta = np.array( [ self.data[ s ][ idx ] for s in [ 'ui', 'vi', 'wi' ] ] )

            
            # emomenta = [ self.data[ s ][ idx ] for s in [ 'ue', 've', 'we' ] ]
        # imomenta = [ self.data[ s ][ idx ] for s in [ 'ui', 'vi', 'wi' ] ]
        # masks gets modified in the total momentum computation.
        masks = [ self.position_cut.apply( x ) for x in [ epositions, ipositions ] ] 

        # print( 'INFO: in compute_position_cuttable_keys' )
        # print( self.position_cut ) 
        # print( masks )

        print( 'compute_position_cuttable_keys: ' + str( epositions ) )
        print( 'compute_position_cuttable_keys: ' + str( self.position_cut ) )
        print( 'compute_position_cuttable_keys: ' + str( masks ) )
        print( 'compute_position_cuttable_keys: ' + str( [ np.sum(x) for x in masks] ) )
        
        # print( 'compute_position_cuttable_keys: ' + str( self.position_cut.cuts ) )
        
        self.compute_spectra( idx, masks = masks ) 

        

        
    def compute_dense( self, idx ) :
        self.data[ 'dense' ][ idx ] = self.data[ 'dens' ][ idx ] - self.data[ 'densi' ][ idx ] 

    
    def compute_charge_dens( self, idx ) :
        self.data[ 'charge_dens' ][ idx ] = 2 * self.data[ 'densi' ][ idx ] - self.data[ 'dens' ][ idx ]





        

def compute_binned_statistic( data, coords, shape, op ) :

    if op not in [ 'max', 'mean' ] :
        print( 'ERROR: invalid operation' )
        sys.exit( 1 ) 
        
    bin_indices = np.ravel_multi_index(coords.astype(int).T, shape)
    
    # print( bin_indices.shape )
    # print( data.shape ) 
    
    aux = sparse.csr_matrix((data, bin_indices, np.arange(data.size+1)),
                            (data.size, np.prod(shape))).tocsc()

    cut = aux.indptr.searchsorted(data.size)

    max_data_pp = np.empty(shape)

    if op == 'max' :
        max_data_pp.ravel()[:cut] = np.maximum.reduceat(aux.data, aux.indptr[:cut])

    elif op == 'mean' : 
        # max_data_pp.ravel()[:cut] = np.mean.reduceat(aux.data, aux.indptr[:cut])
        # broken
        sys.exit( 1 ) 
        
    CLIPAT = 0

    max_data_pp.ravel()[aux.indptr[:-1]==aux.indptr[1:]] = CLIPAT
    max_data_pp[max_data_pp < CLIPAT] = CLIPAT

    return max_data_pp


if USING_NUMBA :
    # compute_binned_statistic = jit( compute_binned_statistic, nopython = 1 ) 
    ... 

        
        
    
    # def compute_masks( self, idx, position_cut = None ) :
    #     epositions = [ self.data[ s ][ idx ] for s in [ 'xe', 'ye', 'ze' ] ]
    #     ipositions = [ self.data[ s ][ idx ] for s in [ 'xi', 'yi', 'zi' ] ]
    #     self.position_masks = [ self.position_cut.apply( x ) for x in [ epositions, ipositions ] ]

        

    
    # def momentum_position_cut( self, idx, momentum_cut = None ) :
    #     return self.apply_momentum_cut( 'uvw', momentum_cut ) 

                
    # def apply_cut( self, idx, components, cut ) :

    #     masks = [ np.arange( len( self.data.xe[ idx ] ) ),
    #               np.arange( len( self.data.xi[ idx ] ) ) ]
        
    #     if not cut :
    #         return masks 
        
    #     particle_types = 'ei'
    #     component_names = 'uvw'

    #     for i in range(2):

    #         if not momentum_cut[i] :
    #             continue
            
    #         for i in range(3):
    #             component = component_names[j] + particle_types[i] 
    #             masks[i][j] &= ( ( self.data[ component ] >= cut[0] ) 
    #                              & ( self.data[ component ] <= cut[1] ) )
                        
    #     self.masks = masks  

    




    


    
    # def rebin_hist( self, hist, new_dim ) :
        
    #     pass 
        
    
    # def compute_
    
            
# # compute squared vector norm of vector field formed with components
# # given in the list components (e.g. components = [ np.array(32,32), np.array(32,32) ] )
# # see compute_BB e.g. for example 
# def vector_norm_squared( components ) : 
#     return np.sum( [ x**2 for x in components ], axis = 0 )







# def calc_psi(f):
#     ''' Calculated the magnetic scaler potential for a 2D simulation
#     Args:
#         d (dict): Dictionary containing the fields of the simulation
#             d must contain bx, by, xx and yy
#     Retruns:
#         psi (numpy.array(len(d['xx'], len(d['yy']))) ): Magnetic scaler
#             potential
#     '''

#     bx = np.squeeze(f['bx'])
#     by = np.squeeze(f['by'])
#     dx = dy = 1./f['c_omp']

#     psi = 0.0*bx
#     psi[1:,0] = np.cumsum(bx[1:,0])*dy
#     psi[:,1:] = (psi[:,0] - np.cumsum(by[:,1:], axis=1).T*dx).T

#     return psi.T
