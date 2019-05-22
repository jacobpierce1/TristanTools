import os
os.environ['ETS_TOOLKIT'] = 'qt4'
# os.environ['QT_API'] = 'pyqt5'
os.environ['QT_API'] = 'pyqt'

from mayavi import mlab 
import numpy as np

import colorcet
import matplotlib.animation as animation
from collections import Counter 
import sys 

import tristan_tools.analysis as analysis 

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

from mpl_toolkits.axes_grid1 import make_axes_locatable

import gc 




import os
os.environ['ETS_TOOLKIT'] = 'qt4'
os.environ['QT_API'] = 'pyqt5'
# os.environ['QT_API'] = 'pyqt'

import numpy as np

from traits.api import HasTraits, Instance, Button, \
    on_trait_change
from traitsui.api import View, Item, HSplit, Group, HGroup

from mayavi import mlab
from mayavi.core.ui.api import MlabSceneModel, SceneEditor




class MyDialog(HasTraits):

    scene1 = Instance(MlabSceneModel, ())
    scene2 = Instance(MlabSceneModel, ())
    scene3 = Instance(MlabSceneModel, ())

    button1 = Button('Redraw')
    button2 = Button('Redraw')

    @on_trait_change('button1')
    def redraw_scene1(self):
        self.redraw_scene(self.scene1)

    @on_trait_change('button2')
    def redraw_scene2(self):
        self.redraw_scene(self.scene2)

    def redraw_scene(self, scene):
        # Notice how each mlab call points explicitely to the figure it
        # applies to.
        # mlab.clf(figure=scene.mayavi_scene)
        x, y, z, s = np.random.random((4, 100))
        mlab.points3d(x, y, z, s, figure=scene.mayavi_scene)

        
    # The layout of the dialog created
    view = View( # HSplit(
        HGroup(
            Group(
                Item('scene1',
                     editor=SceneEditor(), height=250,
                     width=300),
                Item('scene3',
                     editor=SceneEditor(), height=250,
                     width=300),
                'button1',
                show_labels=False,
            ),
            Group(
                Item('scene2',
                     editor=SceneEditor(), height=250,
                     width=300, show_label=False),
                'button2',
                show_labels=False,
            ),
        ),
        resizable=True,
    )

    

m = MyDialog()

m.configure_traits()


dir( m.scene1 ) 































def ffmpeg_combine( plotdir, movie_name ):
    os.system( 'ffmpeg -r 4 -i %s%%03d.png -vcodec mpeg4 -y %s' % ( plotdir, movie_name ) )




analyzer = analysis.TristanDataAnalyzer( './output' )



def jet_movie_data_getter( n, analyzer ) :
    analyzer.unload_indices( n-1 )
    analyzer.load_indices( n, keys = [ 'dens', 'densi',
                                       'bx', 'by', 'bz',
                                       'jx', 'jy', 'jz',
                                       'ex', 'ey', 'ez',
                                       'time' ] )
    analyzer.compute_indices( n, keys = [ 'dense' ] ) 
    # return analyzer.data.dens[ n ][ slice_index, :, : ]



    
