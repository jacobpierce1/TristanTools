import os
os.environ['ETS_TOOLKIT'] = 'qt4'

# use pyqt5 if possible
try :
    os.environ['QT_API'] = 'pyqt5'
    from mayavi import mlab

except :
    os.environ['QT_API'] = 'pyq'
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
                           plane_orientation = 'x_axes',
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
                           tubing = 0,
                           figure = None ) : 

    if figure is None :
        figure = mlab.gcf()
    
    if len( data ) != 3  :
        raise MayaviWrapError( 'ERROR: len( data != 3 )' )
        
    
    src = mlab.pipeline.vector_field( * data )
    
    plot = mlab.pipeline.vector_cut_plane( src,
                                           plane_orientation = plane_orientation,
                                           mask_points = mask_points,
                                           scale_factor = scale_factor,
                                           figure = figure )
    
    # plot.glyph.mask_input_points = True 
    # plot.glyph.mask_points.on_ratio = self.mask_points
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
    # plot.glyph.glyph.scale_factor = self.scale_factor 
    plot.glyph.glyph_source.glyph_position = 'tail'
    
    if remove_arrow :
        ... 
    
    return plot






def volume_slice_wrap( data,
                       plane_orientation = 'x_axes',  # options: 'x_axes', 'y_axes', 'z_axes' 
                       slice_index = 0,
                       figure = None ) :
    if figure is None :
        figure = mlab.gcf()
        
    plot = mlab.volume_slice( data,
                              plane_orientation = plane_orientation,
                              slice_index = slice_index,
                              figure = figure ) 

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
    



    
