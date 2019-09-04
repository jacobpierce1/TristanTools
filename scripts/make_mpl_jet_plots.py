import os

import gc


# from numba import jit
import numpy as np
from scipy import sparse


import colorcet
from collections import Counter 
import sys 

import tristan_tools.analysis as analysis 

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

from mpl_toolkits.axes_grid1 import make_axes_locatable

import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# By default, the PySide binding will be used. If you want the PyQt bindings
# to be used, you need to set the QT_API environment variable to 'pyqt'
#os.environ['QT_API'] = 'pyqt'

# To be able to use PySide or PyQt4 and not run in conflicts with traits,
# we need to import QtGui and QtCore from pyface.qt
from pyface.qt import QtGui, QtCore
# Alternatively, you can bypass this line, but you need to make sure that
# the following lines are executed before the import of PyQT:
#   import sip
#   sip.setapi('QString', 2)



###################################################
# parse command line
print( sys.argv ) 



key_options = [ 'dens', 'densi',
                'jx', 'jy', 'jz',
                'bx', 'by', 'bz',
                'ex', 'ey', 'ez',
                'v3x', 'v3y', 'v3z' ]

scalar_data_key_options = key_options 

cmap_key_options = [ 'spectral', 'linear', 'div' ]

requested_keys = set() 

for x in sys.argv :
    if x in key_options :
        requested_keys += x 

if not requested_keys :
    requested_keys = set( key_options )

requested_keys = list( requested_keys ) 

print( 'requested_keys : ' + str( requested_keys ) ) 


stride = 1 
min_path_index = 1
if len( sys.argv ) > 1 :
    try :
        stride = int( sys.argv[1] )
        min_path_index = 2
    except :
        stride = 1
print( 'INFO: stride = %d' % stride ) 

analyzer_path = './'
if len( sys.argv ) > min_path_index and sys.argv[-1] not in key_options :
    analyzer_path = sys.argv[-1] 
    print( 'INFO: using analyzer path: ' + str( analyzer_path ) ) 

    
analyzer = analysis.TristanDataAnalyzer( analyzer_path + 'output/' )



def get_scalar_data( key, timestep  ) :

    if key in scalar_data_key_options :
        analyzer.load_indices( timestep, keys = [key] )
              
    elif key == 'gammae_max' :
        analyzer.compute_binned_particle_statistic( timestep, 'gammae', 'max' )
      
        
    elif key == 'gammai_max' :
        # return compute_max_gammas( 'i', timestep )
        analyzer.compute_binned_particle_statistic( 'gammai', 'max' )
        
    elif key == 'gammae_mean' :
        # return compute_mean_gammas( 'e', timestep )
        analyzer.compute_binned_particle_statistic( 'gammae', 'mean' )
        
    elif key == 'gammaei_mean' :
        # return compute_mean_gammas( 'i', timestep ) 
        analyzer.compute_binned_particle_statistic( 'gammai', 'mean' )

    return analyzer.data[ key ][ timestep ] 



keys = requested_keys    

# plot the scalar data

cmaps = { 'v3x' : 'div',
          'v3y' : 'div',
          'v3z' : 'spectral',    
          'jx' : 'div',
          'jy' : 'div',
          'jz' : 'div',
          'ex' : 'div',
          'ey' : 'div',
          'ez' : 'div',
          'bx' : 'div',
          'by' : 'div',
          'bz' : 'spectral',
          'dens' : 'spectral',
          'densi' : 'spectral' }



projection_names = [ 'xy', 'xz' ]

for key in keys :
    for projection_name in projection_names : 
        os.makedirs( analyzer_path + 'plots/%s/%s/' % ( projection_name, key ),
                     exist_ok = 1 ) 


timesteps = range( 0, len( analyzer ), stride )




for timestep in timesteps : 

    analyzer.load_indices( timestep, keys = ['time'] )
    time = analyzer.data[ 'time' ][ timestep ][0]

    print( 'time = %.3e w_pe^{-1}' % analyzer.data.time[ timestep ] )
    
    for i in range( len( keys ) ) :

        for projection in range(2) : 
        
            fig, ax = plt.subplots( 1, 1, figsize = ( 5, 5 ) )

            data = get_scalar_data( keys[i], timestep ) 

            cmap_key = cmaps[ keys[i] ]

            colormap = 'spectral'

            if cmap_key == 'spectral' : 
                cmap = colorcet.m_rainbow

            elif cmap_key == 'div' :
                cmap = colorcet.m_coolwarm

            else :
                cmap = reversed( colorcet.linear_bmy_10_95_c78 )

            if projection == 0 :
                projected_data = data[ :, :, int( data.shape[2] / 2 ) ]
            else : 
                projected_data = data[ :, int( data.shape[1] / 2 ), : ]
                
            im = ax.pcolormesh( projected_data, cmap = cmap )

            divider = make_axes_locatable( ax ) 
            cax = divider.append_axes( "right", size="5%", pad=0.05)
            cbar = fig.colorbar( im, cax = cax )

            ax.set_title( '%s: t=%d' % ( keys[i], int( time ) ) )

            plt.savefig( analyzer_path + 'plots/%s/%s/%03d.png' % ( projection_names[ projection ],
                                                                    keys[i], timestep ),
                         dpi = 400 )

            plt.clf()
            plt.close()

            # sys.exit( 1 ) 

            analyzer.unload_indices( timestep ) 
            gc.collect() 


    









