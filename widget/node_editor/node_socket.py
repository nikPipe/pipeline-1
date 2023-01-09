from import_module import *
from widget.node_editor import node_graphic_socket

LEFT_TOP = 1
LEFT_BOTTOM = 2
RIGHT_TOP = 3
RIGHT_BOTTOM = 4


class Socket():
    def __init__(self, node, index=0, position=LEFT_TOP, socket_type=1):

        self.node = node
        self.index = index
        self.position = position
        self.socket_type = socket_type

        self.grSocket = node_graphic_socket.QDMGraphicsSocket(self, self.socket_type)

        self.grSocket.setPos(*self.node.getSocketPosition(index=self.index, position=self.position))

        self.edge = None

    def getSocketPosition(self):
        '''

        :return:
        '''


        return self.node.getSocketPosition(self.index, self.position)

    def setConnectedEdge(self, edge=None):
        '''

        :param edge:
        :return:
        '''
        self.edge = edge

    def hasEdge(self):
        '''

        :return:
        '''
        return self.edge is not None

    def __str__(self):
        '''

        :return:
        '''
        return '<Socket %s...%s>' % (hex(id(self))[2:5], hex(id(self))[-3:])