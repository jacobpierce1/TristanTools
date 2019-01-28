import numpy as np
import tristan_tools.analysis as analysis
import sys 
import os
from pprint import pprint
# import psutil 



output_path_2d = '~/jacob_astroplasmas/tristan/tests/user_beam_on_background_2d/unif_field/output'
output_path_2d = os.path.expanduser( output_path_2d ) 

output_path_3d = '' 
output_path_3d = os.path.expanduser( output_path_3d ) 

output_path = output_path_2d

x = analysis.TristanDataContainer( output_path ) 

x.print_keys() 
print( '\n\n\n' ) 



# print( x.params ) 

# x.load_params()

x.load_indices( [0] ) 


x.print_shapes( 0 )

print( x.data.bx[0] )

print( x.data[0]['bx'] ) 


# print( x )

# plotter = analysis.TristanDataPlotter( x ) 

# print( plotter ) 

