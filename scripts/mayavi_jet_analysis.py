import os
import sys 
os.environ['ETS_TOOLKIT'] = 'qt4'

# use pyqt5 if possible

if 'qt4' in sys.argv : 
    os.environ['QT_API'] = 'pyqt'
else :
    os.environ['QT_API'] = 'pyqt5'

from mayavi import mlab

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

import gc 
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




cmap_key_options = [ 'spectral', 'linear', 'div' ]

scalar_data_key_options = [ 'dens', 'densi',
                            'jx', 'jy', 'jz',
                            'bx', 'by', 'bz',
                            'ex', 'ey', 'ez',
                            'v3x', 'v3y', 'v3z' ]

scalar_computable_key_options = [ 'gammae_mean', 'gammai_mean',
                                  'gammae_max', 'gammai_max' ] 


scalar_plot_options = [ 'vslice', 'contour' ]

vector_data_key_options = [ 'j', 'b', 'e', 'v3' ]

vector_plot_options = [ 'vcp', 'flow' ] 

all_data_key_options = list( scalar_data_key_options ).extend( vector_data_key_options )

all_plot_options = list( scalar_plot_options ).extend(
    vector_plot_options )



def print_help_message() :

    print( 'python mayavi_jet_analysis.py <timestep> <data_data_key> <plot_type> <qt4>' )
    print( 'scalar_data_key_options: ' + str( scalar_data_key_options ) )
    print( 'scalar_plot_options: ' + str( scalar_plot_options ) )
    print( 'vector_data_key_options: ' + str( vector_data_key_options ) )
    print( 'vector_plot_options: ' + str( scalar_plot_options ) )
    print( 'colormap options: ' + str( cmap_key_options ) )
    

if len( sys.argv ) < 2 :
    print( 'ERROR: arg 1 = timstep not specified' )
    print_help_message() 
    sys.exit( 0 )

timestep = int( sys.argv[1] )
print( 'INFO: timestep = %d' % timestep )


try : 
    data_key = sys.argv[2] 
except :
    print_help_message()
    sys.exit(0)

try : 
    plot_type = sys.argv[3] 
except :
    print_help_message()
    sys.exit(0)


try :
    cmap_key = sys.argv[4]
except :
    print_help_message()
    sys.exit(0)



    
if data_key in scalar_data_key_options or data_key in scalar_computable_key_options :
    using_scalar_key = 1
    if plot_type not in scalar_plot_options :
        print( 'ERROR: invalid plot_type' )
        print_help_message()
        sys.exit(0)
        
elif data_key in vector_data_key_options :
    using_scalar_key = 0
    if plot_type not in vector_plot_options :
        print( 'ERROR: invalid plot_type' )
        print_help_message()
        sys.exit(0)
        
else :
    print( 'ERROR: invalid data_key' )
    print_help_message()
    sys.exit(0)


if cmap_key not in cmap_key_options :
    print( 'ERROR: invalid cmap' )
    print_help_message()
    sys.exit(0)
    
# mode = 0
    
# if len( sys.argv ) >= 3 :
#     mode = int( sys.argv[2] )
    





analyzer = analysis.TristanDataAnalyzer( './output' )



from pprint import pprint
        
def print_info( obj ) :
    print( type( obj ) )
    print()

    if hasattr( obj, '__dict__' ) :
        pprint( vars( obj ) )
        print()
        
    pprint( dir( obj ) )
    print()

    if isinstance( obj, HasTraits ) :
        pprint( obj.trait_names() )
        print() 



# def jet_analysis_data_getter( n, analyzer ) :
#     analyzer.unload_indices( n-1 )
#     analyzer.load_indices( n, keys = [ 'dens', 'densi',
#                                        'bx', 'by', 'bz',
#                                        'jx', 'jy', 'jz',
#                                        'ex', 'ey', 'ez',
#                                        'time' ] )
#     analyzer.compute_indices( n, keys = [ 'dense' ] ) 


# if mode == 0 : 
#     jet_analysis_data_getter( timestep, analyzer ) 

