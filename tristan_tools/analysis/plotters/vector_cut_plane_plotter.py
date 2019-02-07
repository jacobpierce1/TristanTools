from mayavi import mlab

from .plotter import Plotter 



# allows you to control up to 3 volume slices 
class VectorCutPlanePlotter( Plotter ) :

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
        self.slices_to_add = [ 1, 0, 0 ] 

        # add default slices if possible. only works if data already is loaded,
        # which means that this only goes through if reset is called 
        # for i in range( 3 ) :
        #     if self.slices_to_add[i] :
        #         self.add_slice( i )


                
    def startup( self ) :
        # super().startup()
        
        colorbar_added = 0 

        self.mask_points = 2 
        
        for i in range(3) :
            if self.slices_to_add[i] :
                self.add_slice( i )

                if not colorbar_added :
                    mlab.vectorbar( self.mayavi_plots[i], orientation = 'vertical' )
                    colorbar_added = 1 
        
        self.set_orientation_axes( 1 )
        self.set_outline( 1 )
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

        source = mlab.pipeline.vector_field( * self.data )
        
        self.mayavi_plots[ axis ] = mlab.pipeline.vector_cut_plane(
            source, plane_orientation = tmp )# ,
            # slice_index = self.data[0].shape[ axis ] / 2 ) 
            # mask_points = self.mask_points )

        self.mayavi_plots[ axis ].glyph.trait_set( mask_input_points = True ) 
        self.mayavi_plots[ axis ].glyph.mask_points.trait_set( on_ratio = self.mask_points, random_mode = False )

        
    def remove_slice( self, axis ) :
        if self.mayavi_plots[ axis ] :
            self.mayavi_plots[ axis ].remove()
            self.mayavi_plots[ axis ] = None


    def set_mask_points( self, mask_points ) :
        self.mask_points = mask_points 
        for plot in self.mayavi_plots :
            if plot :
                plot.glyph.mask_points.trait_set( on_ratio = mask_points )
        

    # return mask points of the first active plot. note that they all have the
    # same mask points.
    def get_mask_points( self ) :
        # return self.mayavi_plot.glyph.mask_points.on_ratio
        for plot in self.mayavi_plots :
            if plot :
                return plot.glyph.mask_points.on_ratio
        

        
                    
    def set_data( self, data ) :
 
        if data is not None : 
            self.data_added = 1 
            
        self.data = data

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

    
