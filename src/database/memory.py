import os

from walrus import *


class MemoryDb:
    db = Database(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), db=0)
    memory = {}

    def append(self, id, value):
        self.memory[id] = value
        data = self.db.List(id)
        data.append(value)

    def get(self, id):
        try:
            return self.db.get_key(id).decode()
        except AttributeError as ae:
            print(ae)
            return 0
        except Exception as ae:
            print('Error not found Key', ae)
            return 0
