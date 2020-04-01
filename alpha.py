from datetime import timedelta

class Alpha:

    tenkan = 9
    kijun = 26
    senkou = 52

    period = 15
    bonus = 0

    def __init__(self, algorithm, symbol, tenkan, kijun, senkou, period=15):

        self.tenkan = tenkan
        self.kijun = kijun
        self.senkou = senkou
        self.period = period

    def getInsightTimedelta(self):
        return timedelta(minutes=(self.kijun * self.period))


    def getConfidence(self):
        return (self.bonus + 0.8)


    def getMagnitude(self, enter, predict):
        if predict > 0:
            return float(round((predict / enter) - 1, 4))
        return 0.01
