from import_module import *
import math

class QDMGraphicsScene(QGraphicsScene):
    def __init__(self, scene, parent=None):
        super(QDMGraphicsScene, self).__init__(parent)

        self.scene = scene
        #setting
        self.gridSize = 20
        self.gridSquare = 4

        self._color_background = QColor('#393939')
        self._color_light = QColor('#2f2f2f')
        self._color_dark = QColor('#292929')

        #LIGHT PEN
        self._pen_light = QPen(self._color_light)
        self._pen_light.setWidth(1)
        #DARK PEN
        self._pen_dark = QPen(self._color_dark)
        self._pen_dark.setWidth(3)

        self.setBackgroundBrush(self._color_background)




    def setGrScene(self, width, height):
        '''

        :param width:
        :param height:
        :return:
        '''
        self.setSceneRect(-width // 2, -height // 2, width, height)


    def drawBackground(self, painter, rect):
        super(QDMGraphicsScene, self).drawBackground(painter, rect)

        #here we create a grid
        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.ceil(rect.bottom()))

        first_left = left - (left % self.gridSize)
        first_top = top - (top % self.gridSize)


        #compute all the line to drawn
        lines_light, line_dark = [], []
        for x in range(first_left, right, self.gridSize):
            if (x % (self.gridSize * self.gridSquare) != 0):
                lines_light.append(QLine(x, top, x, bottom))
            else:
                line_dark.append(QLine(x, top, x, bottom))

        for y in range(first_top, bottom, self.gridSize):
            if (y % (self.gridSize * self.gridSquare) != 0):
                lines_light.append(QLine(left, y, right, y))
            else:
                line_dark.append(QLine(left, y, right, y))

        #draw a lines
        painter.setPen(self._pen_light)
        painter.drawLines(*lines_light)

        painter.setPen(self._pen_dark)
        painter.drawLines(*line_dark)