# elif mode == 1 or mode == 2 :
#     analyzer.load_indices( timestep, keys = [ 'dens', 'time' ] )
#     print( 'time = %.3e w_pe^{-1}' % analyzer.data.time[ timestep ] )









# ################################################################################
# #The actual visualization
# class Visualization(HasTraits):
#     scene = Instance(MlabSceneModel, ())
    
#     # @on_trait_change('scene.activated')
#     # def update_plot(self):
#     #     # This function is called when the view is opened. We don't
#     #     # populate the scene when the view is not yet open, as some
#     #     # VTK features require a GLContext.

#     #     # We can do normal mlab calls on the embedded scene.
#     #     self.scene.mlab.test_points3d()

#     # the layout of the dialog screated
#     view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
#                      height=250, width=300, show_label=False),
#                 resizable=True # We need this to resize with the parent widget
#                 )


# ################################################################################
# # The QWidget containing the visualization, this is pure PyQt4 code.
# class MayaviQWidget(QtGui.QWidget):

#     def __init__(self, data, parent=None):
#         QtGui.QWidget.__init__(self, parent)
#         layout = QtGui.QVBoxLayout(self)
#         layout.setContentsMargins(0,0,0,0)
#         layout.setSpacing(0)
#         self.visualization = Visualization()

#         # If you want to debug, beware that you need to remove the Qt
#         # input hook.
#         #QtCore.pyqtRemoveInputHook()
#         #import pdb ; pdb.set_trace()
#         #QtCore.pyqtRestoreInputHook()

#         # The edit_traits call will generate the widget to embed.
#         self.ui = self.visualization.edit_traits(parent=self,
#                                                  kind='subpanel').control
#         layout.addWidget(self.ui)
#         self.ui.setParent(self)

    
#     def get_mayavi_scene( self ) :
#         return self.visualization.scene.mayavi_scene 


        
# # if __name__ == "__main__":
# if mode == 0 :
#     # Don't create a new QApplication, it would unhook the Events
#     # set by Traits on the existing QApplication. Simply use the
#     # '.instance()' method to retrieve the existing one.
#     app = QtGui.QApplication.instance()
#     container = QtGui.QWidget()
#     container.setWindowTitle("Embedding Mayavi in a PyQt4 Application")
#     # define a "complex" layout to test the behaviour
#     layout = QtGui.QGridLayout(container)

#     dens_keys = [ 'dense', 'densi', 'dens' ]
#     plane_orientations = [ 'x_axes', 'z_axes' ]
#     slice_axes = [ 0, 2 ] 

#     field_keys = [ [ 'bx', 'by', 'bz' ],
#                    [ 'ex', 'ey', 'ez' ],
#                    [ 'jx', 'jy', 'jz' ] ]
                   
#     for i in range(2) :
#         for j in range(3):
#             x = MayaviQWidget( container)
#             layout.addWidget(x, i, j)

#             figure = x.get_mayavi_scene()

#             data = analyzer.data[ dens_keys[ j ] ][ timestep ] 
            
#             plotting.volume_slice_wrap( data,
#                                         plane_orientation = plane_orientations[ i ],
#                                         slice_index = data.shape[ slice_axes[ i ] ] / 2,
#                                         figure = figure )

#             mlab.colorbar( orientation = 'vertical' )

#             data = [ analyzer.data[ key ][ timestep ]
#                      for key in field_keys[ j ] ] 

#             print( data[0].shape ) 
#             mask_points = int( np.prod( data[0].shape ) / 40**3 )
#             print( 'mask_points = %d' % mask_points ) 
            
#             plotting.vector_cut_plane_wrap( data,
#                                             plane_orientation = plane_orientations[ i ],
#                                             figure = figure,
#                                             mask_points = mask_points,
#                                             scale_factor = 8 )
            
#             mlab.outline( figure = figure ) 
#             mlab.axes( figure = figure ) 
#             mlab.orientation_axes( figure = figure ) 

