from mayavi import mlab
import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint





class MayaviWrapError( Exception ) :
    pass 



    



def print_mayavi_info( obj, traits = 1  ) :

    print( type( obj ) )
    print( obj ) 
    print('\n\n\n') 
    pprint( vars( obj ) )
    print('\n\n\n') 
    pprint( dir( obj ) )

    if traits : 
        print('\n\n\n') 
        pprint( sorted( obj.trait_names() ) ) 
        print('\n\n\n') 
        pprint( sorted( obj.editable_traits() ) ) 



        
def vector_cut_plane_wrap( data,
                           mask_points = 1,
                           scale_factor = 1,
                           remove_arrow = 1,
                           glyph_source = 1, #options: 1 = arrow 
                           shaft_radius = 0.03,
                           shaft_resolution = 6,
                           tip_length = 0.35,
                           tip_radius = 0.1,
                           tip_resolution = 6,
                           glyph_position = 'tail', # options:
                           scale_mode = 'scale_by_vector', # options: 'scale_by_vector', 'data_scaling_off' 
                           color_mode = 'color_by_vector', #options:
                           tubing = 0 ) : 

    if( len( data ) != 3 ) :
        raise MayaviWrapError( 'ERROR: len( data != 3 )' )
        
    
    src = mlab.pipeline.vector_field( * data )
    
    plot = mlab.pipeline.vector_cut_plane(src,
                                          mask_points = mask_points,
                                          scale_factor = scale_factor )

    if remove_arrow :
        ... 
    
    return plot






def volume_slice_wrap( data,
                       plane_orientation = 'x_axes',  # options: 'x_axes', 'y_axes', 'z_axes' 
                       slice_index = 0 ) :

    plot = mlab.volume_slice( data,
                              plane_orientation = plane_orientation,
                              slice_index = slice_index ) 

    return plot 




    
    
def flow_wrap( data ) :        
    ...





    

def volume_wrap( data, vmin = 0, vmax = 1 ) :
    s = mlab.pipeline.scalar_field( data ) 
    plot = mlab.pipeline.volume( s, vmin = vmin, vmax = vmax )

    return plot 
        



    
def iso_surface_wrap( data,
                      contours,
                      opacity = 1 ) :

    plot = mlab.pipeline.iso_surface( data,
                                      contours = contours,
                                      opacity = opacity )
    
    return plot



 
def contour3d_wrap( data,
                    contours,
                    opacity = 1 ) :

    plot = mlab.contour3d( data,
                           contours = contours,
                           opacity = opacity )
    
    return plot 
    



    
