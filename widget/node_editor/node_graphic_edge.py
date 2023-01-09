import math

from import_module import *
from widget.node_editor import node_socket
EDGE_CP_ROUNDNESS = 100
class QDMGraphicsEdge(QGraphicsPathItem):
    def __init__(self, edge, parent=None):
        super().__init__(parent)

        self.edge = edge
        self._color = QColor('#001000')
        self._color_selected = QColor('#00ff00')

        self._pen = QPen(self._color)
        self._pen_selected = QPen(self._color_selected)
        self._pen_dragging = QPen(self._color)
        self._pen_dragging.setStyle(Qt.DashLine)

        self.posSource = [0, 0]
        self.posDesination = [200, 100]

        self._pen.setWidthF(2.0)
        self._pen_selected.setWidthF(2.0)
        self._pen_dragging.setWidthF(2.0)

        self.setFlag(QGraphicsItem.ItemIsSelectable)
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
        self.setPath(self.calc_path())


        if self.edge.end_socket is None:
            painter.setPen(self._pen_dragging)
        else:
            painter.setPen(self._pen_selected if self.isSelected() else self._pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(self.path())

    def intersectsWith(self, p1, p2):
        '''

        :return:
        '''
        cutPath = QPainterPath(p1)
        cutPath.lineTo(p2)
        path = self.calc_path()
        return cutPath.intersects(path)


    def calc_path(self):
        '''
        drawing QPainter path from A to B
        :return:
        '''
        raise NotImplemented('This Method has been overwritten in the child class')

class QDMGraphicsEdgeDirect(QDMGraphicsEdge):
    def calc_path(self):
        path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))
        path.lineTo(self.posDesination[0], self.posDesination[1])
        return path



class QDMGraphicsEdgeBezier(QDMGraphicsEdge):
    def calc_path(self):
        s = self.posSource
        d = self.posDesination
        dis = (d[0] - s[0])/2 * 0.5

        cpx_s = +dis
        cpx_d = -dis
        cpy_s = 0
        cpy_d = 0

        sspos = self.edge.start_socket.position

        if (s[0] > d[0]) and sspos is (node_socket.RIGHT_TOP, node_socket.RIGHT_BOTTOM) or (s[0] < d[0] and sspos in (node_socket.LEFT_TOP, node_socket.LEFT_BOTTOM)):
            cpx_d *= -1
            cpx_s *= -1

            cpy_d = ((s[1] - d[1]) / math.fabs(
                (s[1] - d[1]) if (s[1] - d[1]) != 0 else 0.00001)) * EDGE_CP_ROUNDNESS

            cpy_s = ((d[1] - s[1]) / math.fabs(
                (d[1] - s[1]) if (d[1] - s[1]) != 0 else 0.00001)) * EDGE_CP_ROUNDNESS

        path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))
        path.cubicTo(s[0] + cpx_s, s[1] + cpy_s + dis,
                     d[0] + cpx_d, d[1] + cpy_d - dis,
                     self.posDesination[0], self.posDesination[1])
        return path