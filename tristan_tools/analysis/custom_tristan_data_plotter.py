import matplotlib.pyplot as plt
import numpy as np 
import os
import sys




def make_plot_output_directory( path ) :
    output_path = path + '/plots'
    os.makerdirs( output_path, exist_ok = 1 )
    return output_path 



def plot_all( tristan_data_analyzer ) :
    ...

    
# plot total particle and field energies vs. time.
def plot_energies( tristan_data_analyzer ) :
    ... 



# plot the energy of individual particles vs time. 
def plot_particle_energization( tristan_data_analyzer ) :
    ... 



def plot_momentum_spectra( tristan_data_analyzer, times ) :
    ...     



    
