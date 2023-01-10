from widget.node_editor import node_graphic_edge
DEBUG = True
class SceneHistory():
    def __init__(self, scene):
        '''

        :param scene:
        :return:
        '''
        self.scene = scene

        self.history_stake = []
        self.history_current_step = -1
        self.history_limit = 32

    def undo(self):
        '''

        :return:
        '''
        if DEBUG: print('Undo')
        if self.history_current_step > 0:
            self.history_current_step -= 1
            self.restore_history()

    def redo(self):
        '''

        :return:
        '''
        if DEBUG: print('Redo')

        if self.history_current_step + 1 < len(self.history_stake):
            self.history_current_step += 1
            self.restore_history()

    def restore_history(self):
        '''

        :return:
        '''
        if DEBUG: print('restoring history ..... current step: @%d' % self.history_current_step,
                        '%d' % len(self.history_stake))
        self.restore_historyStamp(self.history_stake[self.history_current_step])

    def store_history(self, desc):
        if DEBUG: print('storing history ', '%s' % desc,
                        '..... current step: @%d' % self.history_current_step,
                        '%d' % len(self.history_stake))

        if self.history_current_step+1 < len(self.history_stake):
            self.history_stake = self.history_stake[0:self.history_current_step+1]

        #if the history is outside of the limit
        if self.history_current_step + 1 >= self.history_limit:
            self.history_stake = self.history_stake[1:]
            self.history_current_step -= 1

        hs = self.create_history_stamp(desc)

        self.history_stake.append(hs)
        self.history_current_step += 1
        if DEBUG: print('    setting stop to --- ', self.history_current_step)

    def create_history_stamp(self, desc):
        '''

        :param desc:
        :return:
        '''
        sel_obj = {
            'nodes': [],
            'edges': []
        }
        for item in self.scene.grScene.selectedItems():
            if hasattr(item, 'node'):
                sel_obj['nodes'].append(item.node.id)
            elif isinstance(item, node_graphic_edge.QDMGraphicsEdge):
                sel_obj['edges'].append(item.edge.id)

        history_stamp= {
            'desc': desc,
            'snapshot':self.scene.serialize(),
            'selection':sel_obj
        }


        return history_stamp

    def restore_historyStamp(self, history_stamp):
        if DEBUG: print(history_stamp)

        self.scene.deseralize(data=history_stamp['snapshot'])

        for edgeId in history_stamp['selection']['edges']:
            for edge in self.scene.edges:
                if edge.id  == edgeId:
                    edge.grEdge.setSelected(True)
                    break

        for nodeID in history_stamp['selection']['nodes']:
            for node in self.scene.nodes:
                if node.id == nodeID:
                    node.grNode.setSelected(True)
                    break