def make_jet_movie( analyzer, timesteps,
                    # figsize, title, xlabel, ylabel, 
                    # xslice_index, zslice_index,
                    # hspace, wspace,
                    cmap, interpolation,
                    downsample = 10, scale = 2,
                    show = 1, savepath = None, fps = 30 ) :
    
    fig, axarr = plt.subplots( 2, 3, figsize = (12,8) )
    fig.subplots_adjust( hspace = 0.5, wspace = 0.5 )
    
    axarr[0][0].set_title( 'dens,  $(b_y, b_z)$' )
    axarr[0][1].set_title( 'dense, $(j_y, j_z)$' )
    axarr[0][2].set_title( 'densi, $(e_y, e_z)$' )
    axarr[1][0].set_title( 'dens,  $(b_x, b_y)$' )
    axarr[1][1].set_title( 'dense, $(j_x, j_y)$' )
    axarr[1][2].set_title( 'densi, $(e_x, e_y)$' )
    
    jet_movie_data_getter( 0, analyzer )
    xslice_index = int( analyzer.data.dens[0].shape[0] / 2 )
    zslice_index = int( analyzer.data.dens[0].shape[2] / 2 )
    
    images =  np.zeros( (2, 3), dtype = object )
    quivers = np.zeros( (2, 3), dtype = object )
    quiver_keys = np.zeros( (2,3), dtype = object ) 
    
    dens_slices = [ ( xslice_index, slice( None ), slice( None ) ),
                    ( slice( None ), slice( None ), zslice_index ) ]
    
    dens_data_names = [ 'dens', 'dense', 'densi' ]

    quiver_data_names = [
        [ [ 'bz', 'by' ], [ 'jz', 'jy' ], [ 'ez', 'ey' ] ],
        [ [ 'by', 'bx' ], [ 'jy', 'jx' ], [ 'ey', 'ex' ] ]
    ]

    for i in range(2) :
        for j in range(3) :

            data = analyzer.data[ dens_data_names[j] ][0][ dens_slices[i] ] 
            images[i,j]  = axarr[i,j].imshow( data, cmap = cmap, interpolation = interpolation )

            divider = make_axes_locatable( axarr[i,j] ) 
            cax = divider.append_axes("right", size="5%", pad=0.05)
            cbar = fig.colorbar( images[i,j], cax = cax )
            
            data = [ analyzer.data[ key ][0][ dens_slices[i] ]
                     for key in quiver_data_names[i][j] ] 

            # downsample to 10 points in each direction
            strides = [ int( data[0].shape[i] / downsample ) for i in range(2) ]
            
            # xx, yy = np.meshgrid( np.arange( 0, len( data[0][0] ), strides[0] ),
            #                       np.arange( 0, len( data[0][1] ), strides[1] ) )

            x = np.arange( 0, data[0].shape[0], strides[0] )
            y = np.arange( 0, data[0].shape[1], strides[1] )

            # print( 'INIT: printing' ) 
            # print( x.shape )
            # print( y.shape )
            # print( data[0].shape )
            # print( data[1].shape )
            # print( data[0][::strides[0], ::strides[1] ].shape )
            # print( data[1][::strides[0], ::strides[1] ].shape )

            
            m = np.sqrt( np.amax( data[0] ** 2 + data[1] ** 2 ) )

            quivers[i,j] = axarr[i,j].quiver( x, y,
                                              data[0][::strides[0], ::strides[1] ],
                                              data[1][::strides[0], ::strides[1] ],
                                              angles = 'xy',
                                              scale_units = 'x',
                                              scale = m / scale,
                                              pivot = 'mid',
                                              headwidth = 5,
                                              headaxislength = 5,
                                              linewidth = 0.001 )
            # linestyle = '' )
            
            quiver_keys[i,j] = axarr[i,j].quiverkey( quivers[i,j], 0.9, 0.9, m , '%.2e' % m,
                                                     labelpos = 'E', coordinates = 'axes' )

            # print( quivers[i,j] ) 
            
            # print( type( quivers[0,0] ) )
            # sys.exit( 0 ) 

        
    data_getter = lambda n : jet_movie_data_getter( n, analyzer ) 
    
    def update( n ):
        print( n ) 
        data_getter( n )
        fig.suptitle( 'Time = %.3f' % analyzer.data.time[ n ] )

        for i in range(2) :
            for j in range(3) :
                data = analyzer.data[ dens_data_names[j] ][n][ dens_slices[i] ]
                images[i,j].set_data( data )
                
                data = [ analyzer.data[ key ][n][ dens_slices[i] ]
                         for key in quiver_data_names[i][j] ]
                
                # quivers[i,j].remove()
                quiver_keys[i,j].remove()
                
                # downsample to 10 points in each direction
                strides = [ int( data[0].shape[i] ) / downsample for i in range(2) ]
                
                # xx, yy = np.meshgrid( np.arange( 0, len( data[0][0] ), strides[0] ),
                #                       np.arange( 0, len( data[0][1] ), strides[1] ) )

                # print( xx.shape )
                # print( yy.shape )
                # print( 'printing' ) 
                # print( quivers[i,j].U.shape )
                # print( quivers[i,j].V.shape )
                # print( quivers[i,j].X.shape )
                # print( quivers[i,j].Y.shape )
                # print( quivers[i,j].XY.shape )
                # print( data[0][::strides[0], ::strides[1] ].shape )
                # print( data[1][::strides[0], ::strides[1] ].shape )
                        

                
                m = np.sqrt( np.amax( data[0] ** 2 + data[1] ** 2 ) )
                
                # quivers[i,j] = axarr[i,j].quiver( xx, yy,
                #                                   data[0][::strides[0],::strides[1] ],
                #                                   data[1][::strides[0], ::strides[1] ],
                #                                   scale_units = 'x',
                #                                   scale = 5 * m )

                # quivers[i,j] = axarr[i,j].quiver( xx, yy, * data  )

                quivers[i,j].scale = m / scale

                quivers[i,j].set_UVC( data[0][::strides[0], ::strides[1] ],
                                      data[1][::strides[0], ::strides[1] ] )
                
                quiver_keys[i,j] = axarr[i,j].quiverkey( quivers[i,j], 0.9, 0.9, m , '%.2e' % m,
                                                         labelpos = 'E', coordinates = 'axes' )

                
                
    ani = animation.FuncAnimation( fig, update, timesteps, interval = 30, blit = 0 )
    writer = animation.writers['ffmpeg'](fps = fps )

    if savepath is not None :
        ani.save( savepath, writer=writer, dpi=400 )

    if show : 
        plt.show()
        
    return ani




