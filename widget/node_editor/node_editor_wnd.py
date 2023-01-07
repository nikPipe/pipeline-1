from import_module import *


class NodeEditorWnd(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI_()

    def initUI(self):
        '''

        :return:
        '''
        self.setWindowTitle('NodeEditor')
        self.setGeometry(200, 200, 1000, 600)

        #CREATE GRAPHICS SCENE

        #CREATE A GRAPHICS VIEW


        self.show()