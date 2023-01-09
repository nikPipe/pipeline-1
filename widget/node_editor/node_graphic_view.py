from import_module import *
import math
from widget.node_editor import node_graphic_socket, node_graphic_edge, node_graphics_cutline
from widget.node_editor import node_edge

try:
    from importlib import reload
except:
    pass

for each in [node_graphic_edge, node_graphic_socket, node_edge, node_graphics_cutline]:
    reload(each)


MODE_NOOP = 1
MODE_EDGE_DRAG = 2
MODE_EDGE_CUT = 3

EDGE_DRAG_START_THRESHOLD = 10
DEBUG = True
class QDMGraphicsView(QGraphicsView):
    def __init__(self, grScene, parent=None):
        super(QDMGraphicsView, self).__init__(parent)
        self.grScene = grScene

        self.initUI()
        self.mode = MODE_NOOP
        self.editingFlag = False

        self.setScene(self.grScene)
        self.zoomInFactor = 1.25
        self.zoom = 10
        self.zoomStep = 1
        self.zoomClamp = False
        self.zoomRange = [0, 10]

        #CUTLINE
        self.cutline = node_graphics_cutline.QDMCutLine()
        self.grScene.addItem(self.cutline)


    def initUI(self):
        '''

        :return:
        '''
        self.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.RubberBandDrag)

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

        if hasattr(item, 'node') or isinstance(item, node_graphic_edge.QDMGraphicsEdge) or item is None:
            if event.modifiers() & Qt.ShiftModifier:
                if DEBUG: print('Shift and LLM is Selected')
                event.ignore()
                fakeEvent = QMouseEvent(QEvent.MouseButtonPress, event.localPos(), event.screenPos(),
                                        Qt.LeftButton, event.buttons() | Qt.LeftButton,
                                        event.modifiers() | Qt.ControlModifier)

                super().mousePressEvent(fakeEvent)
                return


        if type(item) is node_graphic_socket.QDMGraphicsSocket:
            if self.mode == MODE_NOOP:
                self.mode = MODE_EDGE_DRAG
                self.edgeDragStart(item)
                return

        if self.mode == MODE_EDGE_DRAG:
            self.mode = MODE_NOOP
            res = self.edgeDragEnd(item)
            if res: return

        if item is None:
            if event.modifiers() & Qt.ControlModifier:
                self.mode = MODE_EDGE_CUT
                fakeEvent =QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(), Qt.LeftButton,
                                       Qt.NoButton, event.modifiers())
                super().mouseReleaseEvent(fakeEvent)
                QApplication.setOverrideCursor(Qt.CrossCursor)
                return

        super().mousePressEvent(event)

    def rightMouseButtonPressed(self, event):
        '''

        :param event:
        :return:
        '''
        super().mousePressEvent(event)
        item = self.getItemAtClicked(event)
        if DEBUG:
            if type(item) is node_graphic_socket.QDMGraphicsSocket: print('RMB DEBUG: ', item.socket, ' has edge: ', item.socket.edge)

            if item is None:
                print('Scene: ')
                print('Node: ')
                for node in self.grScene.scene.nodes: print('    ', node)
                print('Edge: ')
                for edge in self.grScene.scene.edges: print('    ', edge)

            if isinstance(item, node_graphic_edge.QDMGraphicsEdge): print('RMB Debug: ', item.edge, 'Connecting sockets',
                                                                          item.edge.start_socket, ' <------> ', item.edge.end_socket)

    def middleMouseButtonRelease(self, event):
        '''

        :return:
        '''
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
        super().mouseReleaseEvent(fakeEvent)
        self.setDragMode(QGraphicsView.NoDrag)

    def edgeDragStart(self, item):
        '''

        :param item:
        :return:
        '''
        print('Start Dragging Edge')
        print('  assigned start socket to ', item.socket)
        self.previousEdge = item.socket.edge
        self.last_start_socket = item.socket
        self.dragEdge = node_edge.Edge(self.grScene.scene, item.socket, None, node_edge.EDGE_TYPE_BEZIER)
        if DEBUG:
            print('dragEdge: ', self.dragEdge)
    def edgeDragEnd(self, item):
        self.mode = MODE_NOOP
        print('End Dragiing Edge')
        if type(item) == node_graphic_socket.QDMGraphicsSocket:
            if item.socket != self.last_start_socket:
                if item.socket.hasEdge():
                    item.socket.edge.remove()
                print('  assign End Socket: ', item.socket)
                if self.previousEdge is not None:
                    self.previousEdge.remove()
                self.dragEdge.start_socket = self.last_start_socket
                self.dragEdge.end_socket = item.socket
                self.dragEdge.start_socket.setConnectedEdge(self.dragEdge)
                self.dragEdge.end_socket.setConnectedEdge(self.dragEdge)
                self.dragEdge.update_position()
                if DEBUG:
                    print('reassign start and end Socket to dragEdge')
                return True

        self.dragEdge.remove()
        self.dragEdge = None
        if DEBUG: print('about to set the socket to previous Edge')
        if self.previousEdge is not None:
            self.previousEdge.start_socket.edge = self.previousEdge

        return False

    def mouseMoveEvent(self, event):
        '''

        :param event:
        :return:
        '''
        if self.mode == MODE_EDGE_DRAG:
            pos = self.mapToScene(event.pos())
            self.dragEdge.grEdge.setDesination(pos.x(), pos.y())
            self.dragEdge.grEdge.update()

        if self.mode == MODE_EDGE_CUT:
            pos = self.mapToScene(event.pos())
            self.cutline.line_points.append(pos)
            self.cutline.update()

        super().mouseMoveEvent(event)


    def distanceBetweenClickandReleaseOff(self, event):
        '''

        :return:
        '''
        new_lmb_click_scene_pos = self.mapToScene(event.pos())
        dis_scene = new_lmb_click_scene_pos - self.last_lmb_click_scene_pos
        edge_drag_sqare = EDGE_DRAG_START_THRESHOLD * EDGE_DRAG_START_THRESHOLD
        return (dis_scene.x() * dis_scene.x() + dis_scene.y() * dis_scene.y()) > edge_drag_sqare

    def leftMouseButtonRelease(self, event):
        '''

        :param event:
        :return:
        '''
        item = self.getItemAtClicked(event)

        if hasattr(item, 'node') or isinstance(item, node_graphic_edge.QDMGraphicsEdge) or item is None:
            if event.modifiers() & Qt.ShiftModifier:
                if DEBUG: print('Shift and LLM is Release')
                event.ignore()
                fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                        Qt.LeftButton, Qt.NoButton,
                                        event.modifiers() | Qt.ControlModifier)

                super().mouseReleaseEvent(fakeEvent)
                return

        if self.mode == MODE_EDGE_DRAG:
            new_lmb_click_scene_pos = self.mapToScene(event.pos())
            dis_scene = new_lmb_click_scene_pos - self.last_lmb_click_scene_pos
            print('distance from click and release: ', dis_scene)

            if self.distanceBetweenClickandReleaseOff(event):
                res = self.edgeDragEnd(item)
                if res: return

        if self.mode == MODE_EDGE_CUT:
            self.cutIntersectingEdges()
            self.cutline.line_points = []
            self.cutline.update()
            QApplication.setOverrideCursor(Qt.ArrowCursor)
            self.mode = MODE_NOOP
            return
        super().mouseReleaseEvent(event)

    def cutIntersectingEdges(self):
        '''

        :return:
        '''
        for ix in range(len(self.cutline.line_points) - 1):
            p1 = self.cutline.line_points[ix]
            p2 = self.cutline.line_points[ix + 1]
            for edge in self.grScene.scene.edges:
                if edge.grEdge.intersectsWith(p1, p2):
                    edge.remove()

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

    def keyPressEvent(self, event):
        '''

        :param event:
        :return:
        '''
        if event.key() == Qt.Key_Delete:
            self.deleteSelected()

        else:
            super().keyPressEvent(event)

    def deleteSelected(self):
        '''

        :return:
        '''
        for eachItem in self.grScene.selectedItems():
            if isinstance(eachItem, node_graphic_edge.QDMGraphicsEdge):
                eachItem.edge.remove()
            elif hasattr(eachItem, 'node'):
                eachItem.node.remove()