#             if i == 0 : 
#                 mlab.view( azimuth = 0, elevation = 90, roll = 0  )
            
            
    
            
#     window = QtGui.QMainWindow()
#     window.setCentralWidget(container)
#     window.show()

#     # Start the main event loop.
#     app.exec_()




# def set_scalar_lut_from_mpl_cmap( ) ;
# ...



# elif mode == 1 or mode == 2 :
#mlab.figure( 10, 8 ) 


def get_scalar_data( key, timestep  ) :

    if key in scalar_data_key_options :

        analyzer.load_indices( timestep, keys = [key] )
        # return analyzer.data[ key ][ timestep ]

    # else :
        # analyzer.compute_indices( timestep, keys = [key] ) 
        # return analyzer.data[ key ][ timestep ]
        
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


    

        
# def compute_mean_gammas( particle_type, timestep ) :

#     if particle_type == 'e' :
#         gamma_key ='gammae'
#         coords_keys = [ 'xe', 'ye', 'ze' ]

#     elif particle_type == 'i' :
#         gamma_key = 'gammai'
#         coords_keys = [ 'xi', 'yi', 'zi' ]

#     else :
#         print( 'ERROR: unrecognized particle type' )
#         sys.exit( 0 ) 
            
#     analyzer.load_indices( timestep, keys = [ gamma_key ].extend( coords_keys ) )        
#     gammas = analyzer.data[ gamma_key ][ timestep ] 

#     coords = [ analyzer.data[ key ][ timestep ] for key in coords_keys ] 
    
#     bins = [ np.arange( analyzer.params.mx0 ),
#              np.arange( analyzer.params.my0 ),
#              np.arange( analyzer.params.mz0 ) ]

#     # print( bins ) 
#     # print( coords )
#     # print( gammas ) 
    
#     gamma_counts, edges = np.histogramdd( coords, bins = bins )
#     gamma_sums, edges   = np.histogramdd( coords, bins = bins, weights = gammas )

#     gamma_counts[ gamma_counts == 0 ] = np.inf
    
#     return gamma_sums / gamma_counts 
    


    
# def compute_max_gammas( particle_type, timestep, min_gamma = 20 ) :

#     if particle_type == 'e' :
#         gamma_key ='gammae'
#         coords_keys = [ 'xe', 'ye', 'ze' ]

#     elif particle_type == 'i' :
#         gamma_key = 'gammai'
#         coords_keys = [ 'xi', 'yi', 'zi' ]

#     else :
#         print( 'ERROR: unrecognized particle type' )
#         sys.exit( 0 ) 


#     # do this many particles at a time 
#     batch_size = 1e7

#     with analyzer.open_data_file( timestep, 'prtl.tot' ) as f :

#         total_particles = len( f[ gamma_key ] )

#         for i in range( 0, total_particles, batch_size ) :

#             end = min( i + batch_size, total_particles )

#             gammas = f[ gamma_key ][ i : end ]
#             coords = np.vstack( [ analyzer.data[ key ][ timestep ] for key in coords_keys ] ).T
    
#     indices = ( gammas >= min_gamma )
#     gammas = gammas[ indices ]
#     coords = coords[ indices ]

#     analyzer.unload_indices( timestep )
#     gc.collect() 
    
#     shape = ( analyzer.params.mx0, analyzer.params.my0, analyzer.params.mz0 )

#     # print( shape ) 

#     max_gammas = np.zeros( shape )

#     # print( coords.shape )
    
#     print( len( gammas ) )
#     for i in range( len( gammas ) ) :
#         if not ( i % ( len( gammas ) // 10 ) ) :
#             print( i )
        
#         xyz = tuple( coords[i].astype( int ) ) 
#         max_gammas[ xyz ] = max( max_gammas[ xyz ], gammas[ i ] )
        
#     # gamma_counts = np.histogramdd( coords, [ bins = shape ) )
#     # gamma_sums   = np.histogramdd( coords, [ bins = shape ), weights = gammas )
    
#     return max_gammas
    


        

    

