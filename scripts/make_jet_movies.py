import os
os.environ['ETS_TOOLKIT'] = 'qt4'
# os.environ['QT_API'] = 'pyqt5'
os.environ['QT_API'] = 'pyqt'

from mayavi import mlab 
import numpy as np
import matplotlib.pyplot as plt
matplotlib.use('TkAgg') # <-- THIS MAKES IT FAST!

import colorcet
import matplotlib.animation as animation
from collections import Counter 
import sys 

import tristan_tools.analysis as analysis 

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

from mpl_toolkits.axes_grid1 import make_axes_locatable

import gc 




def ffmpeg_combine( plotdir, movie_name ):
    os.system( 'ffmpeg -r 4 -i %s%%03d.png -vcodec mpeg4 -y %s' % ( plotdir, movie_name ) )




analyzer = analysis.TristanDataAnalyzer( './output' )

timestep = 10

analyzer.load_indices( timestep )
B = [ analyzer.data[ key ][ timestep ] for key in [ 'bx', 'by', 'bz' ] ]
dens = analyzer.data.dens[ timestep ]




# cmap = colorcet.fire
# cmap = colorcet.m_linear_bmy_10_95_c71
# cmap = colorcet.m_linear_worb_100_25_c53

# def dens_data_getter( n, analyzer, slice_index ) :
#     analyzer.unload_indices( n-1 )
#     analyzer.load_indices( n, keys = [ 'dens' ] )
#     return analyzer.data.dens[ n ][ slice_index, :, : ]


# def make_mpl_image_movie( data_getter, timesteps,
#                           figsize, title, xlabel, ylabel, 
#                           slice_index, projected_axis,
#                           cmap, interpolation,
#                           show = 1, savepath = None, fps = 30 ) :

#     fig, ax = plt.subplots( figsize = figsize )
#     ax.set_title( title )

#     data = data_getter( 0 ) 
#     im = ax.imshow( data, cmap = cmap, interpolation = interpolation  )
        
#     def update( n ):
#         ax.set_title( 'dens: %d' % n )
#         data = data_getter( n ) 
#         im.set_data( data )
#         return im

#     # interval = 200
    
#     ani = animation.FuncAnimation( fig, update, timesteps, interval = 30 )
#     writer = animation.writers['ffmpeg'](fps = fps )

#     if savepath is not None :
#         ani.save( savepath, writer=writer, dpi=100 )

#     if show : 
#         plt.show()
    
#     return ani





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

cmap = colorcet.m_linear_worb_100_25_c53
interpolation = 'bilinear' 

fps = 5

ani = make_jet_movie_new( analyzer, range( len( analyzer ) ),
                          # ( 9, 6 ), '', '$x$ (cells)', '$y$ (cells)',
                          # slice_index, 0, 
                          cmap, interpolation,
                          show = 1, savedir = './plots/projections/', fps = 30 )







def compute_energies( analyzer ) :

    E = np.zeros( ( 3, len( tristan_data_analyzer ) ) )
    B = np.zeros( ( 3, len( tristan_data_analyzer ) ) )

    particles = np.zeros( len( tristan_data_analyzer ) )

    for i in range( len( analyzer ) ) :
        analyzer.load_indices( [i], keys = [ 'ex', 'ey', 'ez',
                                             'bx', 'by', 'bz',
                                             'ue', 've', 'we',
                                             'ui', 'vi', 'wi' ] )





def plot_particle_energization( analyzer, ax, inde_tags = None, 
                                savepath = None ) :
    
    keys = [ 'inde', # 'indi', 
             'gammae' ] # , 'ue', 've', 'we' ] 
             # 'ui', 'vi', 'wi' ] )
    
    # get the initial indices 
    last_idx = len( analyzer ) - 1
    analyzer.load_indices( [ last_idx ], keys = keys  )

    
    if inde_tags is None :
        inde_tags = np.copy( analyzer.data.inde[ last_idx ] )  # len = initial num particles 

    gammas = np.zeros( ( len( inde_tags ), len( analyzer ) ) )
    gammas[:] = np.nan 

    # https://stackoverflow.com/questions/32191029/getting-the-indices-of-several-elements-in-a-numpy-array-at-once
    # sorter = np.argsort( inde_tags )
    
    for i in range( len( analyzer ) ) : 
        
        analyzer.load_indices( [i], keys = keys )

        # these are the indices that map the particle inde number to the array indices in the timestep=0 array.
        sorter = np.argsort( analyzer.data.inde[i] )
        indices = sorter[ np.searchsorted( analyzer.data.inde[i],
                                           inde_tags,
                                           sorter = sorter ) ]
        
        # print( indices )
        # print( analyzer.data.inde[i][ indices ] )
        # print( inde_tags )
        # print( np.all( analyzer.data.inde[i][ indices ] == inde_tags ) ) 
        
        gammas[ :, i ] = analyzer.data.gammae[i][ indices ] 
        
        analyzer.unload_indices( [i] )


    # append to the plot 
    x = np.arange( len( analyzer ) )
    for i in range( len( inde_tags ) ) :
        ax.plot( x, gammas[i], color = 'k', linewidth = 0.01  )
    
        
        

# fig, ax = plt.subplots( figsize = ( 7, 7 ) ) 
# plot_particle_energization( analyzer, ax ) 
# plt.show() 





def plot_gamma_spectra( analyzer, ax, times ) :
    print( times ) 
    for time in times :
        analyzer.load_indices( time, keys = [ 'gammae', 'time' ]  )

        hist, bins = np.histogram( analyzer.data.gammae[ time ], bins = 'fd', density = 1 ) 

        simtime = analyzer.data.time[ time ][0]
        ax.plot( bins[:-1], hist, ls = 'steps-mid', label = '%3f' % simtime  )

        analyzer.unload_indices( time ) 
        
    ax.legend( loc = 'best', title = 'time' ) 
    # ax.legend( bbox_to_anchor=(1.2, 1), loc='upper right')




fig, ax = plt.subplots( figsize = ( 7, 7 ) ) 
times = np.arange( 0, len(analyzer), len( analyzer ) // 5, dtype = int )
plot_gamma_spectra( analyzer, ax, times )
plt.savefig( './plots/gamma_spectra.png', dpi = 400 )
plt.show() 





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




figure = mlab.figure( size = ( 1000, 1000 ) )

plot_name = 'dens_contour' 
plotdir = './plots/' + plot_name + '/'
os.makedirs( plotdir, exist_ok = 1 ) 

m = np.amax( dens ) 
plot = analysis.contour3d_wrap( dens, contours = [ m/8, m/2, 7*m/8 ], opacity = 0.5  )
mlab.view( azimuth = 90, elevation = 90, roll = 90 )

# mlab.show() 

@mlab.animate( delay=500, ui=0 )
def anim() :
    timestep = 0 
    while timestep < len( analyzer ) :
        if timestep > 0 :
            analyzer.unload_indices( timestep - 1 )
        analyzer.load_indices( timestep, keys = [ 'dens' ] )
        plot.mlab_source.trait_set( scalars = analyzer.data.dens[ timestep ] )
        timestep += 1
        mlab.savefig( plotdir + '%03d.png' % timestep ) 
        yield 


a = anim()

mlab.outline()
mlab.colorbar( orientation = 'vertical' ) 
mlab.show() 


movie_name = './plots/' + plot_name + '.mp4'
ffmpeg_combine( plotdir, movie_name ) 
