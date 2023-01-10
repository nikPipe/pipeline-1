import os.path

from import_module import *
from widget.node_editor import node_editor_widget

class NodeEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.filename = None
        self.initUI()

    def createAct(self, name, shortcut, toolTip, callback):
        '''

        :param name:
        :param shortcut:
        :param toolTip:
        :param callback:
        :return:
        '''
        act = QAction(name, self)
        act.setShortcut(shortcut)
        act.setToolTip(toolTip)
        act.triggered.connect(callback)
        return act

    def initUI(self):
        '''

        :return:
        '''
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('File')
        fileMenu.addAction(self.createAct(name='New', shortcut='Ctrl+N', toolTip='Create New Scene', callback=self.on_file_new))
        fileMenu.addSeparator()
        fileMenu.addAction(self.createAct(name='Open', shortcut='Ctrl+O', toolTip='Open File', callback=self.on_file_open))
        fileMenu.addAction(self.createAct(name='Save', shortcut='Ctrl+S', toolTip='Save File', callback=self.on_file_save))
        fileMenu.addAction(self.createAct(name='SaveAs', shortcut='Ctrl+Shift+S', toolTip='Save As File', callback=self.on_file_saveAs))
        fileMenu.addSeparator()
        fileMenu.addAction(self.createAct(name='Exit', shortcut='Ctrl+Q', toolTip='Close', callback=self.close))

        editMenu = menuBar.addMenu('Edit')
        editMenu.addAction(self.createAct(name='Undo', shortcut='Ctrl+Z', toolTip='Undo', callback=self.on_file_undo))
        editMenu.addAction(self.createAct(name='Redo', shortcut='Ctrl+Shift+Z', toolTip='Redo', callback=self.on_file_redo))
        editMenu.addSeparator()
        editMenu.addAction(self.createAct(name='Delete', shortcut='Del', toolTip='Delete', callback=self.on_file_delete))



        nodeeditor_widget = node_editor_widget.NodeEditorWidget()
        self.setCentralWidget(nodeeditor_widget)

        self.statusBar().showMessage('')
        self.status_mouse_pos = QLabel('')
        self.statusBar().addPermanentWidget(self.status_mouse_pos)
        nodeeditor_widget.view.scenePosChange.connect(self.onSceneChanged)

        #SET WINDOW PROPERTY
        self.setWindowTitle('NodeEditor')
        self.setGeometry(200, 200, 1000, 600)
        self.show()

    def onSceneChanged(self, x, y):
        '''

        :return:
        '''
        self.status_mouse_pos.setText('Scene Pos: (%d %d)' %(x, y))

    def on_file_new(self):
        '''

        :return:
        '''
        self.centralWidget().scene.clear()


    def on_file_open(self):
        '''

        :return:
        '''
        fileName, filter = QFileDialog.getOpenFileNames(self, 'Open Graph From File')
        if fileName == '':
            return
        if os.path.isfile(fileName[0]):
            self.centralWidget().scene.loadFromFile(fileName[0])

    def on_file_save(self):
        '''

        :return:
        '''
        if self.filename is None: return self.on_file_saveAs()

        self.centralWidget().scene.saveToFile(self.filename)
        self.statusBar().showMessage('SucessFully Save %s' % self.filename)


    def on_file_saveAs(self):
        '''

        :return:
        '''
        fileName, filter = QFileDialog.getSaveFileName(self, 'Save Graph to File')
        if fileName == '':
            return
        print(fileName)
        self.filename = fileName
        self.on_file_save()

    def on_file_undo(self):
        '''

        :return:
        '''
        self.centralWidget().scene.history.undo()

    def on_file_redo(self):
        '''

        :return:
        '''
        self.centralWidget().scene.history.redo()

    def on_file_delete(self):
        '''

        :return:
        '''
        self.centralWidget().scene.grScene.views()[0].deleteSelected()

