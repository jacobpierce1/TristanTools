import resource

def print_memory_usage () :
    print( resource.getrusage(resource.RUSAGE_SELF).ru_maxrss ) 

print_memory_usage()
    
import numpy as np
import tristan_tools.analysis as analysis
import sys 
import os
from pprint import pprint
# import psutil 



output_path_2d = '~/jacob_astroplasmas/tristan/tests/user_beam_on_background_2d/unif_field/output'
output_path_2d = os.path.expanduser( output_path_2d ) 

output_path_3d = '' 

# process = psutil.Process(os.getpid())

# def print_memory_usage() : 
#     print(process.memory_info().rss)


print_memory_usage() 

# def print_size( description, obj ) :
#     print( description + '---> size: ' + str( sys.getsizeof( obj ) ) )


x = analysis.TristanDataContainer( output_path_2d ) 
# print_size( 'before load', x ) 

x.load_params()
# print_size( 'after loading params', x ) 
print_memory_usage() 


x.load_all()

print_memory_usage()

# print_size( 'after loading all', x ) 


# b.load_all() 

# pprint( b.params ) 


# a.load( output_path_2d,  ) 


