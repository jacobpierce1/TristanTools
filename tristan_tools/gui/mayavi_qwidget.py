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
        self.tristan_data_plotter.plot_timestep( timestep )
        
    # the layout of the dialog screated
    view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                     height=0, width=0, show_label=False),
                resizable=True )

    tristan_data_plotter = None
    


    
class MayaviQWidget( QWidget ) : # QtGui.QWidget ):

    def __init__(self, tristan_data_analyzer, plot_type, keys ):
        super().__init__()

        self.analyzer = tristan_data_analyzer
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        self.title_label = QLabel( '' )
        self.title_label.setAlignment( Qt.AlignCenter ) 
        layout.addWidget( self.title_label ) 

        self.visualization = Visualization()

        # The edit_traits call will generate the widget to embed.
        self.ui = self.visualization.edit_traits( parent = None,
                                                  handler = DisableToolbarHandler(), # ,
                                                  kind='subpanel').control

        self.tristan_data_plotter = TristanDataPlotter(
            self.analyzer, plot_type = plot_type, keys = keys,
            mayavi_scene = self.visualization.scene.mayavi_scene ) 

        print( 'mayavi scene: ', self.visualization.scene.mayavi_scene ) 
        
        self.visualization.tristan_data_plotter = self.tristan_data_plotter

        # print( 'in MayaviQWidget. indices are loaded: '
        #        + str( self.visualization.tristan_data_plotter.analyzer.indices_with_data )  )
        self.ui.setParent( self )
        layout.addWidget( self.ui )
        
        self.plot_controller = PlotControlWidget( self.tristan_data_plotter )
        layout.addWidget( self.plot_controller )

        self.setLayout( layout ) 
        
        self.set_title() 
        
        


        
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

        
        # self.tristan_data_plotter.plotter.set_title( self.tristan_data_plotter.plot_type ) 



    def set_title( self, title = None ) :

        # default title 
        if title is None :

            keys_str = ''
            keys = self.tristan_data_plotter.keys 
            for i in range( len( keys ) ) :

                keys_str += str( keys[i] )

                if i < len( keys ) - 1 :
                    keys_str += ', '
                            
            plot_type = self.tristan_data_plotter.plot_type

            title = keys_str + ': ' + plot_type
            
        self.title_label.setText( title ) 
        



        
# hack to disable the mayavi toolbar
class DisableToolbarHandler( Handler ):

    def position(self, info):
        editor = info.ui.get_editors('scene')[0]
        editor._scene._tool_bar.setVisible(False)
     
