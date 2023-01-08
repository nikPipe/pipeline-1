from import_module import *


class QDMGraphicsSocket(QGraphicsItem):
    def __init__(self, parent=None, socket_type=1):
        super(QDMGraphicsSocket, self).__init__(parent=parent)

        self.radius = 6.0
        self.outline_width = 1.0

        self.colors = [
            QColor('#FFFF7700'),
            QColor('#FF52e220'),
            QColor('#FF0053a6'),
            QColor('#FFa86db1')
        ]

        self._color_background = self.colors[socket_type]
        self._color_outline = QColor('#FF000000')

        self._pen = QPen(self._color_outline)
        self._pen.setWidthF(self.outline_width)
        self._brush = QBrush(self._color_background)

    def boundingRect(self):
        return QRectF(
            -self.radius - self.outline_width,
            -self.radius - self.outline_width,
            2 * self.radius + self.outline_width,
            2 * self.radius + self.outline_width
        ).normalized()
    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        '''

        :param painter:
        :param QStyleOptionGraphicsItem:
        :param widget:
        :return:
        '''
        #PAINTING CIRCLE
        painter.setBrush(self._brush)
        painter.setPen(self._pen)
        painter.drawEllipse(int(-self.radius), int(-self.radius), int(2*self.radius), int(2*self.radius))


