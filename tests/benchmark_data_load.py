import tristan_tools.analysis as analysis
import timeit
import threading


# USE_THREAD = 1 


output_path = '../test_data/user_beam_on_background_3d/output'


analyzer = analysis.TristanDataAnalyzer( output_path ) 

def without_thread() :
    analyzer.load_indices( range(10), keys = [ 'bx'], _reload = 1  ) 



def with_thread() :
    x = threading.Thread( target = without_thread )
    x.start()
    x.join() 
    
out = timeit.timeit( without_thread, number = 100 ) 
print( out ) 
print( type( out ) ) 
