from import_module import *


class QDMGraphicsEdge(QGraphicsPathItem):
    def __init__(self, edge, parent=None):
        super().__init__(parent)

        self.edge = edge
        self._color = QColor('#001000')
        self._color_selected = QColor('#00ff00')

        self._pen = QPen(self._color)
        self._pen_selected = QPen(self._color_selected)

        self.posSource = [0, 0]
        self.posDesination = [200, 100]

        self._pen.setWidthF(2.0)
        self._pen_selected.setWidthF(2.0)

        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setZValue(-1)

    def setSource(self, x, y):
        '''

        :param x:
        :param y:
        :return:
        '''
        self.posSource = [x, y]

    def setDesination(self, x, y):
        '''

        :param x:
        :param y:
        :return:
        '''
        self.posDesination = [x, y]


    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        '''

        :param painter:
        :param QStyleOptionGraphicsItem:
        :param widget:
        :return:
        '''
        self.update_path()


        painter.setPen(self._pen_selected if self.isSelected() else self._pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(self.path())

    def update_path(self):
        '''
        drawing QPainter path from A to B
        :return:
        '''
        raise NotImplemented('This Method has been overwritten in the child class')

class QDMGraphicsEdgeDirect(QDMGraphicsEdge):
    def update_path(self):
        path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))
        path.lineTo(self.posDesination[0], self.posDesination[1])
        self.setPath(path)




class QDMGraphicsEdgeBezier(QDMGraphicsEdge):
    def update_path(self):
        s = self.posSource
        d = self.posDesination
        dis = (d[0] - s[0])/2 * 0.5
        if s[0]> d[0]: dis *= -1



        path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))
        path.cubicTo(s[0] + dis, s[1] + dis,
                     d[0] - dis, d[1] - dis,
                     self.posDesination[0], self.posDesination[1])
        self.setPath(path)