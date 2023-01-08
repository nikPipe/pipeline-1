from import_module import *
from widget.node_editor import node_graphic_edge


try:
    from importlib import reload
except:
    pass

for each in [node_graphic_edge]:
    reload(node_graphic_edge)


EDGE_TYPE_DIRECT = 1
EDGE_TYPE_BEZIER = 2

class Edge():
    def __init__(self, scene, start_socket, end_socket, edge_type=EDGE_TYPE_DIRECT):
        self.scene = scene
        self.start_socket = start_socket
        self.end_socket = end_socket

        self.start_socket.edge = self
        if self.end_socket is not None:
            self.end_socket.edge = self


        self.grEdge = node_graphic_edge.QDMGraphicsEdgeDirect(self) if edge_type == EDGE_TYPE_DIRECT else node_graphic_edge.QDMGraphicsEdgeBezier(self)

        self.update_position()
        self.scene.grScene.addItem(self.grEdge)


    def update_position(self):
        '''

        :return:
        '''
        source_pos = self.start_socket.getSocketPosition()
        source_pos[0] += self.start_socket.node.grNode.pos().x()
        source_pos[1] += self.start_socket.node.grNode.pos().y()
        self.grEdge.setSource(*source_pos)
        if self.end_socket is not None:
            end_pos = self.end_socket.getSocketPosition()
            end_pos[0] += self.end_socket.node.grNode.pos().x()
            end_pos[1] += self.end_socket.node.grNode.pos().y()
            self.grEdge.setDesination(*end_pos)

        self.grEdge.update()

    def remove_from_socket(self):
        '''

        :return:
        '''
        if self.start_socket is not None:
            self.start_socket.edge = None
        if self.end_socket is not None:
            self.end_socket.edge = None

        self.start_socket = None
        self.end_socket = None

    def remove(self):
        '''

        :return:
        '''
        self.remove_from_socket()
        self.scene.grScene.removeItem(self.grEdge)
        self.grEdge = None
        self.scene.removeEdge(self)



