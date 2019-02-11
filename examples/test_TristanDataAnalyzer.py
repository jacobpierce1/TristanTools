import tristan_tools.analysis as analysis 
import os



# output_path_2d = '~/jacob_astroplasmas/tristan/tests/user_beam_on_background_2d/unif_field/output'
# output_path_2d = os.path.expanduser( output_path_2d ) 

# output_path_3d = '' 
# output_path_3d = os.path.expanduser( output_path_3d ) 


output_path_3d = '../test_data/user_beam_on_background_3d/output/'


output_path = output_path_3d
os.path.expanduser( output_path ) 

analyzer = analysis.TristanDataAnalyzer( output_path )

# analyzer.print_keys() 


analyzer.load_indices( [5] ) 
# analyzer.print_shapes( 5 )


# print( analyzer.data.che[5] ) 

# uncomment to see that it loaded 
# print( analyzer.data[0] ) 

# compute all quantities at index 0 


analyzer.compute_indices( 5, recompute = 0, save = 1  ) 

