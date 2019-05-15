from mayavi import mlab
import tristan_tools.analysis as analysis
import os
import sys


cwd = os.getcwd()

# check if cwd is the output directory 
if os.path.basename( cwd ) == 'output' :
    data_path = cwd
    
# check if there's a directory called 'output' in cwd
else :
    tmp = os.path.join( cwd, 'output' )
    if os.path.exists( tmp ) :
        data_path = tmp
    else :
        data_path = None 

if data_path :
    print( 'INFO: found data at path: %s' % data_path )
else : 
    print( 'ERROR: did not find tristan output data path' )
    sys.exit( 0 ) 

# set the type of analyzer to be used in the gui_config.py
analyzer = analysis.TristanDataAnalyzer( data_path ) 





timestep = 1


analyzer.load_indices( [timestep ], keys = 'dens' )

print( [ x for x in analyzer.data ] )

print( type( analyzer.data ) ) 

# source = mlab.pipeline.vector_field( * data )

print( analyzer.data.dens[ timestep ] )

plot = mlab.pipeline.scalar_cut_plane( analyzer.data.dens[1], plane_orientation = 'z_axes' )

# plot = mlab.pipeline.warp_vector_cut_plane( source ) 

# print_info( plot.glyph.glyph_source.glyph_source ) 

# print( plot.glyph.glyph_source.glyph_list ) 

# plot.glyph.scale_mode = 'data_scaling_off'


# plot.glyph.mask_input_points = True
# plot.glyph.mask_points.on_ratio = 10
# plot.glyph.mask_points.random_mode = False
# plot.glyph.glyph_source.glyph_source = plot.glyph.glyph_source.glyph_list[1]
# plot.glyph.glyph_source.glyph_source.shaft_radius = 0.03
# plot.glyph.glyph_source.glyph_source.shaft_resolution = 6
# plot.glyph.glyph_source.glyph_source.tip_length = 0.35
# plot.glyph.glyph_source.glyph_source.tip_radius = 0.1
# plot.glyph.glyph_source.glyph_source.tip_resolution = 6
# plot.glyph.glyph.scale_factor = 5
# plot.glyph.glyph_source.glyph_position = 'tail'
# plot.glyph.scale_mode = 'scale_by_vector'
# plot.glyph.color_mode = 'color_by_vector'
# plot.implicit_plane.normal = (1, 0, 0) # set normal to Ox axis
# plot.implicit_plane.origin = (10, 25, 25) # set origin to (i=10, j=25, k=25) for a structured grid
# plot.actor.property.diffuse = 0.0 # set some color properties
# plot.actor.property.ambient = 1.0 # 
# plot.actor.property.opacity = 1.0 #
# # plot.module_manager.vector_lut_manager.data_range = [0, 1]

# plot.implicit_plane.widget.tubing = False

# plot.implicit_plane.widget.diagonal_ratio = 0
# plot.implicit_plane.widget.handle_size = 0.001


# plot.implicit_plane.widget._vtk_obj.SetNormalToZAxis(1)

# print_info( plot.glyph.mask_points ) 

mlab.show()
# mlab.draw()




