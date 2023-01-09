from import_module import *

class QDMGraphicsNode(QGraphicsItem):
    def __init__(self, node, parent=None):
        super(QDMGraphicsNode, self).__init__(parent)

        self.node = node
        self.content = self.node.content


        self._title_color = Qt.white
        self._title_font = QFont('Ubuntu', 10)

        self.width = 200
        self.height = 300
        self.edge_size = 10.0
        self.title_height = 24
        self._padding = 10
        self.title_x_pos = self._padding
        self.title_y_pos = 0

        self._brush_title = QBrush(QColor('#FF313131'))
        self._brush_background = QBrush(QColor('#E3212121'))

        self._pen_default = QPen(QColor('#7F000000'))
        self._pen_selected = QPen(QColor('#FFFFA637'))

        self.initTitle()
        self.title = self.node.title

        #INIT SOCKET
        self.initSocket()

        #INIT CONTENT
        self.initContent()

        self.initUI()

    def mouseMoveEvent(self, event):
        '''

        :param event:
        :return:
        '''
        super().mouseMoveEvent(event)
        #self.node.updateConnectedEdge()
        for node in self.scene().scene.nodes:
            if node.grNode.isSelected():
                node.updateConnectedEdge()



    def boundingRect(self):
        return QRectF(
            0,
            0,
            self.width,
            self.height
        ).normalized()

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value
        self.titleItem.setPlainText(self._title)

    def initUI(self):
        '''

        :return:
        '''
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)

    def initContent(self):
        '''

        :return:
        '''
        self.grContent = QGraphicsProxyWidget(self)
        self.content.setGeometry(int(self.edge_size), int(self.title_height + self.edge_size),
                                 int(self.width - (2 * self.edge_size)), int(self.height - (2 * self.edge_size) - self.title_height))
        self.grContent.setWidget(self.content)

    def initSocket(self):
        '''

        :return:
        '''
        pass


    def initTitle(self):
        '''

        :return:
        '''
        self.titleItem = QGraphicsTextItem(self)
        self.titleItem.node = self.node
        self.titleItem.setDefaultTextColor(self._title_color)
        self.titleItem.setFont(self._title_font)
        self.titleItem.setPos(self.title_x_pos, self.title_y_pos)
        self.titleItem.setTextWidth(
            self.width - (2 * self._padding)
        )



    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        '''

        :param painter:
        :param QStyleOptionGraphicsItem:
        :param widget:
        :return:
        '''
        #TITILE
        path_title = QPainterPath()
        path_title.setFillRule(Qt.WindingFill)
        path_title.addRoundedRect(0, 0, self.width, self.title_height, self.edge_size, self.edge_size)
        path_title.addRect(0, self.title_height -self.edge_size, self.edge_size, self.edge_size)
        path_title.addRect(self.width - self.edge_size, self.title_height -self.edge_size, self.edge_size, self.edge_size)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_title)
        painter.drawPath(path_title.simplified())

        #CONTENT
        path_content = QPainterPath()
        path_content.setFillRule(Qt.WindingFill)
        path_content.addRoundedRect(0, self.title_height, self.width, self.height - self.title_height, self.edge_size, self.edge_size)
        path_content.addRect(0, self.title_height, self.edge_size, self.edge_size)
        path_content.addRect(self.width - self.edge_size, self.title_height, self.edge_size, self.edge_size)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_background)
        painter.drawPath(path_content.simplified())

        #OUTLINE
        path_outline = QPainterPath()
        path_outline.addRoundedRect(0, 0, self.width, self.height, self.edge_size, self.edge_size)
        painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path_outline.simplified())
