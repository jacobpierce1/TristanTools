from mayavi import mlab

from .plotter import MayaviPlotter 



# allows you to control up to 3 volume slices 
class VectorCutPlanePlotter( MayaviPlotter ) :

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

        self.mask_points = 10
        self.scale_factor = 8
        self.scale_mode = 'scale_by_vector'

        
        # startup if possible 
        if self.data is not None :
            self.startup()
            


                
    def startup( self ) :
        # super().startup()

        # this will reduce the amount of data to roughly a grid of 15x15x15 vectors. can
        # always change later in the gui.
        self.mask_points = int( ( self.data[0].shape[0] / 15. ) ** 3 ) 
        
        for i in range(3) :
            if self.slices_to_add[i] :
                self.add_slice( i )
        
        self.set_orientation_axes( 1 )
        self.set_outline( 1 )
        mlab.vectorbar( orientation = 'vertical' )
        mlab.vectorbar( orientation = 'vertical' )
        # mlab.vectorbar()
        self.needs_startup =  0 
      

        
    def clear( self ) :
        for i in range(3) :
            self.remove_slice(i)         
        super().clear() 

        
    def reset( self ) :
        self.clear() 
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

        source = mlab.pipeline.vector_field( * self.data, figure = self.mayavi_scene )
        
        self.mayavi_plots[ axis ] = mlab.pipeline.vector_cut_plane(
            source, plane_orientation = tmp,
            # scale_mode = 'none',
            figure = self.mayavi_scene )# ,
            # slice_index = self.data[0].shape[ axis ] / 2 ) 
            # mask_points = self.mask_points )

        plot = self.mayavi_plots[ axis ]
            
        plot.glyph.mask_input_points = True 
        plot.glyph.mask_points.on_ratio = self.mask_points
        plot.glyph.mask_points.random_mode = False

        # disable the annoying-ass rotation widget in the middle of the plot .
        plot.implicit_plane.widget.diagonal_ratio = 0
        plot.implicit_plane.widget.handle_size = 0.001

        # 3d arrow and corresponding options
        plot.glyph.glyph_source.glyph_source = plot.glyph.glyph_source.glyph_list[1]
        plot.glyph.glyph_source.glyph_source.shaft_radius = 0.03
        plot.glyph.glyph_source.glyph_source.shaft_resolution = 6
        plot.glyph.glyph_source.glyph_source.tip_length = 0.35
        plot.glyph.glyph_source.glyph_source.tip_radius = 0.1
        plot.glyph.glyph_source.glyph_source.tip_resolution = 6
        plot.glyph.glyph.scale_factor = self.scale_factor 
        plot.glyph.glyph_source.glyph_position = 'tail'
        

        # this forces the plot to refresh, which properly establishes the above sizes
        # (making the vtk objects invisible).
        # self.mayavi_plots[ axis ].implicit_plane.widget._vtk_obj.SetNormalToZAxis(1)
        # i spent a long time and this was the only way I was able to do it 
        
        vtk_obj = self.mayavi_plots[ axis ].implicit_plane.widget._vtk_obj
        if axis == 0 :
            vtk_obj.SetNormalToXAxis(1)
        elif axis == 1 :
            vtk_obj.SetNormalToYAxis(1)
        elif axis == 2 :
            vtk_obj.SetNormalToZAxis(1)


        
    def remove_slice( self, axis ) :
        if self.mayavi_plots[ axis ] :
            self.mayavi_plots[ axis ].remove()
            self.mayavi_plots[ axis ] = None

            

    def set_mask_points( self, mask_points ) :
        self.mask_points = mask_points 
        for plot in self.mayavi_plots :
            if plot :
                plot.glyph.mask_points.on_ratio = mask_points
        


    # options for x: 'scale_by_vector', 'data_scaling_off'
    def set_scale_mode( self, x ) :
        self.scale_mode = x
        for plot in self.mayavi_plots :
            if plot :
                plot.glyph.scale_mode = self.scale_mode
            
            
                
                
    def set_scale_factor( self, scale_factor ) :
        self.scale_factor = scale_factor 
        for plot in self.mayavi_plots :
            if plot :
                plot.glyph.glyph.scale_factor = self.scale_factor 
        
                
    # return mask points of the first active plot. note that they all have the
    # same mask points.
    def get_mask_points( self ) :
        return self.mask_points
    
            
    def get_scale_factor( self ) :
        return self.scale_factor 

        
                    
    def set_data( self, data ) :
 
        if data is not None : 
            self.data_added = 1 
            
        self.data = data

        try:
            print( data.shape )
        except :
            pass
        
        if self.data_added and self.needs_startup :
            self.startup() 

        else :
            for plot in self.mayavi_plots : 
                if plot : 
                    plot.mlab_source.trait_set( u = data[0], v = data[1], w = data[2] )
            

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
            
