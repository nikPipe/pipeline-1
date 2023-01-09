
from import_module import *
from widget.node_editor import node_graphics_node
from widget.node_editor import node_content_widget
from widget.node_editor import node_socket
try:
    from importlib import reload
except:
    pass
for each in [node_graphics_node, node_content_widget, node_socket]:
    reload(each)

class Node():
    def __init__(self, scene, title='Define Node', inputs=[], outputs=[]):
        '''

        :param scene:
        :param title:
        '''
        self.scene = scene
        self.title = title
        self.socket_spacing = 20

        self.content = node_content_widget.QDMNodeWidget()
        self.grNode = node_graphics_node.QDMGraphicsNode(node=self)


        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)
        #self.grNode.title = 'something'


        #CREATE A SOCKET FROM INPUTS AND OUTPUT
        self.inputs = []
        self.outputs = []
        a = 0
        for each in inputs:
            socket = node_socket.Socket(node=self, index=a, position=node_socket.LEFT_BOTTOM, socket_type=a)
            self.inputs.append(socket)
            a+=1

        a = 0
        for each in outputs:
            socket = node_socket.Socket(node=self, index=a, position=node_socket.RIGHT_TOP, socket_type=a)
            self.outputs.append(socket)
            a += 1

    def __str__(self):
        '''

        :return:
        '''
        return '<Node %s...%s>' % (hex(id(self))[2:5], hex(id(self))[-3:])

    def getSocketPosition(self, index, position):
        '''

        :param index:
        :param position:
        :return:
        '''
        x = 0 if position in (node_socket.LEFT_TOP, node_socket.LEFT_BOTTOM) else self.grNode.width
        if position in (node_socket.LEFT_BOTTOM, node_socket.RIGHT_BOTTOM):
            y = self.grNode.height - self.grNode.edge_size - self.grNode._padding - index * self.socket_spacing
        else:
            y = self.grNode.title_height + self.grNode._padding + self.grNode.edge_size +  (index * self.socket_spacing)


        return [x, y]

    @property
    def pos(self):
        self.grNode.pos()

    def setPosition(self, x, y):
        '''

        :param x:
        :param y:
        :return:
        '''
        self.grNode.setPos(x, y)

    def updateConnectedEdge(self):
        '''

        :return:
        '''
        for socket in self.inputs + self.outputs:
            if socket.hasEdge():
                socket.edge.update_position()

    def remove(self):
        '''

        :return:
        '''

        #REMOVE EDGE FROM SOCKET
        for socket in (self.inputs + self.outputs):
            if socket.hasEdge():
                socket.edge.remove()
        #REMOVE NODE
        self.scene.grScene.removeItem(self.grNode)
        self.grNode = None
        #REMOVE ITEM
        self.scene.removeNode(self)


