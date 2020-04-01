from signals import Signals


# Price Crose Kijun And Tenkan
class PriceCrossKijun(Signals):

    def __init__(self, moneymanagement):

        super().__init__(moneymanagement)

    def update(self, data, higher):

        self.moneymanagement.update_positions(data)

        if not self.can_find_pattern(data):
            return

        #if self.moneymanagement.calc_atr(higher) > 0.2:
            #return

        self.find_watterfall(data, higher)

    def can_find_pattern(self, data):

        if self.moneymanagement.checkDrawdown() < - float(self.moneymanagement.algorithm.Portfolio.Cash) * 0.1:
            return False

        return True
