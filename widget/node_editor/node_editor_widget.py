from import_module import *
from widget.sample import sample_widget_template
from widget.node_editor import node_scene
from widget.node_editor import node_graphic_view
from widget.node_editor.node_node import Node
from widget.node_editor import node_edge
from widget.node_editor.node_socket import Socket


try:
    from importlib import reload
except:
    pass

for each in [node_scene, node_graphic_view]:
    reload(each)


class NodeEditorWidget(QWidget):
    def __init__(self):
        super(NodeEditorWidget, self).__init__()
        self.sample_widget = sample_widget_template.SAMPLE_WIDGET_TEMPLATE()


        self.initUI()

    def initUI(self):
        '''

        :return:
        '''


        self.layout = self.sample_widget.vertical_layout(parent_self=self, set_contents_margins=[0, 0, 0, 0])


        # CREATE A GRAPHICS VIEW
        self.scene = node_scene.Scene()
        #self.grScene = self.scene.grScene

        self.addNode()


        #CREATE GRAPHICS SCENE
        self.view = node_graphic_view.QDMGraphicsView(self.scene.grScene, self)
        self.layout.addWidget(self.view)

        self.show()

        #self.addDebugContent()

    def addNode(self):
        '''

        :return:
        '''
        input = [1, 1, 1]
        output = [1]

        node1 = Node(self.scene, title='OneNode', inputs=input, outputs=output)
        node2 = Node(self.scene, title='TwoNode', inputs=input, outputs=output)
        node3 = Node(self.scene, title='ThreeNode', inputs=input, outputs=output)

        node1.setPosition(-350, -250)
        node2.setPosition(-75, 0)
        node3.setPosition(200, -150)

        edge1 = node_edge.Edge(scene=self.scene, start_socket=node1.outputs[0], end_socket=node2.inputs[0])
        edge1 = node_edge.Edge(scene=self.scene, start_socket=node2.outputs[0], end_socket=node3.inputs[2], edge_type=node_edge.EDGE_TYPE_BEZIER)

    def addDebugContent(self):
        '''

        :return:
        '''
        '''
        greenBrush = QBrush(Qt.green)

        outlinePen = QPen(Qt.black)
        outlinePen.setWidth(2)

        rect = self.grScene.addRect(-100, 100, 80, 100, outlinePen, greenBrush)
        rect.setFlag(QGraphicsItem.ItemIsMovable)
        print('this is working now')

        text = self.grScene.addText('This is my Text')
        '''
        greenBrush = QBrush(Qt.green)
        outlinePen = QPen(Qt.black)
        outlinePen.setWidth(2)

        divide = 4


        rect = self.grScene.addRect(-100, -100, 80, 100, outlinePen, greenBrush)
        rect.setFlag(QGraphicsItem.ItemIsMovable)


        text = self.grScene.addText("This is my Awesome text!", QFont("Ubuntu"))
        text.setFlag(QGraphicsItem.ItemIsSelectable)
        text.setFlag(QGraphicsItem.ItemIsMovable)
        text.setDefaultTextColor(QColor.fromRgbF(1.0, 1.0, 1.0))

        widget1 = QPushButton("Hello World")
        proxy1 = self.grScene.addWidget(widget1)
        proxy1.setFlag(QGraphicsItem.ItemIsMovable)
        proxy1.setPos(0, 30)

        widget2 = QTextEdit()
        proxy2 = self.grScene.addWidget(widget2)
        proxy2.setFlag(QGraphicsItem.ItemIsSelectable)
        proxy2.setPos(0, 60)

        line = self.grScene.addLine(-200, -200, 400, -100, outlinePen)
        line.setFlag(QGraphicsItem.ItemIsMovable)
        line.setFlag(QGraphicsItem.ItemIsSelectable)




