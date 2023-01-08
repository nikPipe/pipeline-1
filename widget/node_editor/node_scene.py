from import_module import *
from widget.sample import sample_widget_template
from widget.node_editor import node_graphic_scene


try:
    from importlib import reload
except:
    pass

for each in [node_graphic_scene]:
    reload(each)

class Scene():
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.scene_width = 64000
        self.scene_height = 64000

        self.initUI()

    def initUI(self):
        '''

        :return:
        '''
        self.grScene = node_graphic_scene.QDMGraphicsScene(self)
        self.grScene.setGrScene(width=self.scene_width, height=self.scene_height)

    def addNode(self, node):
        self.nodes.append(node)

    def addEdge(self, edge):
        '''

        :param edge:
        :return:
        '''
        self.edges.append(edge)

    def removeNode(self, node):
        '''

        :param node:
        :return:
        '''
        self.nodes.remove(node)

    def removeEdge(self, edge):
        '''

        :param edge:
        :return:
        '''
        self.edges.remove(edge)