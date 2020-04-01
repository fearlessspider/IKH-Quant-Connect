class Balance(object):

    # type : w - week, d - day, m - month
    def __init__(self, start):
        self.start = start
        self.end = start
        self.type = 'd'

    @property
    def profit(self):
        return self.end - self.start
