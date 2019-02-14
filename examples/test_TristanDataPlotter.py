import matplotlib.pyplot as plt 
import tristan_tools.analysis as analysis 
import os

output_path_3d = '../test_data/user_beam_on_background_3d/output/'


output_path = output_path_3d
os.path.expanduser( output_path ) 

analyzer = analysis.TristanDataAnalyzer( output_path )



plot_time = 0

analyzer.load_indices( plot_time ) 

analyzer.compute_indices( plot_time ) 

analyzer.print_shapes( plot_time )  


plotter = analysis.TristanDataPlotter( analyzer, plot_type = 'hist1d', keys = [ 'PP_e_spec' ] )

print( plotter.plotter.data ) 

ax = plt.axes()
plotter.set_plotter_canvas( ax ) 


plotter.plot_timestep( plot_time )
plotter.timestep = plot_time + 1 
plotter.plot_timestep( plot_time ) 

plt.show() 
