# track the state of the gui and allow the user to save and reload a state

STATE_SAVE_PATH = './saved_states/'
DEFAULT_STATE_NAME = 'default' 


import numpy as np
from enum import Enum 


class LoadPolicy( Enum ) :
    LOAD_ALL = 0
    LOAD_NECESSARY = 1

    DESCRIPTIONS = ['Load all', 'Load necessary' ]


    

class StateHandler( object ) :

    def __init__( self ) :

        # self.load_state( DEFAULT_STATE_NAME ) 

        self.shape = ( 1, 1 ) 
        # self.shape = (1,1)
        
        self.data_load_policy = LoadPolicy.LOAD_ALL 

        self.keys = np.array( [ [ [ 'dens'],
                                  [ 'bx', 'by', 'bz' ],
                                  [ 'ex', 'ey', 'ez' ] ] ] ) 

        self.plot_types = np.array( [ [ 'volume_slice', 'quiver3d', 'quiver3d' ] ] ) 

        # self.plot_data = [ [ 'dens' ],
        #                    [ 'bx', 'by', 'bz' ],
        #                    [ 'ex', 'ey', 'ez' ] ]
        
        self.computation_keys = []

        self.stride = 1
        

    def save_state( self ) :
        pass

        
    def load_state( self ) :
        pass     
