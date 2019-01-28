import numpy as np
import tristan_tools.analysis as analysis
import sys 
import os
from mayavi import mlab 



output_path_2d = '~/jacob_astroplasmas/tristan/tests/user_beam_on_background_2d/unif_field/output'
output_path_2d = os.path.expanduser( output_path_2d ) 

output_path_3d = '~/jacob_astroplasmas/tristan/tests/user_beam_on_background_3d_2/output/'
output_path_3d = os.path.expanduser( output_path_3d ) 

output_path = output_path_3d



tristan_data = analysis.TristanDataContainer( output_path ) 

# data.print_keys() 

# print( x.params ) 

idx = 30 

tristan_data.load_indices( [idx] ) 

print( tristan_data.data.bx[30].shape ) 

sys.exit(0)



# x, y, z = np.ogrid[-5:5:64j, -5:5:64j, -5:5:64j]

# print( x )
# print( x.shape )

# print

# scalars = x * x * 0.5 + y * y + z * z * 2.0

obj = mlab.volume_slice( tristan_data.data.bz[idx], plane_orientation='x_axes')

mlab.show()


bx, by, bz = [ tristan_data.data[key][idx] for key in ['bx', 'by', 'bz'] ]

mlab.quiver3d( bx, by, bz )

mlab.show() 

mlab.flow( bx, by, bz ) 

mlab.show()

    
