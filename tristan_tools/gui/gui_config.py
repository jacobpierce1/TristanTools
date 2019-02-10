

DEVELOPER_MODE = 1

# dimensions of the gui main window in pixels 
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 1000 

# number of rows and cols in the array of plots
NUM_PLOT_ROWS = 1
NUM_PLOT_COLS = 2



# this is the number of timesteps ahead and behind that we will look.
# so 2 * DATA_LOADER_BUFFER_SIZE + 1  is the total amount of data
# that is loaded at any given time. for small datasets, you may as well
# make this number large.
DATA_LOADER_FORWARD_TIMESTEPS = 10

# max number of threads that will run at any given time
# by the data loader. 
DATA_LOADER_NUM_THREADS = 6


# change this if you subclass the analyzer and want to use
# a different one for your analysis 
import tristan_tools.analysis as analysis
analyzer = analysis.TristanDataAnalyzer 
