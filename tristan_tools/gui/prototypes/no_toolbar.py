import os
os.environ['ETS_TOOLKIT'] = 'qt4'
os.environ['QT_API'] = 'pyqt5' 

from traits.api import HasTraits, Instance, on_trait_change
from traitsui.api import View, Item
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, SceneEditor
from PyQt5.QtWidgets import *
# from main import Ui_MainWindow
import sys
from traitsui.api import Handler


class Visualization(HasTraits):
    scene = Instance(MlabSceneModel, ())

    @on_trait_change('scene.activated')
    def update_plot(self):
        self.scene.mlab.test_points3d()

    view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                 height=0, width=0, show_label=False),
            resizable=True  # We need this to resize with the parent widget
            )


class DisableToolbarHandler(Handler):
    def position(self, info):
        editor = info.ui.get_editors('scene')[0]
        editor._scene._tool_bar.setVisible(False)


class MayaviQWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.visualization = Visualization()
        self.ui = self.visualization.edit_traits(handler=DisableToolbarHandler(), kind='subpanel').control
        layout.addWidget(self.ui)
        self.ui.setParent(self)


class Action(QWidget):
    def __init__(self, parent=None):
        super(Action, self).__init__(parent)
        # self.setupUi(self)
        # self.splitter.setSizes([100, 300])
        # self.splitter_2.setSizes([400, 100])

        # container = QWidget()
        # mayavi_widget = MayaviQWidget()

        layout = QHBoxLayout()
        # layout.addWidget(mayavi_widget)

        for i in range(2) :
            layout.addWidget( MayaviQWidget() ) 
        
        self.setLayout( layout )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    action = Action()
    action.show()
    sys.exit(app.exec_())
