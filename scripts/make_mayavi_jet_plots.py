import os
import sys 
os.environ['ETS_TOOLKIT'] = 'qt4'

# use pyqt5 if possible

if 'USING_GPU' in os.environ :  
    os.environ['QT_API'] = 'pyqt'
else :
    os.environ['QT_API'] = 'pyqt5'


import gc
from mayavi import mlab
mlab.options.offscreen = True


# from numba import jit
import numpy as np
from scipy import sparse


import colorcet
import matplotlib.animation as animation
from collections import Counter 
import sys 

import tristan_tools.analysis as analysis 
import tristan_tools.plotting as plotting

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

from mpl_toolkits.axes_grid1 import make_axes_locatable

import sys



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

from traits.api import HasTraits, Instance, on_trait_change
from traitsui.api import View, Item
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, \
        SceneEditor


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

plot_type = 'vslice'
    

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



for key in keys :
    os.makedirs( analyzer_path + 'plots/' + key, exist_ok = 1 ) 


timesteps = range( 0, len( analyzer ), stride )
        
for timestep in timesteps : 

    analyzer.load_indices( timestep, keys = ['time'] )
    time = analyzer.data[ 'time' ][ timestep ][0]

    print( 'time = %.3e w_pe^{-1}' % analyzer.data.time[ timestep ] )
    
    for i in range( len( keys ) ) :
        
        data = get_scalar_data( keys[i], timestep ) 

        cmap_key = cmaps[ keys[i] ]
    
        mlab.figure( size = ( 1000, 1000 ) ) 

        mlab.view( azimuth = 0, elevation = 90, roll = 180, distance = 200 )


        cmap = list( reversed( colorcet.linear_bmy_10_95_c78 ) )
        # cmap = list( reversed( colorcet.rainbow_bgyrm_35_85_c71 ) )

        colormap = 'spectral'

        if cmap_key == 'spectral' : 
            colormap = 'spectral'

        elif cmap_key == 'div' :
            colormap = 'RdBu'

        if plot_type == 'vslice'  : 
            plot = mlab.volume_slice( data,
                                      colormap = colormap,
                                      plane_orientation = 'x_axes',
                                      slice_index = data.shape[ 0 ] / 2 )

        elif plot_type == 'contour' :
            m = np.amax( data ) 
            contours = list( np.linspace( m/4, m - 2, 3 ) )
            plotting.contour3d_wrap( data,
                                     contours = contours,
                                     opacity = 0.1 )


        # print( cmap[2] )


        if cmap_key == 'linear' : 
            lut_table = np.zeros( ( len( cmap ), 3 ) )
            new_table = np.append( 255 * np.array( cmap ),
                                   255 * np.ones( ( len( cmap ), 1 ) ),
                                   axis = 1 )
            print( new_table.shape ) 


            plot.module_manager.scalar_lut_manager.lut.number_of_colors = len( new_table )
            plot.module_manager.scalar_lut_manager.lut.table = new_table 

        mlab.title( '%s: t=%d' % ( keys[i], int( time ) ) )
            
        mlab.colorbar( orientation = 'vertical' )

        mlab.outline() 
        mlab.axes() 
        mlab.orientation_axes() 
        mlab.axes( nb_labels = 4, line_width = 4 )
               
        
        mlab.colorbar( orientation = 'vertical' )

        mlab.outline() 
        mlab.axes() 
        mlab.orientation_axes() 
        mlab.axes( nb_labels = 4, line_width = 4 )
        
        mlab.savefig( analyzer_path + 'plots/%s/%03d.png' % ( keys[i], timestep ) )

        # print( mlab.view() ) 
        # mlab.show()

        
        # mlab.clf()
        mlab.clf()
        mlab.close()
        
        # sys.exit( 1 ) 

        analyzer.unload_indices( timestep ) 
        gc.collect() 
        

    









