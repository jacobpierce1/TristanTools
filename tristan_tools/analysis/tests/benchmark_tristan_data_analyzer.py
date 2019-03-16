import tristan_tools.analysis as analysis 

import numpy as np 
import os


import time


output_path_3d = '../../../test_data/test1/output/'



output_path = output_path_3d
os.path.expanduser( output_path ) 

analyzer = analysis.TristanDataAnalyzer( output_path )

# analyzer.print_keys() 

timestep = 5

analyzer.load_indices( timestep )





def benchmark( func, num_iterations = 100, description = '' ) : 

    times = np.zeros( num_iterations + 1 )
    times[0] = time.time() 
    
    # start = time.time() 
    
    for i in range( num_iterations ) :
        func()
        times[i+1] = time.time() 
        
    timediff = np.ediff1d( times ) 
    
    a = min( timediff )
    b = max( timediff )
    mean = np.mean( timediff )
    std = np.std( timediff ) 
    
    
    msg = 'min = %.3e s, max = %.3e s, mean = %.3e s, std = %.3e s, N = %d' % (a, b, mean, std, num_iterations)

    if description :
        msg += ', ' + description
    
    print( msg )

            

benchmark( lambda : analyzer.compute_EE( timestep ), 100, 'compute_EE' )
benchmark( lambda : analyzer.compute_E_parallel( timestep ), 100, 'compute_E_parallel' )
benchmark( lambda : analyzer.compute_total_momentum_spectrum( timestep, 'e' ), 100, 'compute_total_momentum_spectrum' ) 
    


        # analyzer.compute_total_momentum_spectrum( timestep )








# print_info( plot.stream_tracer ) 
