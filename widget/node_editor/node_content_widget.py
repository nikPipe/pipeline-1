from import_module import *
from widget.sample import sample_widget_template

try:
    from importlib import reload
except:
    pass

for each in [sample_widget_template]:
    reload(each)


class QDMNodeWidget(QWidget):
    def __init__(self, parent=None):
        super(QDMNodeWidget, self).__init__()
        self.sample_widget_template = sample_widget_template.SAMPLE_WIDGET_TEMPLATE()
        self.initUI()

    def initUI(self):
        '''

        :return:
        '''
        self.layout = self.sample_widget_template.vertical_layout(parent_self=self, set_contents_margins=[0, 0, 0, 0])

        label = self.sample_widget_template.label(set_text='Test')
        self.layout.addWidget(label)

        self.layout.addWidget(self.sample_widget_template.plainTextEdit())


        pushButton = self.sample_widget_template.pushButton(set_text='this is button')
        self.layout.addWidget(pushButton)
