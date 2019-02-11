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

            
                
    def startup( self ) :
        self.ax.plot( range(10), range(10 ) )
        self.needs_startup =  0

    
    def reset( self ) :
        # mlab.clf( figure = self.mayavi_scene ) 
        # self.__init__( self.mayavi_scene, data = self.data ) 

        pass
        

    
    def set_data( self, data ) :

        self.ax.clear() 
        # plt.cla()
        print( 'called mpl set data' ) 
        self.data = data
        
        hist, bins = data[0][:,:-1]

        print( 'self.needs_startup :' + str( self.needs_startup  ) ) 
        
        if self.needs_startup :
            self.startup()

        else :
            print( 'calling semilogy' ) 
            self.ax.semilogy( hist, bins ) 
        
        # self.ax.
        
        # if data is not None : 
        #     self.data_added = 1 
            
        # self.data = data[0]

        # if self.data_added and self.needs_startup :
        #     self.startup() 

        # else : 
        #     if self.mayavi_plot : 
        #         self.mayavi_plot.mlab_source.trait_set( scalars = self.data  )
            
                
def print_info( obj ) :

    print( type( obj ) )
    print('') 
    pprint( vars( obj ) )
    print('') 
    pprint( dir( obj ) ) 
    print('') 
    pprint( obj.trait_names() ) 



