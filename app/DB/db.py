class Database:
    def __init__(self):
        self.banco = {}

    def insert(self, id, object):
        self.banco[id] = object
    
    def getData(self):
        return self.banco
    
    def updateData(self, id):
        pass