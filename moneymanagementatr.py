from alpha import Alpha
from drawdown import Drawdown
from position import Position
from positionsize import PositionSize
from stoplose import StopLose


class MoneyManagementAtr(Alpha, PositionSize, Drawdown, StopLose):
    positions = []
    orderType = 0

    def __init__(self, algorithm, symbol, tenkan, kijun, senkou, period=15):

        super().__init__(algorithm, symbol, tenkan, kijun, senkou, period)

        self.algorithm = algorithm
        self.symbol = symbol
        self.tenkan = tenkan
        self.kijun = kijun
        self.senkou = senkou
        self.positions = []
        self.balanceHistory = []
        self.period = period

    def open_position(self, data, type=1):
        openNewPosition = True
        for position in self.positions:
            if position.tp[2] < data[-1].Close and position.type == type and position.leave == 0:
                openNewPosition = False
                break
        if openNewPosition:
            self.open_order(data, type)

    def open_order(self, data, type=1):
        self.close_orders(type*-1)

        sl = self.calc_stop_lose(data, type)
        delta = self.calc_delta_with_atr(data, sl)

        check_position = self.checkSLPosition(delta, type, data)

        self.algorithm.EmitInsights(
            # Creates an insight for our symbol, predicting that it will move down
            Insight.Price(self.symbol,
                          self.getInsightTimedelta(), InsightDirection.Down if type == -1 else InsightDirection.Up,
                          self.getMagnitude(data[-1].Close, delta*4*type+data[-1].Close),
                          self.getConfidence())
        )

        newPosition = Position("MM", self.algorithm, self.symbol, check_position, type, delta, sl)

        self.orderType = type

        if newPosition.order.Status != OrderStatus.Invalid:

            pos = 0
            for position in self.positions:
                if position.type == type and position.leave == 0:
                    position.tp = newPosition.tp
                    position.sl = newPosition.sl
                    self.positions[pos] = position
                pos += 1

            self.positions.append(newPosition)

    def close_orders(self, type=1):
        self.orderType = 0
        pos = 0
        for position in self.positions:
            if position.stopOrder and position.stopOrder.Status != OrderStatus.Filled and position.stopOrder.Status != OrderStatus.Canceled and position.type == type:
                position.stopOrder.Cancel("Close Stop")

            if position.leave == 0 and position.type == type:
                newTicket = self.algorithm.MarketOrder(self.symbol, -position.order.QuantityFilled, False,
                                                       "Close Long " + str(position.enter))
                if newTicket.Status != OrderStatus.Invalid:
                    self.algorithm.Log("Close Long {0}: L {1} {2}".format(self.algorithm.Time, newTicket.AverageFillPrice, position.order.QuantityFilled))
                    position.leave = newTicket.AverageFillPrice
            self.positions[pos] = position
            pos += 1

    def update_positions(self, data):
        pos = 0
        for position in self.positions:
            if position.leave == 0:

                if self.close_positions_at_the_end(position, data):
                    continue

                for k in range(len(position.tp)-1, 2, -1):
                    # Move SL to previous TP
                    if position.type == -1 and data[-1].Close <= position.tp[k - 1] and position.sl > position.tp[
                        k - 2] and data[-1].isDown:
                        position.sl = position.tp[k - 2]
                        if position.stopOrder:
                            order = self.algorithm.Transactions.GetOrderById(position.stopOrder.OrderId)
                            if order.Status != OrderStatus.Filled and order.Status != OrderStatus.Canceled:
                                stopTicket = self.algorithm.StopMarketOrder(self.symbol, order.Quantity, position.sl,
                                                                            "SL to " + str(
                                                                                position.order.AverageFillPrice))
                                self.algorithm.Log(
                                    "Stop Short {0}: {1}: {2}".format(self.algorithm.Time, position.sl, order.Quantity))
                                position.stopOrder.Cancel("SL to " + str(position.order.AverageFillPrice))
                                position.stopOrder = stopTicket

                        else:
                            stopTicket = self.algorithm.StopMarketOrder(self.symbol, -position.order.Quantity,
                                                                        position.sl,
                                                                        "SL to " + str(position.order.AverageFillPrice))
                            self.algorithm.Log("Stop Short {0}: {1}: {2}".format(self.algorithm.Time, position.sl,
                                                                                 position.order.Quantity))
                            position.stopOrder = stopTicket

                        break
                    elif position.type == 1 and data[-1].Close >= position.tp[k - 1] and position.sl < position.tp[
                        k - 2] and data[-1].isUp:
                        position.sl = position.tp[k - 2]
                        if position.stopOrder:
                            order = self.algorithm.Transactions.GetOrderById(position.stopOrder.OrderId)
                            if order.Status != OrderStatus.Filled and order.Status != OrderStatus.Canceled:
                                stopTicket = self.algorithm.StopMarketOrder(self.symbol, order.Quantity, position.sl,
                                                                             "SL to " + str(
                                                                                position.order.AverageFillPrice))
                                self.algorithm.Log(
                                    "Stop Long {0}: {1}: {2}".format(self.algorithm.Time, position.sl, order.Quantity))
                                position.stopOrder.Cancel("SL to " + str(position.order.AverageFillPrice))
                                position.stopOrder = stopTicket

                        else:
                            stopTicket = self.algorithm.StopMarketOrder(self.symbol, -position.order.Quantity,
                                                                        position.sl,
                                                                        "SL to " + str(position.order.AverageFillPrice))
                            self.algorithm.Log("Stop Long {0}: {1}: {2}".format(self.algorithm.Time, position.sl,
                                                                                position.order.Quantity))
                            position.stopOrder = stopTicket

                        break
                position.counterCheck += 1

            self.positions[pos] = position
            pos += 1

    def close_positions_at_the_end(self, position, data):
        if (position.type == -1 and data[-1].Close <= position.tp[-1]) or (
                position.type == 1 and data[-1].Close >= position.tp[-1]):
            self.close_position(data, position)
            return True
        elif position.counterCheck == 3 and self.period < 60:
            if position.type == 1 and data[-1].Close < data[-1].Tenkan:
                self.close_position(data, position)
                return True
            if position.type == -1 and data[-1].Close > data[-1].Tenkan:
                self.close_position(data, position)
                return True

        return False


    def close_position(self, data, position):
        position.leave = data[-1].Close
        if position.stopOrder:
            position.stopOrder.Cancel()
        if position.type != 0:
            self.close_orders(position.type)
        self.algorithm.MarketOrder(self.symbol, -position.order.Quantity, False,
                                                "Result " + str(position.type * (position.leave - position.enter)))
        self.algorithm.Log(
            "Close Short {0}: {1}: {2}".format(self.algorithm.Time, data[-1].Close, position.order.Quantity))
        return position
