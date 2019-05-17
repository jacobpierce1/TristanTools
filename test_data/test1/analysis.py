import os
os.environ['ETS_TOOLKIT'] = 'qt4'
os.environ['QT_API'] = 'pyqt5'

from mayavi import mlab 
import numpy as np
import matplotlib.pyplot as plt
import colorcet
import matplotlib.animation as animation
from collections import Counter 
import sys 

import tristan_tools.analysis as analysis 

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)


# def make_movie() :



analyzer = analysis.TristanDataAnalyzer( './output' )

timestep = 10

analyzer.load_indices( timestep )
B = [ analyzer.data[ key ][ timestep ] for key in [ 'bx', 'by', 'bz' ] ]
dens = analyzer.data.dens[ timestep ]




# cmap = colorcet.fire
# cmap = colorcet.m_linear_bmy_10_95_c71
# cmap = colorcet.m_linear_worb_100_25_c53

def dens_data_getter( n, analyzer, slice_index ) :
    analyzer.unload_indices( n-1 )
    analyzer.load_indices( n, keys = [ 'dens' ] )
    return analyzer.data.dens[ n ][ slice_index, :, : ]


def make_mpl_image_movie( data_getter, timesteps,
                          figsize, title, xlabel, ylabel, 
                          slice_index, projected_axis,
                          cmap, interpolation,
                          show = 1, savepath = None, fps = 30 ) :

    fig, ax = plt.subplots( figsize = figsize )
    ax.set_title( title )

    data = data_getter( 0 ) 
    im = ax.imshow( data, cmap = cmap, interpolation = interpolation  )
        
    def update( n ):
        ax.set_title( 'dens: %d' % n )
        data = data_getter( n ) 
        im.set_data( data )
        return im

    # interval = 200
    
    ani = animation.FuncAnimation( fig, update, timesteps, interval = 30 )
    writer = animation.writers['ffmpeg'](fps = fps )

    if savepath is not None :
        ani.save( savepath, writer=writer, dpi=100 )

    if show : 
        plt.show()
    
    return ani

    
# analyzer.load_indices( 0, keys = [ 'dens' ] )
# slice_index = int( analyzer.data.dens[0].shape[0] / 2 )
# data_getter = lambda n : dens_data_getter( n, analyzer, slice_index )

# cmap = colorcet.m_linear_worb_100_25_c53
# interpolation = 'bilinear' 

# fps = 5

# ani = make_mpl_image_movie( data_getter, range( len( analyzer ) ),
#                             ( 4, 6 ), '', '$x$ (cells)', '$y$ (cells)',
#                             slice_index, 0, 
#                             cmap, interpolation,
#                             show = 1, savepath = 'plots/dens.mp4', fps = 30 )







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




# fig, ax = plt.subplots( figsize = ( 7, 7 ) ) 
# times = np.arange( 0, len(analyzer), len( analyzer ) // 5, dtype = int )
# plot_gamma_spectra( analyzer, ax, times ) 
# plt.show() 





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




figure = mlab.figure( size = ( 1000, 1000 ) )
# figure.scene.movie_maker.record = True

# plot = analysis.vector_cut_plane_wrap( B )


# dens = analyzer.data.dens[ timestep ]
# plot = analysis.volume_slice_wrap( dens,
#                                    # plane_orientation = 'z_axes',
#                                    slice_index = dens.shape[0] / 2 )


# m = np.amax( dens ) 
# plot = analysis.volume_wrap( dens, vmin = m / 4, vmax = 3 * m / 4  )


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


def save( plotdir, movie_name ):
    os.system( 'ffmpeg -r 4 -i %s%%03d.png -vcodec mpeg4 -y %s' % ( plotdir, movie_name ) )


a = anim()

mlab.outline()
mlab.colorbar( orientation = 'vertical' ) 
mlab.show() 


movie_name = './plots/' + plot_name + '.mp4'
save( plotdir, movie_name ) 
