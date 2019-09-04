from mayavi import mlab
from pprint import pprint 

from .plotter import *

# from mayavi.filters.mask_points import MaskPoints



# allows you to control up to 3 volume slices
class VolumePlotter( MayaviPlotter ) :

    def __init__( self, mayavi_scene, data = None ) :
        super().__init__( mayavi_scene ) 

        self.data_added = 0
        self.needs_startup = 1 
        
        self.data = data
        # self.colorbar_added = 0 
        
        # variable storing each of the 3 addable /removable slices 
        self.mayavi_plot = None


                
    def startup( self ) :
        # super().startup()

        # print( len( self.data ) ) 
        src = mlab.pipeline.scalar_field( self.data, figure = self.mayavi_scene )
        self.mayavi_plot = mlab.pipeline.volume( src, figure = self.mayavi_scene, vmin = 12 , vmax = 14 ) 
                                                 # vmin = 0.8, vmax = 1.0,
                                                 # color = (0.5,0.5,0.5))

        # print_info( self.mayavi_plot._otf ) 
        
        mlab.colorbar( self.mayavi_plot, orientation = 'vertical' )


        # see https://docs.enthought.com/mayavi/mayavi/auto/example_magnetic_field.html
        # self.mayavi_plot.glyph.trait_set( mask_input_points = True ) 
        # self.mayavi_plot.glyph.mask_points.trait_set( on_ratio = 2, random_mode = False )

        # print_info( self.mayavi_plot.glyph.mask_points ) 

        
        # self.set_mask_points( 5 ) 

        # print_info( self.mayavi_plot ) 

        # self.axes_bounds = self.data.shape * self.scale
        self.set_orientation_axes( 1 )
        # self.set_outline( 1 )
        self.needs_startup =  0



        
    # def set_mask_points( self, mask_points ) :
    #     self.mayavi_plot.glyph.mask_points.trait_set( on_ratio = mask_points )
        

    # def get_mask_points( self ) :
    #     return self.mayavi_plot.glyph.mask_points.on_ratio
    

    def set_vmin( self, vmin ) :
        
        pass


    def set_vmax( self, vmax ) :
        pass

    
    def reset( self ) :
        mlab.clf( figure = self.mayavi_scene ) 
        self.__init__( self.mayavi_scene, data = self.data ) 
        
            
    def set_data( self, data ) :
 
        if data is not None : 
            self.data_added = 1 
            
        self.data = data[0]

        if self.data_added and self.needs_startup :
            self.startup() 

        else : 
            if self.mayavi_plot : 
                self.mayavi_plot.mlab_source.trait_set( scalars = self.data  )
            
                
def print_info( obj ) :

    print( type( obj ) )
    print('') 
    pprint( vars( obj ) )
    print('') 
    pprint( dir( obj ) ) 
    print('') 
    pprint( obj.trait_names() ) 



