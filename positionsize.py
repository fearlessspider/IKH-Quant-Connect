from decimal import Decimal


class PositionSize:

    symbol = "USDJPY"
    algorithm = None
    bonus = 0

    def __init__(self, algorithm, symbol, tenkan, kijun, senkou, period=15):

        self.symbol = symbol
        self.algorithm = algorithm

    # Get POINT value for current asset
    def get_point_value(self):
        # lotSize = 1000
        conversionRate = self.algorithm.Portfolio.Securities[self.symbol].QuoteCurrency.ConversionRate

        # conversionRate = 1.31819(GBPUSD)
        pointValue = self.get_lot_size() * conversionRate
        # pointValue = 1318.19USD
        return pointValue

    # Get LOT size
    def get_lot_size(self):
        # E.g.: symbol = "EURGBP";
        lotSize = self.algorithm.Portfolio.Securities[self.symbol].SymbolProperties.LotSize

        return lotSize

    def checkSLPosition(self, sl, type, data):
        self.algorithm.Log("Check {0}".format(sl))
        _bonus = self.bonus

        _volume = Decimal(0.01) * self.get_wins_lose_multiplier()

        position = self.get_point_value() * Decimal(sl)
        lot = (self.algorithm.Portfolio.Cash * (_volume + Decimal(_bonus))) * self.get_lot_size() / position

        orderQua = abs(self.algorithm.CalculateOrderQuantity(self.symbol, 38 * type))
        #buiyng = self.algorithm.Portfolio.GetBuyingPower(self.symbol, OrderDirectiondirection = OrderDirection.Up)

        if lot > orderQua:
            return int(orderQua)

        return int(lot)

    # Get wins and loses multiplier from closed positions
    def get_wins_lose_multiplier(self):
        multiplier = 1
        positionClosed = []

        for position in self.positions:
            if position.leave > 0:
                positionClosed.append(position)

        if len(positionClosed) > 0:
            if positionClosed[-1].Result >= 0:
                multiplier += 1

                if len(positionClosed) > 1:
                    if positionClosed[-2].Result >= 0:
                        multiplier += 1

                        if len(positionClosed) > 2:
                            if positionClosed[-3].Result >= 0:
                                multiplier += 1

            if positionClosed[-1].Result < 0:
                multiplier -= 0.1

                if len(positionClosed) > 1:
                    if positionClosed[-2].Result < 0:
                        multiplier -= 0.1

                        if len(positionClosed) > 2:
                            if positionClosed[-3].Result < 0:
                                multiplier -= 0.1

        return multiplier
