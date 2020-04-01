class Pattern(object):

    def __init__(self, name, value):
        self.name = name
        self.value = value

    @property
    def Name(self):
        return self.name

    @property
    def Value(self):
        return self.value

