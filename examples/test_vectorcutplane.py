# https://scipy-cookbook.readthedocs.io/items/MayaVi_ScriptingMayavi2_MainModules.html
# from above site: 
# vcp = VectorCutPlane()
# script.add_module(vcp)
# vcp.glyph.mask_input_points = True
# vcp.glyph.mask_points.on_ratio = 5
# vcp.glyph.mask_points.random_mode = False
# vcp.glyph.glyph_source = vcp.glyph.glyph_list[1]
# vcp.glyph.glyph_source.shaft_radius = 0.03
# vcp.glyph.glyph_source.shaft_resolution = 6
# vcp.glyph.glyph_source.tip_length = 0.35
# vcp.glyph.glyph_source.tip_radius = 0.1
# vcp.glyph.glyph_source.tip_resolution = 6
# vcp.glyph.glyph.scale_factor = 20
# vcp.glyph.glyph_position = 'tail'
# vcp.glyph.scale_mode = 'scale_by_vector'
# vcp.glyph.color_mode = 'color_by_vector'
# vcp.implicit_plane.normal = (1, 0, 0) # set normal to Ox axis
# vcp.implicit_plane.origin = (10, 25, 25) # set origin to (i=10, j=25, k=25) for a structured grid
# vcp.implicit_plane.widget.enabled = True
# vcp.actor.property.diffuse = 0.0 # set some color properties
# vcp.actor.property.ambient = 1.0 # 
# vcp.actor.property.opacity = 1.0 #
# vcp.module_manager.vector_lut_manager.data_range = [0, 1]


import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)



import os
os.environ['ETS_TOOLKIT'] = 'qt4'
os.environ['QT_API'] = 'pyqt5'

from mayavi import mlab
import tristan_tools.analysis as analysis 

import numpy as np 


from pprint import pprint

def print_info( obj, traits = 1  ) :

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


output_path_3d = '../test_data/test1/output/'



timestep = 1



output_path = output_path_3d
os.path.expanduser( output_path ) 

analyzer = analysis.TristanDataAnalyzer( output_path )

# analyzer.print_keys() 


analyzer.load_indices( [timestep ] ) 


keys = [ 'bx', 'by', 'bz' ]
data = [ analyzer.data[x][ timestep ] for x in keys ]

# plot  = mlab.flow( * data, seed_resolution = 1, seedtype = 'point', integration_direction = 'both',
#                    linetype = 'line' ) 

source = mlab.pipeline.vector_field( * data )
plot = mlab.pipeline.vector_cut_plane( source, plane_orientation = 'z_axes' )

# plot = mlab.pipeline.warp_vector_cut_plane( source ) 

# print_info( plot.glyph.glyph_source.glyph_source ) 

# print( plot.glyph.glyph_source.glyph_list ) 

plot.glyph.scale_mode = 'data_scaling_off'


plot.glyph.mask_input_points = True
plot.glyph.mask_points.on_ratio = 10
plot.glyph.mask_points.random_mode = False
plot.glyph.glyph_source.glyph_source = plot.glyph.glyph_source.glyph_list[1]
plot.glyph.glyph_source.glyph_source.shaft_radius = 0.03
plot.glyph.glyph_source.glyph_source.shaft_resolution = 6
plot.glyph.glyph_source.glyph_source.tip_length = 0.35
plot.glyph.glyph_source.glyph_source.tip_radius = 0.1
plot.glyph.glyph_source.glyph_source.tip_resolution = 6
plot.glyph.glyph.scale_factor = 5
plot.glyph.glyph_source.glyph_position = 'tail'
plot.glyph.scale_mode = 'scale_by_vector'
plot.glyph.color_mode = 'color_by_vector'
plot.implicit_plane.normal = (1, 0, 0) # set normal to Ox axis
plot.implicit_plane.origin = (10, 25, 25) # set origin to (i=10, j=25, k=25) for a structured grid
plot.actor.property.diffuse = 0.0 # set some color properties
plot.actor.property.ambient = 1.0 # 
plot.actor.property.opacity = 1.0 #
# plot.module_manager.vector_lut_manager.data_range = [0, 1]

plot.implicit_plane.widget.tubing = False

plot.implicit_plane.widget.diagonal_ratio = 0
plot.implicit_plane.widget.handle_size = 0.001

# plot.implicit_plane.widget.origin_translation = False

# plot.implicit_plane.widget.interactor.enabled = False

# plot.implicit_plane.widget._vtk_obj.SetEnabled( 0 )

# plot.implicit_plane.widget._vtk_obj.SetOriginTranslation(0) 


# plot.implicit_plane.widget.origin += np.array( [0,0,0.001] ) 

# print( plot.implicit_plane.widget._vtk_obj.GetHandleSizeMinValue() ) 
# print( plot.implicit_plane.widget._vtk_obj.GetDiagonalRatioMinValue() ) 

# print_info( plot.implicit_plane.widget.interactor.render_window._vtk_obj, traits = 0 )

# plot.implicit_plane.widget.interactor.render_window._vtk_obj.Render() 
# plot.implicit_plane.widget.interactor.render_window() 

# plot.implicit_plane.widget._vtk_obj.RemoveAllObservers()
# plot.glyph.glyph_source.glyph_source = plot.glyph.glyph_source.glyph_list[1]
# plot.glyph.glyph_source.glyph_source.shaft_radius = 0.03

# print_info( plot.actors ) 

# plot.draw()

# print_info( plot.implicit_plane.widget.interactor.picker )

# plot.implicit_plane.widget.interactor.picker.pick_position = ( 0, 0, 0.1 ) 


# print_info( plot.glyph  )
plot.implicit_plane.widget._vtk_obj.SetNormalToZAxis(1)

print_info( plot.glyph.mask_points ) 

mlab.show()
mlab.draw()

# print_info( plot.stream_tracer ) 
