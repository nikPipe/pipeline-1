


class Serializable():
    def __init__(self):
        '''

        :return:
        '''
        self.id = id(self)

    def serialize(self):
        '''

        :return:
        '''
        raise NotImplemented()

    def deserialize(self, data, hashmao=[]):
        '''

        :return:
        '''
        raise NotImplemented()
