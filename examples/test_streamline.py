import os
os.environ['ETS_TOOLKIT'] = 'qt4'
os.environ['QT_API'] = 'pyqt5'

from mayavi import mlab
import tristan_tools.analysis as analysis 




output_path_3d = '../test_data/test1/output/'



timestep = 1



output_path = output_path_3d
os.path.expanduser( output_path ) 

analyzer = analysis.TristanDataAnalyzer( output_path )

# analyzer.print_keys() 


analyzer.load_indices( [timestep ] ) 


keys = [ 'bx', 'by', 'bz' ]
data = [ analyzer.data[x][ timestep ] for x in keys ]

plot  = mlab.flow( * data, seed_resolution = 1, seedtype = 'point', integration_direction = 'both',
                   linetype = 'line' ) 


plot.stream_tracer.maximum_number_of_steps = 4000 

plot.stream_tracer.maximum_propagation = 400

# mlab.pipeline.streamline( *data ) 

mlab.show() 



from pprint import pprint

def print_info( obj ) :

    print( type( obj ) )
    print('') 
    pprint( vars( obj ) )
    print('') 
    pprint( dir( obj ) ) 
    print('') 
    pprint( obj.trait_names() ) 



print_info( plot.stream_tracer ) 
