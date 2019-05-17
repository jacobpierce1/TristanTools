# First, and before importing any Enthought packages, set the ETS_TOOLKIT
# environment variable to qt4, to tell Traits that we will use Qt.
import os
os.environ['ETS_TOOLKIT'] = 'qt4'
os.environ['QT_API'] = 'pyqt5'


from .tristan_data_analyzer import TristanDataAnalyzer 
from .tristan_data_container import TristanDataContainer, TristanError
from .tristan_data_plotter import TristanDataPlotter # , ALL_1D_SPECTRA_KEYS
from .helper_functions import check_spatial_dim
from .helper_classes import RecursiveAttrDict, AttrDict
from .tristan_cut import TristanCut 

from .mayavi_wrapper import * 
# from .helper_classes import AttrDict, AttrDictSeries 
