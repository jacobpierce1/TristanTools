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

source = mlab.pipeline.vector_field( * data )
plot = mlab.pipeline.vector_cut_plane( source, plane_orientation = 'z_axes' )

# do things to modify plot here 


mlab.show()
mlab.draw()

# print_info( plot.stream_tracer ) 
