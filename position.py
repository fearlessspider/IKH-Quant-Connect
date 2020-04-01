from decimal import Decimal


class Position(object):
    algorithm = None
    symbol = None
    sl = 0
    tp = []
    enter = 0
    leave = 0
    type = 0
    order = None
    stopOrder = None
    counterCheck = 0

    def __init__(self, name, algorithm, symbol, volume, type, delta, sl):
        self.tp = []
        self.algorithm = algorithm
        self.symbol = symbol
        self.type = type
        self.sl = sl
        self.order = self.algorithm.MarketOrder(self.symbol, type*volume, False, name)

        if self.order.Status != OrderStatus.Invalid:
            self.enter = self.order.AverageFillPrice
            self.tp.append(self.enter)

            if type == -1:
                self.stopOrder = self.algorithm.StopMarketOrder(self.symbol, -self.order.Quantity, sl,
                                               "SL to " + str(
                                                   self.order.AverageFillPrice))
                for k in range(1, 21):
                    self.tp.append(self.enter - (delta * k))
                    
            else:
                self.stopOrder = self.algorithm.StopMarketOrder(self.symbol, -self.order.Quantity, sl,
                                               "SL to " + str(
                                                   self.order.AverageFillPrice))
                for k in range(1, 21):
                    self.tp.append(self.enter + (delta * k))

    def __str__(self):
        return "SL: %f ENTER: %f TYPE: %d LEAVE: %f RESULT: %f %f" % (self.sl, self.enter, self.type, self.leave, self.type * (self.leave - self.enter), self.type * (self.leave - self.enter) * Decimal("90") - Decimal("0.50"))

    @property
    def Result(self):
        if self.leave != 0:
            return self.type * (self.leave - self.enter)
        return 0
