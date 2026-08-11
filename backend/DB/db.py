class Database:
    def __init__(self):
        self.index = 0
        self.banco = {}

    def insert(self, id, object):
        self.banco[id] = object
    
    def getData(self):
        return self.banco
    
    def updateData(self, id):
        pass

    def next_index(self):
        self.index += 1

        yield self.index