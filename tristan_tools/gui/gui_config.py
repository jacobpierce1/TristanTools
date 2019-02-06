
# dimensions of the gui main window in pixels 
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600 

# number of rows and cols in the array of plots
NUM_PLOT_ROWS = 1
NUM_PLOT_COLS = 2


# change this if you subclass the analyzer and want to use
# a different one for your analysis 
import tristan_tools.analysis as analysis
analyzer = analysis.TristanDataAnalyzer 
