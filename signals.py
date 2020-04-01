from pattern import Pattern
from utils import distance_chikou_price


class Signals:

    moneymanagement = None

    def __init__(self, moneymanagement):

        self.moneymanagement = moneymanagement

    def find_watterfall(self, data, higher):

        if data[-1].Kumo < 0.0 and data[-1].isCloseBelowTenkan and data[-1].isTenkanBelowKijun and data[-2].isTenkanBelowKijun:
            if data[-1].isOpenAboveKijun and abs(data[-1].OC) > abs(data[-2].OC):
                pattern = Pattern("pricecrosskijun" + str(self.moneymanagement.period), 0)
                data[-1].pattern_short = pattern
                if data[-2].Tenkan > data[-1].Tenkan and distance_chikou_price(data[-1].Close, data) > 26 and higher[-1].Kijun < higher[-1].SenkouA:
                    # Short
                    self.moneymanagement.open_order(data, -1)

        elif data[-1].Kumo > 0.0 and data[-1].isCloseAboveTenkan and data[-1].isTenkanAboveKijun and data[-2].isTenkanAboveKijun:
            if data[-1].isOpenBelowKijun and abs(data[-1].OC) > abs(data[-2].OC):
                pattern = Pattern("pricecrosskijun" + str(self.moneymanagement.period), 0)
                data[-1].pattern_long = pattern
                if data[-2].Tenkan < data[-1].Tenkan and distance_chikou_price(data[-1].Close, data) > 26 and higher[-1].Kijun > higher[-1].SenkouA:
                    # Long
                    self.moneymanagement.open_order(data, 1)
