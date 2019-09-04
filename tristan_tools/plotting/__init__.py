import os
os.environ['ETS_TOOLKIT'] = 'qt4'
os.environ['QT_API'] = 'pyqt5'


from .mayavi_wrapper import *
from .tristan_data_plotter import TristanDataPlotter # , ALL_1D_SPECTRA_KEYS
