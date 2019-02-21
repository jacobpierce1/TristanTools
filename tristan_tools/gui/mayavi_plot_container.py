# First, and before importing any Enthought packages, set the ETS_TOOLKIT
# environment variable to qt4, to tell Traits that we will use Qt.
# import os
# os.environ['ETS_TOOLKIT'] = 'qt4'
# os.environ['QT_API'] = 'pyqt5'


# from pyface.qt import QtGui, QtCore

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt



# Alternatively, you can bypass this line, but you need to make sure that
# the following lines are executed before the import of PyQT:
#   import sip
#   sip.setapi('QString', 2)


from traits.api import HasTraits, Instance, on_trait_change
from traitsui.api import View, Item, Handler

from mayavi.core.ui.api import MayaviScene, MlabSceneModel, \
    SceneEditor

# from PyQt5.QtWidgets import *
# from PyQt5 import QtCore


from plot_control_widget import PlotControlWidget 







class Visualization( HasTraits ) :

    scene = Instance(MlabSceneModel, ())

    # @on_trait_change('scene.activated')
    def update_plot( self, timestep ) :
        # This function is called when the view is opened. We don't
        # populate the scene when the view is not yet open, as some
        # VTK features require a GLContext.

        # We can do normal mlab calls on the embedded scene.
        # self.scene.mlab.test_points3d()
        self.tristan_data_plotter.plot_timestep( timestep )
        
    # the layout of the dialog screated
    view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                     height=0, width=0, show_label=False),
                resizable=True )

    tristan_data_plotter = None
    


    
class MayaviPlotContainer( QWidget ) : # QtGui.QWidget ):

    def __init__(self, tristan_data_plotter ):
        super().__init__()

        self.tristan_data_plotter = tristan_data_plotter
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        self.visualization = Visualization()

        # The edit_traits call will generate the widget to embed.
        self.ui = self.visualization.edit_traits( parent = self,
                                                  handler = DisableToolbarHandler(), # ,
                                                  kind='subpanel').control

        # very important: gives access to the scene for plotting via mlab. 
        self.tristan_data_plotter.plotter.set_mayavi_scene( self.visualization.scene.mayavi_scene ) 

        print( 'mayavi scene: ', self.visualization.scene.mayavi_scene )

        self.mayavi_scene = self.visualization.scene.mayavi_scene
        
        self.visualization.tristan_data_plotter = self.tristan_data_plotter

        # print( 'in MayaviQWidget. indices are loaded: '
        #        + str( self.visualization.tristan_data_plotter.analyzer.indices_with_data )  )
        # self.ui.setParent( self )
        layout.addWidget( self.ui )
        
        self.setLayout( layout ) 
        
        
        

    # if the timestep is supplied, then set the timestep and update plot to the
    # new timestep. otherwise, grab the timestep from the plot controller and
    # update the plot to that timestep.
    def update( self, timestep ) :
        self.visualization.update_plot( timestep ) 

        
        # self.tristan_data_plotter.plotter.set_title( self.tristan_data_plotter.plot_type ) 

    def get_canvas( self ) :
        return self.mayavi_scene



    
    def delete( self ) :
        pass 


    def clear( self ) :
        self.tristan_data_plotter.clear() 

        
    def reset( self ) :
        self.tristan_data_plotter.reset() 



        
# hack to disable the mayavi toolbar
class DisableToolbarHandler( Handler ):

    def position(self, info):
        editor = info.ui.get_editors('scene')[0]
        editor._scene._tool_bar.setVisible(False)
     


