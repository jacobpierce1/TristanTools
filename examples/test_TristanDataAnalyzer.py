import tristan_tools.analysis as analysis 
import os



output_path_2d = '~/jacob_astroplasmas/tristan/tests/user_beam_on_background_2d/unif_field/output'
output_path_2d = os.path.expanduser( output_path_2d ) 

output_path_3d = '' 
output_path_3d = os.path.expanduser( output_path_3d ) 

output_path = output_path_2d

analyzer = analysis.TristanDataAnalyzer( output_path )

analyzer.print_keys() 

analyzer.load_indices( [0] ) 

# uncomment to see that it loaded 
# print( analyzer.data[0] ) 

# compute all quantities at index 0 
analyzer.compute_indices( [0] ) 



print( analyzer.computations[0] ) 


print( analyzer.computations.BB[0].shape ) 
