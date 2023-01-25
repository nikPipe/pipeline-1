from import_module import *
from widget.sample import sample_widget_template
from widget.node_editor import node_graphic_scene
from widget.node_editor.node_serializable import Serializable
from collections import OrderedDict
from widget.node_editor.node_node import Node
from widget.node_editor.node_edge import Edge
from widget.node_editor.node_scene_history import SceneHistory
from widget.node_editor.node_scene_clipboard import SceneClipboard
import json


try:
    from importlib import reload
except:
    pass

for each in [node_graphic_scene]:
    reload(each)

class Scene(Serializable):
    def __init__(self):
        super().__init__()
        self.nodes = []
        self.edges = []
        self.scene_width = 64000
        self.scene_height = 64000

        self.initUI()
        self.history = SceneHistory(self)
        self.clipboard = SceneClipboard(self)

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

    def clear(self):
        '''

        :return:
        '''
        while len(self.nodes) > 0:
            self.nodes[0].remove()

    def saveToFile(self, fileName):
        '''

        :param fileName:
        :return:
        '''
        with open(fileName, 'w') as file:
            file.write(json.dumps(self.serialize(), indent=4))

        print('saving to ' + fileName + ' sucessfully')

    def loadFromFile(self, fileName):
        '''

        :param fileName:
        :return:
        '''
        with open(fileName, 'r') as file:
            rawData = file.read()
            data = json.loads(rawData)
            self.deseralize(data)

    def serialize(self):
        '''

        :return:
        '''
        nodes, edges = [], []
        for node in self.nodes: nodes.append(node.serialize())
        for edge in self.edges: edges.append(edge.serialize())

        return OrderedDict([
            ('id', self.id),
            ('scene_width', self.scene_width),
            ('scene_height', self.scene_height),
            ('nodes', nodes),
            ('edges', edges),
        ])
    def deseralize(self, data, hashmap=[], restore_id=True):
        '''

        :return:
        '''
        print('Deseralizating data: ', data)
        self.clear()
        if restore_id:self.id = data['id']

        hashmap={}

        #CREATE NODES
        for node_data in data['nodes']:
            Node(self).deseralize(node_data, hashmap, restore_id)

        #CREATE EDGES
        for edge_data in data['edges']:
            new_edge = Edge(self).deseralize(edge_data, hashmap, restore_id)

        return True


