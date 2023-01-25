
from collections import OrderedDict
import  node_graphic_edge
DEBUG = True

class SceneClipboard():
    def __init__(self, scene):
        '''

        :param scene:
        '''
        self.scene = scene

    def serializeSelected(self, delete=False):
        '''

        :param delete:
        :return:
        '''
        sel_nodes, sel_edges, sel_socket = [], [], {}

        #SORT EDGES AND NODES
        for item in self.scene.grScene.selectedItems():
            print(item)
            if hasattr(item, 'node'):
                sel_nodes.append(item.node.serialize())
                for socket in (item.node.inputs + item.node.outputs):
                    sel_socket[socket.id] = socket

            if isinstance(item, node_graphic_edge.QDMGraphicsEdge):
                print('1>>>> ', item)

        if DEBUG:
            print(' Nodes:\n         ', sel_nodes)
            print(' Socket:\n         ', sel_socket)
            print(' Edges:\n         ', sel_edges)

        #REMOVE THE EDGE IS NOT CONNECTED

        #CREATE ORDER DICTONARY
        data = OrderedDict([

        ])

        #IF CUT REMOVE SELECTED ITEM
        if delete:
            self.scene.grScene.view().deleteSelected()



        return data

    def serializefromClipboard(self, data):
        '''

        :param data:
        :return:
        '''
        print('deseralize from clipboard')
