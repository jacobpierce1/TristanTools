import os
import sys 
# os.environ['ETS_TOOLKIT'] = 'qt4'
# os.environ['QT_API'] = 'pyqt5'
# os.environ['QT_API'] = 'pyqt'

# from mayavi import mlab 
import numpy as np

import matplotlib


show = 1
if len( sys.argv ) == 3 and sys.argv[2] == '0' :
    show = 0

if not show :
    matplotlib.use( 'Agg' )

import matplotlib.pyplot as plt



import colorcet
import matplotlib.animation as animation
from collections import Counter 
import sys 

import tristan_tools.analysis as analysis 

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

from mpl_toolkits.axes_grid1 import make_axes_locatable

import gc 


os.makedirs( './plots/', exist_ok = 1 ) 



analyzer = analysis.TristanDataAnalyzer( './output' )






downsample = 1
if len( sys.argv ) > 1 :
    downsample = int( sys.argv[1] )

    
load = 1
if len( sys.argv ) > 2 :
    load = int( sys.argv[2] )

    
timesteps = np.arange( 0, len(analyzer), downsample, dtype = int )    

print( timesteps ) 


for j in range( len( timesteps ) ) :

    print( j ) 

    timestep = timesteps[j]
    print( timestep )

    keys = [ 'gammae', 'gammai' ]
    # ops = [ 'max', 'mean' ] 
    ops = [ 'max' ] 
    
    for key in keys :
        print( key )

        for op in ops :
            print( op ) 

            analyzer.compute_binned_particle_statistic( timestep, key, op, load = load  )
            gc.collect() 


if show: 
    plt.show() 
