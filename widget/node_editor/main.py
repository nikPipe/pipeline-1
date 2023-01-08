from import_module import *
from widget.node_editor import node_editor_wnd
import sys

try:
    from importlib import reload
except:
    pass


for each in [node_editor_wnd]:
    reload(each)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = node_editor_wnd.NodeEditorWnd()


    sys.exit(app.exec_())
