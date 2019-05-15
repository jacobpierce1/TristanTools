from mayavi import mlab
import numpy as np
import matplotlib.pyplot as plt




class MayaviWrapError( Exception ) :
    pass 



# class MayaviWrapper( object ) :

#     def __

def vector_cut_plane_wrap( data, mask_points = 1, scale_factor = 1 ) : 

    if( len( data ) != 3 ) :
        raise MayaviWrapError( 'ERROR: len( data != 3 )' )
        
    
    src = mlab.pipeline.vector_field( * data )
    
    plot = mlab.pipeline.vector_cut_plane(src,
                                          mask_points = mask_points,
                                          scale_factor = scale_factor )
    
    return plot



def scalar_cut_plane_wrap( data ) :

    mlab.scalar_cut_plane( * data ) 


    
def flow_wrap( data ) :        
    ...


def volume_wrap( data ) :
    ...
        


def iso_surface_wrap( data, contours ) :
    mlab.pipeline.iso_surface(magnitude, contours = contours )

    



    
