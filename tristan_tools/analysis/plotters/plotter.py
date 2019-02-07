from mayavi import mlab



# this class and its subclasses handle all mayavi plotting functionality
# divorced from the TristanDataContainer 
# here is the functionality that will be used by all the plotters. 

class Plotter( object ) :

    def __init__( self, mayavi_scene ) : 
        self.mayavi_scene = mayavi_scene
        # self.mayavi_plot = None
        # self.needs_update = 1 

                
        self.orientation_axes = None
        
        
        self.orientation_axes_state = 0
        self.outline_state = 0

        # these make the oaxes and outline get generated automatically
        # feel free to disable.
        
        
        # self.actions = [ self.toggle_orientation_axes ]
        # self.actions_descriptions = [ 'toggle orientation axes' ] 


        
    # # this function is called when the data is plotted for the first time
    # # feel free to change 
    # def startup( self ) :
        
        
    def set_orientation_axes( self, state ) :

        if state :

            # already exists x
            if self.orientation_axes_state :
                return 
            
            self.orientation_axes = mlab.orientation_axes( figure = self.mayavi_scene ) 
            self.orientation_axes_state = 1 
            
        # remove 
        else :

            #already removed 
            if not self.orientation_axes_state :
                return
            
            self.orientation_axes.remove() 
            self.orientation_axes_state = 0 
            


            
    def set_outline( self, state ) :

        if state :

            # already exists x
            if self.outline_state :
                return 
            
            self.outline = mlab.outline( figure = self.mayavi_scene ) 
            self.outline_state = 1 
            
        # remove 
        else :

            #already removed 
            if not self.outline_state :
                return
            
            self.outline.remove() 
            self.outline_state = 0 
            


    def clear( self ) :
        mlab.clf( figure = self.mayavi_scene ) 
            
        
    # to be implemented by subclasses 
    def update( self ) :
        pass


    # def set_title( self, title ) :

    #     # if not title :
    #     #     title = self.plot_type 

    #     print( self.mayavi_scene ) 
    #     mlab.title( title, figure = self.mayavi_scene )

        
    
    # # does not need to be reimplemented for subclasses
    # def reset( self ) :
    #     # self.mayavi_scene.clear()
    #     mlab.clf( figure = self.mayavi_scene ) 
    #     self.__init__( self.mayavi_scene ) 
    #     # self.set_data( self.data ) 
        
    # def set_data( data ) :
    #     self.data = data 


    
