import pathlib

class gnu:
    def __init__(self, path, name):
        self.path = pathlib.Path(path)
        self.name = name
