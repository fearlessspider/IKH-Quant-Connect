class Strategy:

    moneymanagement = None

    def __init__(self, moneymanagement):
        self.moneymanagement = moneymanagement

    def can_find_pattern(self, data):

        if self.moneymanagement.checkDrawdown() < - float(self.moneymanagement.algorithm.Portfolio.Cash) * 0.1:
            return False

        return True