if using_scalar_key : 
    analyzer.load_indices( timestep, keys = ['time'] )
    print( 'time = %.3e w_pe^{-1}' % analyzer.data.time[ timestep ] )

    data = get_scalar_data( data_key, timestep ) 

    # cmap = colorcet.m_linear_worb_100_25_c53
    # cmap = colorcet.linear_worb_100_25_c53
    # cmap = colorcet.rainbow_bgyrm_35_85_c71
    # cmap = colorcet.linear_bmy_10_95_c78 
    
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

    
    mlab.colorbar( orientation = 'vertical' )

    mlab.outline() 
    mlab.axes() 
    mlab.orientation_axes() 
    mlab.axes( nb_labels = 4, line_width = 4 )
               
    mlab.show()
    
else :
    keys = [ data_key + s for s in 'xyz' ]
    analyzer.load_indices( timestep, keys = keys + [ 'time' ] )
    print( 'time = %.3e w_pe^{-1}' % analyzer.data.time[ timestep ] )

    data = [ analyzer.data[ key ][ timestep ] for key in keys ] 
    
    if plot_type == 'vcp' :
        mask_points = int( np.prod( data[0].shape ) / 20**3 )
        print( 'mask_points = %d' % mask_points )

        plotting.vector_cut_plane_wrap( data,
                                        mask_points = mask_points,
                                        scale_factor = 5 )

    if plot_type == 'flow' :

        plot  = mlab.flow( * data, seed_resolution = 1,
                           # seedtype = 'point',
                           seedtype = 'point',
                           integration_direction = 'both',
                           linetype = 'line' )

        
        plot.stream_tracer.maximum_number_of_steps = 40000 
        
        plot.stream_tracer.maximum_propagation = 4000

        
            
        
    mlab.colorbar( orientation = 'vertical' )

    mlab.outline() 
    mlab.axes() 
    mlab.orientation_axes() 
    mlab.axes( nb_labels = 4, line_width = 4 )
               
    mlab.show()
    
    print( 'ERROR: mode not recognized' ) 

    











# @mlab.animate(delay = 100)
# def updateAnimation():
#     t = 0.0
#     while True:
#         ball.mlab_source.set(x = np.cos(t), y = np.sin(t), z = 0)
#         t += 0.1
#         yield

# ball = mlab.points3d(np.array(1.), np.array(0.), np.array(0.))

# updateAnimation()
# mlab.show()




# figure = mlab.figure( size = ( 1000, 1000 ) )

# plot = analysis.vector_cut_plane_wrap( B )


# dens = analyzer.data.dens[ timestep ]
# plot = analysis.volume_slice_wrap( dens,
#                                    # plane_orientation = 'z_axes',
#                                    slice_index = dens.shape[0] / 2 )


# m = np.amax( dens ) 
# plot = analysis.volume_wrap( dens, vmin = m / 4, vmax = 3 * m / 4  )




# figure = mlab.figure( size = ( 1000, 1000 ) )

# plot_name = 'dens_contour' 
# plotdir = './plots/' + plot_name + '/'
# os.makedirs( plotdir, exist_ok = 1 ) 

# m = np.amax( dens ) 
# plot = analysis.contour3d_wrap( dens, contours = [ m/8, m/2, 7*m/8 ], opacity = 0.5  )
# mlab.view( azimuth = 90, elevation = 90, roll = 90 )

# # mlab.show() 

# @mlab.animate( delay=500, ui=0 )
# def anim() :
#     timestep = 0 
#     while timestep < len( analyzer ) :
#         if timestep > 0 :
#             analyzer.unload_indices( timestep - 1 )
#         analyzer.load_indices( timestep, keys = [ 'dens' ] )
#         plot.mlab_source.trait_set( scalars = analyzer.data.dens[ timestep ] )
#         timestep += 1
#         mlab.savefig( plotdir + '%03d.png' % timestep ) 
#         yield 


# a = anim()

# mlab.outline()
# mlab.colorbar( orientation = 'vertical' ) 
# mlab.show() 


# movie_name = './plots/' + plot_name + '.mp4'
# ffmpeg_combine( plotdir, movie_name ) 
