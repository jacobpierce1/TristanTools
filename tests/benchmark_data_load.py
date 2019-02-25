import tristan_tools.analysis as analysis
import timeit
import threading


import cProfile


# USE_THREAD = 1 


output_path = '../test_data/test1/output'


analyzer = analysis.TristanDataAnalyzer( output_path ) 

# def without_thread() :
#     analyzer.load_indices( 1, keys = [ 'bx'], _reload = 1  ) 



# def with_thread() :
#     x = threading.Thread( target = without_thread )
#     x.start()
#     x.join() 


pr = cProfile.Profile()
pr.enable()


for i in range(10) : 
    analyzer.load_indices( _reload = 1 )
    analyzer.compute_indices( recompute = 1 ) 
 
pr.disable()
pr.print_stats( sort = 'cumtime' ) 

# out = timeit.repeat( without_thread, number = 100, repeat = 10 )

# print( out ) 
# print( type( out ) ) 
