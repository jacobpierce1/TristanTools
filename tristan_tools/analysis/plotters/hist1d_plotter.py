# from mayavi import mlab
from pprint import pprint 

from .plotter import MPLPlotter 

import matplotlib.pyplot as plt 

# from mayavi.filters.mask_points import MaskPoints



# allows you to control up to 3 volume slices
class Hist1dPlotter( MPLPlotter ) :

    def __init__( self, mpl_ax, data = None ) :
        super().__init__( mpl_ax ) 

        self.ax = mpl_ax
        self.data = data 
        
        
        self.data_added = 0
        self.needs_startup = 1 
        
        self.data = data
        
        if self.data is not None : 
            self.startup() 

            
                
    # def startup( self ) :
    #     # self.ax.plot( range(10), range(10 ) )
    #     self.needs_startup =  0

    
    def reset( self ) :
        # mlab.clf( figure = self.mayavi_scene ) 
        # self.__init__( self.mayavi_scene, data = self.data ) 

        pass
        

    
    def set_data( self, data ) :

        self.ax.clear() 

        self.data = data
        
        hist, bins = data[0][:,:-1]

        print( 'self.needs_startup :' + str( self.needs_startup  ) ) 
    
        self.ax.semilogy( bins, hist, ls = 'steps-mid' ) 

            
                
def print_info( obj ) :

    print( type( obj ) )
    print('') 
    pprint( vars( obj ) )
    print('') 
    pprint( dir( obj ) ) 
    print('') 
    pprint( obj.trait_names() ) 



