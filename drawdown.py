
class Drawdown:

    balanceHistory = []

    def __init__(self, algorithm, symbol, tenkan, kijun, senkou, period=15):
        pass

    def checkDrawdown(self):
        profit = 0
        if len(self.balanceHistory) > 7:
            for balance in self.balanceHistory[-7:]:
                profit += balance.profit
            return profit
        return 0
