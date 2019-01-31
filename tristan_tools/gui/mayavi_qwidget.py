# First, and before importing any Enthought packages, set the ETS_TOOLKIT
# environment variable to qt4, to tell Traits that we will use Qt.
import os
os.environ['ETS_TOOLKIT'] = 'qt4'
os.environ['QT_API'] = 'pyqt5'


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

from PyQt5.QtWidgets import *
from PyQt5 import QtCore

from plot_control_widget import PlotControlWidget 


from tristan_tools.analysis import TristanDataPlotter 


class Visualization( HasTraits ) :

    scene = Instance(MlabSceneModel, ())

    # @on_trait_change('scene.activated')
    def update_plot( self, timestep ) :
        # This function is called when the view is opened. We don't
        # populate the scene when the view is not yet open, as some
        # VTK features require a GLContext.

        # We can do normal mlab calls on the embedded scene.
        # self.scene.mlab.test_points3d()
        self.plotter.plot_timestep( timestep )
        
    # the layout of the dialog screated
    view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                     height=250, width=250, show_label=False),
                resizable=True # We need this to resize with the parent widget
                )

    plotter = None
    


    
class MayaviQWidget( QtGui.QWidget ):

    def __init__(self, tristan_data_analyzer, plot_type, keys ):
        super().__init__()

        self.analyzer = tristan_data_analyzer
        
        layout = QtGui.QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        self.visualization = Visualization()
        self.plotter = TristanDataPlotter( self.analyzer, plot_type = plot_type,
                                           keys = keys,
                                mayavi_scene = self.visualization.scene.mayavi_scene ) 

        self.visualization.plotter = self.plotter

        print( 'in MayaviQWidget. indices are loaded: '
               + str( self.visualization.plotter.analyzer.indices_with_data )  )

        # The edit_traits call will generate the widget to embed.
        self.ui = self.visualization.edit_traits(parent=self,
                                                 kind='subpanel').control
        self.ui.setParent(self)
        layout.addWidget(self.ui)
        
        self.plot_controller = PlotControlWidget( self.analyzer )
        layout.addWidget( self.plot_controller ) 

        
    # def mouseReleaseEvent(self, QMouseEvent):
    #     if QMouseEvent.button() == QtCore.Qt.LeftButton:
    #         print("Left Button Clicked")
    #     elif QMouseEvent.button() == QtCore.Qt.RightButton:
    #         #do what you want here
    #         print("Right Button Clicked")

            
    # if the timestep is supplied, then set the timestep and update plot to the
    # new timestep. otherwise, grab the timestep from the plot controller and
    # update the plot to that timestep.
    def update( self, timestep = None ) :

        if timestep is None :
            timestep = self.plot_controller.time_slider_widget.timestep  

        else :
            self.plot_controller.time_slider_widget.update( timestep ) 

        self.visualization.update_plot( timestep ) 
            