# analyzer.load_indices( 0, keys = [ 'dens' ] )

def make_jet_movie_new( analyzer, timesteps,
                        # figsize, title, xlabel, ylabel, 
                        # xslice_index, zslice_index,
                        # hspace, wspace,
                        cmap, interpolation,
                        downsample = 10, scale = 2,
                        show = 1, savedir = None, fps = 30 ) :

    os.makedirs( savedir, exist_ok = 1 )
    
    fig, axarr = plt.subplots( 2, 3, figsize = (12,8) )
    fig.subplots_adjust( hspace = 0.5, wspace = 0.5 )
    
    axarr[0][0].set_title( 'dens,  $(b_y, b_z)$' )
    axarr[0][1].set_title( 'dense, $(j_y, j_z)$' )
    axarr[0][2].set_title( 'densi, $(e_y, e_z)$' )
    axarr[1][0].set_title( 'dens,  $(b_x, b_y)$' )
    axarr[1][1].set_title( 'dense, $(j_x, j_y)$' )
    axarr[1][2].set_title( 'densi, $(e_x, e_y)$' )
    
    jet_movie_data_getter( 0, analyzer )
    xslice_index = int( analyzer.data.dens[0].shape[0] / 2 )
    zslice_index = int( analyzer.data.dens[0].shape[2] / 2 )
    
    images =  np.zeros( (2, 3), dtype = object )
    quivers = np.zeros( (2, 3), dtype = object )
    quiver_keys = np.zeros( (2,3), dtype = object ) 
    
    dens_slices = [ ( xslice_index, slice( None ), slice( None ) ),
                    ( slice( None ), slice( None ), zslice_index ) ]
    
    dens_data_names = [ 'dens', 'dense', 'densi' ]

    quiver_data_names = [
        [ [ 'bz', 'by' ], [ 'jz', 'jy' ], [ 'ez', 'ey' ] ],
        [ [ 'by', 'bx' ], [ 'jy', 'jx' ], [ 'ey', 'ex' ] ]
    ]

    for i in range(2) :
        for j in range(3) :

            data = analyzer.data[ dens_data_names[j] ][0][ dens_slices[i] ] 
            images[i,j]  = axarr[i,j].imshow( data, cmap = cmap, interpolation = interpolation )

            divider = make_axes_locatable( axarr[i,j] ) 
            cax = divider.append_axes("right", size="5%", pad=0.05)
            cbar = fig.colorbar( images[i,j], cax = cax )
            
            data = [ analyzer.data[ key ][0][ dens_slices[i] ]
                     for key in quiver_data_names[i][j] ] 

            # downsample to 10 points in each direction
            strides = [ int( data[0].shape[i] / downsample ) for i in range(2) ]

            x = np.arange( 0, data[0].shape[0], strides[0] )
            y = np.arange( 0, data[0].shape[1], strides[1] )
            
            m = np.sqrt( np.amax( data[0] ** 2 + data[1] ** 2 ) )

            quivers[i,j] = axarr[i,j].quiver( x, y,
                                              data[0][::strides[0], ::strides[1] ],
                                              data[1][::strides[0], ::strides[1] ],
                                              angles = 'xy',
                                              scale_units = 'x',
                                              scale = m / scale,
                                              pivot = 'mid',
                                              headwidth = 5,
                                              headaxislength = 5,
                                              linewidth = 0.001 )
            # linestyle = '' )
            
            quiver_keys[i,j] = axarr[i,j].quiverkey( quivers[i,j], 0.9, 0.9, m , '%.2e' % m,
                                                     labelpos = 'E', coordinates = 'axes' )
            
            
            # print( quivers[i,j] ) 
            
            # print( type( quivers[0,0] ) )
            # sys.exit( 0 ) 

        
    data_getter = lambda n : jet_movie_data_getter( n, analyzer ) 

    for n in timesteps :
        
        print( n ) 
        data_getter( n )
        fig.suptitle( 'Time = %.3f' % analyzer.data.time[ n ] )

        for i in range(2) :
            for j in range(3) :
                data = analyzer.data[ dens_data_names[j] ][n][ dens_slices[i] ]
                images[i,j].set_data( data )
                
                data = [ analyzer.data[ key ][n][ dens_slices[i] ]
                         for key in quiver_data_names[i][j] ]

                gc.collect()
                
                # quivers[i,j].remove()
                quiver_keys[i,j].remove()
                
                # downsample to 10 points in each direction
                strides = [ int( data[0].shape[i] / downsample ) for i in range(2) ]

                print( strides ) 

                m = np.sqrt( np.amax( data[0] ** 2 + data[1] ** 2 ) )
                
                quivers[i,j].scale = m / scale

                quivers[i,j].set_UVC( data[0][::strides[0], ::strides[1] ],
                                      data[1][::strides[0], ::strides[1] ] )
                
                quiver_keys[i,j] = axarr[i,j].quiverkey( quivers[i,j], 0.9, 0.9, m , '%.2e' % m,
                                                         labelpos = 'E', coordinates = 'axes' )

        plt.savefig( savedir + '%03d.png' % n, dpi = 400 ) 

                
    ffmpeg_combine( savedir, './plots/jet_projections.mp4' )
    



# analyzer.load_indices( 0, keys = [ 'dens' ] )
# slice_index = int( analyzer.data.dens[0].shape[0] / 2 )
# data_getter = lambda n : dens_data_getter( n, analyzer, slice_index )

# cmap = colorcet.m_linear_worb_100_25_c53
# interpolation = 'bilinear' 

# fps = 5

# ani = make_jet_movie_new( analyzer, range( len( analyzer ) ),
#                           # ( 9, 6 ), '', '$x$ (cells)', '$y$ (cells)',
#                           # slice_index, 0, 
#                           cmap, interpolation,
#                           show = 1, savedir = './plots/projections/', fps = 30 )











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
