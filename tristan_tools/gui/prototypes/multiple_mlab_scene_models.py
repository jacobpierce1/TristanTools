# http://docs.enthought.com/mayavi/mayavi/auto/example_multiple_mlab_scene_models.html#example-multiple-mlab-scene-models

disable_toolbar = 1

import numpy as np

from traits.api import HasTraits, Instance, Button, on_trait_change

from traitsui.api import View, Item, HSplit, Group, Handler

from mayavi import mlab
from mayavi.core.ui.api import MlabSceneModel, SceneEditor


class MyDialog(HasTraits):

    scene1 = Instance(MlabSceneModel, ())
    scene2 = Instance(MlabSceneModel, ())

    button1 = Button('Redraw')
    button2 = Button('Redraw')

    @on_trait_change('button1')
    def redraw_scene1(self):
        self.redraw_scene(self.scene1)

    @on_trait_change('button2')
    def redraw_scene2(self):
        self.redraw_scene(self.scene2)

    def redraw_scene(self, scene):
        # Notice how each mlab call points explicitely to the figure it
        # applies to.
        mlab.clf(figure=scene.mayavi_scene)
        x, y, z, s = np.random.random((4, 100))
        mlab.points3d(x, y, z, s, figure=scene.mayavi_scene)

    # The layout of the dialog created
    view = View(HSplit(
                  Group(
                       Item('scene1',
                            editor=SceneEditor(), height=250,
                            width=300),
                       'button1',
                       show_labels=False,
                  ),
                  Group(
                       Item('scene2',
                            editor=SceneEditor(), height=250,
                            width=300, show_label=False),
                       'button2',
                       show_labels=False,
                  ),
                ),
                resizable=True,
                )

class DisableToolbarHandler(Handler):
    def position(self, info):
        for name in ["scene1", "scene2"]:
            editor = info.ui.get_editors(name)[0]
            editor._scene._tool_bar.setVisible(False)




m = MyDialog()

if disable_toolbar :
    m.configure_traits( handler=DisableToolbarHandler() )

else :
    m.configure_traits()
