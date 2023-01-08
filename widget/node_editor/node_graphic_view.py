from import_module import *
import math
from widget.node_editor import node_graphic_socket, node_graphic_edge

MODE_NOOP = 1
MODE_EDGE_DRAG = 2

class QDMGraphicsView(QGraphicsView):
    def __init__(self, grScene, parent=None):
        super(QDMGraphicsView, self).__init__(parent)
        self.grScene = grScene

        self.initUI()
        self.mode = MODE_NOOP

        self.setScene(self.grScene)
        self.zoomInFactor = 1.25
        self.zoom = 10
        self.zoomStep = 1
        self.zoomClamp = False
        self.zoomRange = [0, 10]


    def initUI(self):
        '''

        :return:
        '''
        self.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonPressed(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonPressed(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonPressed(event)
        else:
            super().mousePressEvent(event)


    def mouseReleaseEvent(self, event):

        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonRelease(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonRelease(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)


    def middleMouseButtonPressed(self, event):
        '''

        :param event:
        :return:
        '''
        releaseEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(),
                                   Qt.LeftButton, Qt.NoButton, event.modifiers())
        super().mouseReleaseEvent(releaseEvent)

        self.setDragMode(QGraphicsView.ScrollHandDrag)
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
        super().mousePressEvent(fakeEvent)

    def leftMouseButtonPressed(self, event):
        '''

        :param event:
        :return:
        '''

        item = self.getItemAtClicked(event)
        self.last_lmb_click_scene_pos = self.mapToScene(event.pos())
        if type(item) is node_graphic_socket.QDMGraphicsSocket:
            if self.mode == MODE_NOOP:
                self.mode = MODE_EDGE_DRAG
                print('Start Dragging Edge')
                print('  assigned start socket')
                return

        if self.mode == MODE_EDGE_DRAG:
            self.mode = MODE_NOOP
            print('End Dragging Edge')
            if type(item) is node_graphic_socket.QDMGraphicsSocket:
                print('  assign End socket')
                return

        super().mousePressEvent(event)

    def rightMouseButtonPressed(self, event):
        '''

        :param event:
        :return:
        '''
        super().mousePressEvent(event)

    def middleMouseButtonRelease(self, event):
        '''

        :return:
        '''
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
        super().mouseReleaseEvent(fakeEvent)
        self.setDragMode(QGraphicsView.NoDrag)

    def leftMouseButtonRelease(self, event):
        '''

        :param event:
        :return:
        '''
        item = self.getItemAtClicked(event)
        if self.mode == MODE_EDGE_DRAG:
            new_lmb_click_scene_pos = self.mapToScene(event.pos())
            distance_scene_pos = new_lmb_click_scene_pos - self.last_lmb_click_scene_pos
            print('distance from click and release: ', distance_scene_pos)
            if mouse_has_not_moved_enough:
                pass
            else:
                self.mode = MODE_NOOP
                print('End Dragiing Edge')
                if type(item) == node_graphic_socket.QDMGraphicsSocket:
                    print('  assign End Socket')
        super().mouseReleaseEvent(event)

    def rightMouseButtonRelease(self, event):
        '''

        :param event:
        :return:
        '''
        super().mouseReleaseEvent(event)

    def getItemAtClicked(self, event):
        '''

        :param event:
        :return:
        '''
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj


    def wheelEvent(self, event):
        '''

        :param event:
        :return:
        '''
        #CALCULATE THE ZOOM FACTOR
        zoomOutFactor = 1/self.zoomInFactor

        #CALCULATE ZOOM
        if event.angleDelta().y() > 0:
            zoomFactor = self.zoomInFactor
            self.zoom += self.zoomStep
        else:
            zoomFactor = zoomOutFactor
            self.zoom -= self.zoomStep

        clamped = False
        if self.zoom < self.zoomRange[0] :
            self.zoom, clamped = self.zoomRange[0], True
        if self.zoom > self.zoomRange[1] :
            self.zoom, clamped = self.zoomRange[1], True


        #SET THE SCENE SCALE
        if not clamped or self.zoomClamp is False:
            self.scale(zoomFactor, zoomFactor)



