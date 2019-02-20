from mayavi import mlab

from .plotter import *



# allows you to control up to 3 volume slices 
class VolumeSlicePlotter( MayaviPlotter ) :

    def __init__( self, mayavi_scene, data = None ) :
        super().__init__( mayavi_scene ) 

        self.data_added = 0
        self.needs_startup = 1 
        
        self.data = data
        # self.colorbar_added = 0 
        
        # variable storing each of the 3 addable /removable slices 
        self.mayavi_plots = [ None, None, None ]

        # these slices are added on the next
        # set defaults here 
        self.slices_to_add = [ 0, 0, 1 ] 

        # startup if possible 
        if self.data is not None :
            self.startup()
            
        # add default slices if possible. only works if data already is loaded,
        # which means that this only goes through if reset is called 
        # for i in range( 3 ) :
        #     if self.slices_to_add[i] :
        #         self.add_slice( i )


                
    def startup( self ) :
        # super().startup()
        
        colorbar_added = 0 
        
        for i in range(3) :
            if self.slices_to_add[i] :
                self.add_slice( i )


        self.set_orientation_axes( 1 )
        self.set_outline( 1 )
        colorbar = mlab.colorbar( orientation = 'vertical' )


        # mlab.draw() 
        # mlab.colorbar( orientation = 'vertical' )
        self.needs_startup =  0 
      
        
        
                
    def reset( self ) :
        mlab.clf( figure = self.mayavi_scene ) 
        self.__init__( self.mayavi_scene, data = self.data ) 
        
        
    # axis can be 0, 1, or 2 
    def add_slice( self, axis ) :
        
        # do nothing if axis already created. 
        if self.mayavi_plots[ axis ] :
            return 

        try :
            tmp = [ 'x', 'y', 'z' ][ axis ] + '_axes' 
        except : 
            print( 'ERROR: axis must be 0, 1, or 2' )
            sys.exit(1)

        self.mayavi_plots[ axis ] = mlab.volume_slice( self.data, plane_orientation = tmp,
                                                       slice_index = self.data.shape[ axis ] / 2,
                                                       figure = self.mayavi_scene )
        
        
    def remove_slice( self, axis ) :
        if self.mayavi_plots[ axis ] :
            self.mayavi_plots[ axis ].remove()
            self.mayavi_plots[ axis ] = None
            
        
    def set_data( self, data ) :

        # if self.data is None :
        #     self.needs_startup = 1 
 
        if data is not None : 
            self.data_added = 1 
            
        self.data = data[0]

        if self.data_added and self.needs_startup :
            self.startup() 

        else : 
            for mayavi_plot in self.mayavi_plots : 
                if mayavi_plot : 
                    mayavi_plot.mlab_source.trait_set( scalars = self.data )
            

    def encode( self ) :
        return

    
    @classmethod 
    def decode( cls, self ) :
        return 

    

        
from pprint import pprint
        
def print_info( obj ) :
    pprint( vars( obj ) )
    print() 
    pprint( dir( obj ) )
    print() 
    pprint( obj.trait_names() )
    print() 
