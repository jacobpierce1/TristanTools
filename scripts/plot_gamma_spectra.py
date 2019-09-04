import os
import sys 
# os.environ['ETS_TOOLKIT'] = 'qt4'
# os.environ['QT_API'] = 'pyqt5'
# os.environ['QT_API'] = 'pyqt'

# from mayavi import mlab 
import numpy as np

import matplotlib


downsample = 1
if len( sys.argv ) > 1 :
    downsample = int( sys.argv[1] )

show = 1
if len( sys.argv ) > 2 :
    show = int( sys.argv[2] )

load = 1
if len( sys.argv ) > 3 :
    load = int( sys.argv[3] )

    
analyzer_path = './'
if len( sys.argv ) > 4 :
    analyzer_path = sys.argv[4] + '/'


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


analyzer = analysis.TristanDataAnalyzer( analyzer_path + 'output' )

os.makedirs( analyzer_path + 'plots/', exist_ok = 1 ) 


        
def plot_gamma_spectra2( analyzer, axarr, timesteps ) :
    print( timesteps ) 

    max_gammas = np.zeros( ( 2, len( timesteps ) ) )
    mean_gammas = np.zeros( ( 2, len( timesteps ) ) )
    times = np.zeros( len( timesteps ) ) 

    
    for j in range( len( timesteps ) ) :

        timestep = timesteps[j]
        print( timestep )
        
        keys = [ 'gammae_spec', 'gammai_spec' ]

        analyzer.compute_gamma_spectrum( timestep, 'e', load = load )
        analyzer.compute_gamma_spectrum( timestep, 'i', load = load )
        analyzer.load_indices( timestep, keys = [ 'time' ]  )

        simtime = analyzer.data.time[ timestep ] 
        times[j] = simtime
        

        
        for i in range( 2 ) :

            hist, bins = analyzer.data[ keys[i] ][ timestep ] 

            # power_index = np.gradient( np.log( hist ), np.log( bins ) )
            
            grad = np.gradient( hist, bins )
            
            power_index = np.clip( ( bins / hist ) * grad, -10, 10 )
            # power_index = np.log( hist ) / np.log( bins ) 
            
            axarr[i,0].loglog( bins,
                               hist,
                               # ls = 'steps-mid',
                               label = '%3f' % simtime  )

            axarr[i,1].semilogx( bins, power_index,
                                 label = '%3f' % simtime  )
            
            analyzer.unload_indices( timestep, keys = keys )
            gc.collect() 

            mean_gammas[i,j]  = np.average( bins, weights = hist )
            max_gammas[i,j] = np.amax( bins ) 

            
    for i in range(2) :
        axarr[i,2].plot( times, mean_gammas[i], label = r'mean', marker = 'o' )
        axarr[i,2].plot( times, max_gammas[i], label = r'max', marker = 'o' )
        
    for i in range(2) : 
        axarr[i,0].legend( loc = 'best', title = r'Time $[\omega_\mathrm{pe}^{-1}]$' )
        axarr[i,1].legend( loc = 'best', title = r'Time $[\omega_\mathrm{pe}^{-1}]$' )
        axarr[i,2].legend( loc = 'best' )

    # ax.legend( bbox_to_anchor=(1.2, 1), loc='upper right')




fig, axarr = plt.subplots( 2, 3, figsize = ( 14, 10 ) ) 
fig.subplots_adjust( wspace = 0.5, hspace = 0.5 )

axarr[0,0].set_title( 'Electron energy spectra', fontsize = 14 )
axarr[1,0].set_title( 'Proton + Positron energy spectra', fontsize = 14 )

axarr[0,1].set_title( 'Electron power law index' )
axarr[1,1].set_title( 'Proton + positron power law index' )

axarr[0,2].set_title( 'Electron Energization' )
axarr[1,2].set_title( 'Proton + Positron Energization' )

for i in range(2) : 
    axarr[i,0].set_ylabel( r'$f( \beta \gamma )$', fontsize = 12 )
    axarr[i,0].set_xlabel( r'$ \beta \gamma $', fontsize = 12 )

    # axarr[i,1].set_ylabel( r'$ d \log[ f(\beta\gamma) ]/ d \log [ \beta\gamma ]  $',
    # fontsize = 12 )
    axarr[i,1].set_ylabel( r'$ \log[ f(\beta\gamma) ]/ \log [ \beta\gamma ]  $',
                           fontsize  = 12 )

    axarr[i,1].set_xlabel( r'$ \beta \gamma $', fontsize = 12 )
    
    axarr[i,2].set_ylabel( r'$\beta \gamma $' )
    axarr[i,2].set_xlabel( r'Time $(\omega_\mathrm{pe}^{-1}) $' )



    
times = np.arange( 0, len(analyzer), downsample, dtype = int )    


plot_gamma_spectra2( analyzer, axarr, times )
plt.savefig( analyzer_path + 'plots/gamma_spectra.png', dpi = 400 )

if show: 
    plt.show() 
