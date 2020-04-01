#
#   Ichimoku Kinko Quant
#
from clr import AddReference

from moneymanagement import MoneyManagement
from moneymanagementatr import MoneyManagementAtr
from pricecrosskijun import PriceCrossKijun

AddReference("System")
AddReference("QuantConnect.Algorithm")
AddReference("QuantConnect.Algorithm.Framework")
AddReference("QuantConnect.Common")
AddReference("QuantConnect.Indicators")

from System import *
from QuantConnect import *
from QuantConnect.Algorithm import *
from QuantConnect.Algorithm.Framework import *
from QuantConnect.Algorithm.Framework.Alphas import *
from QuantConnect.Indicators import *
from QuantConnect.Indicators.CandlestickPatterns import *

from datetime import timedelta

from symboldata import SymbolData


class IKQAlgorithm(QCAlgorithmFrameworkBridge):

    def Initialize(self):

        # Set requested data resolution
        # self.UniverseSettings.Resolution = Resolution.Minute

        # Set the cash we'd like to use for our backtest
        # This is ignored in live trading 
        self.SetCash(1000)

        # Start and end dates for the backtest.
        # These are ignored in likeve trading.
        self.SetStartDate(2011, 1, 1)
        #self.SetEndDate(2016, 1, 1)

        self.symbols = [
            #["EURUSD", ["kijunpullback"], [9, 33, 129], [26, 65, 257], [52, 130, 514], 10],
            #["GBPNZD", ["pricecrosskijun"], [9,9,9], [26,26,26], [52,52,52]],
            #["GBPAUD", ["pricecrosskijun"], [9, 9, 9], [26, 26, 26], [52, 52, 52]],
            ["GBPJPY", ["pricecrosskijun"], [9, 9, 9], [26, 26, 26], [52, 52, 52]],
            #["GBPUSD", ["pricecrosskijun"], [9, 9, 9], [26, 26, 26], [52, 52, 52]],
            #["GBPCHF", ["pricecrosskijun"], [9, 9, 9], [26, 26, 26], [52, 52, 52]],
            #["EURGBP", ["pricecrosskijun"], [9, 9, 9], [26, 26, 26], [52, 52, 52]],
            #["EURUSD", ["pricecrosskijun"], [9, 9, 9], [26, 26, 26], [52, 52, 52]],
            #["EURAUD", ["pricecrosskijun"], [9, 9, 9], [26, 26, 26], [52, 52, 52]],
            #["EURNZD", ["pricecrosskijun"], [9, 9, 9], [26, 26, 26], [52, 52, 52]],
            #["AUDUSD", ["pricecrosskijun"], [9, 9, 9], [26, 26, 26], [52, 52, 52]],
            #["AUDCHF", ["pricecrosskijun"], [9, 9, 9], [26, 26, 26], [52, 52, 52]],
            #["AUDNZD", ["pricecrosskijun"], [9, 9, 9], [26, 26, 26], [52, 52, 52]],
            #["AUDJPY", ["pricecrosskijun"], [9, 9, 9], [26, 26, 26], [52, 52, 52]],
            #["EURJPY", ["pricecrosskijun"], [9, 9, 9], [26, 26, 26], [52, 52, 52]],
            #["CADJPY", ["pricecrosskijun"], [9, 9, 9], [26, 26, 26], [52, 52, 52]],
            #["USDJPY", ["pricecrosskijun"], [9, 9, 9], [26, 26, 26], [52, 52, 52]],
            #["NZDJPY", ["pricecrosskijun"], [9, 9, 9], [26, 26, 26], [52, 52, 52]],
        ]

        # Set Brokerage model to load OANDA fee structure.
        self.SetBrokerageModel(BrokerageName.OandaBrokerage)
        # Add assets you'd like to see
        # Code Automatically Generated

        # Holds all of our data keyed by each symbol
        self.Data15 = {}
        self.Data60 = {}

        for symbol, managerType, tenkan, kijun, senkou in self.symbols:
            forex = self.AddSecurity(SecurityType.Forex, symbol, Resolution.Minute, leverage=30.0)
            self.Data15[symbol] = SymbolData(symbol, 15, tenkan[0], kijun[0], senkou[0], managerType)
            self.Data60[symbol] = SymbolData(symbol, 60, tenkan[1], kijun[1], senkou[1], managerType)

        # loop through all our symbols and request data subscriptions and initialize indicator
        for symbol, symbolData in self.Data15.items():
            # define a consolidator to consolidate data for this symbol on the requested period
            consolidator = QuoteBarConsolidator(timedelta(minutes=symbolData.period))
            self.register_indicators(symbol, symbolData, consolidator)
            # write up our consolidator to update the indicator
            consolidator.DataConsolidated += self.OnDataConsolidated15
            # we need to add this consolidator so it gets auto updates
            self.SubscriptionManager.AddConsolidator(symbol, consolidator)
            bars = map(lambda x: x[symbol], self.History(timedelta(53), Resolution.Minute))

            for bar in bars:
                consolidator.Update(bar)

        for symbol, symbolData in self.Data60.items():
            # define a consolidator to consolidate data for this symbol on the requested period
            consolidator = QuoteBarConsolidator(timedelta(minutes=symbolData.period))
            self.register_indicators(symbol, symbolData, consolidator)
            # write up our consolidator to update the indicator
            consolidator.DataConsolidated += self.OnDataConsolidated60
            # we need to add this consolidator so it gets auto updates
            self.SubscriptionManager.AddConsolidator(symbol, consolidator)
            bars = map(lambda x: x[symbol], self.History(timedelta(53), Resolution.Minute))

            for bar in bars:
                consolidator.Update(bar)

        self.SetWarmUp(timedelta(53))

    def register_indicators(self, symbol, symbolData, consolidator):
        # define the indicator
        symbolData.ichimoku = IchimokuKinkoHyo(
            self.CreateIndicatorName(symbol, "IKH" + str(symbolData.period), Resolution.Minute), symbolData.tenkan, symbolData.kijun, symbolData.kijun,
            symbolData.senkou, symbolData.kijun, symbolData.kijun)

        symbolData.moneyManagement.append(MoneyManagement(self, symbol, symbolData.tenkan, symbolData.kijun, symbolData.senkou, symbolData.period))
        symbolData.moneyManagement.append(MoneyManagementAtr(self, symbol, symbolData.tenkan, symbolData.kijun, symbolData.senkou, symbolData.period))

        self.RegisterIndicator(symbol, symbolData.ichimoku, consolidator)

        for pattern in symbolData.patterns:
            self.RegisterIndicator(symbol, pattern, consolidator)

    def OnDataConsolidated15(self, sender, bar):
        '''This is our event handler for our 30 minute trade bar defined above in Initialize(). So each time the
        consolidator produces a new 30 minute bar, this function will be called automatically. The 'sender' parameter
         will be the instance of the IDataConsolidator that invoked the event, but you'll almost never need that!'''
        if bar.Symbol.Value not in self.Data15:
            return

        if self.IsWarmingUp:
            return

        self.Data15[bar.Symbol.Value].bar = bar
        self.Data15[bar.Symbol.Value].check_candle_patterns_long()
        self.Data15[bar.Symbol.Value].check_candle_patterns_short()
        self.Data15[bar.Symbol.Value].update_candles()

        if len(self.Data60[bar.Symbol.Value].candles) > 53:
            if "pricecrosskijun" in self.Data15[bar.Symbol.Value].moneyManagerType:
                PriceCrossKijun(self.Data15[bar.Symbol.Value].moneyManagement[0]).update(self.Data15[bar.Symbol.Value].candles, self.Data60[bar.Symbol.Value].candles)
                PriceCrossKijun(self.Data15[bar.Symbol.Value].moneyManagement[1]).update(self.Data15[bar.Symbol.Value].candles, self.Data60[bar.Symbol.Value].candles)


    def OnDataConsolidated60(self, sender, bar):
        '''This is our event handler for our 30 minute trade bar defined above in Initialize(). So each time the
        consolidator produces a new 30 minute bar, this function will be called automatically. The 'sender' parameter
         will be the instance of the IDataConsolidator that invoked the event, but you'll almost never need that!'''
        if bar.Symbol.Value not in self.Data60:
            return

        if self.IsWarmingUp:
            return

        self.Data60[bar.Symbol.Value].bar = bar
        self.Data60[bar.Symbol.Value].check_candle_patterns_long()
        self.Data60[bar.Symbol.Value].check_candle_patterns_short()
        self.Data60[bar.Symbol.Value].update_candles()


    def OnOrderEvent(self, orderEvent):

        self.after_order_event(self.Data15, orderEvent)
        self.after_order_event(self.Data60, orderEvent)


    def after_order_event(self, data, orderEvent):
        order = self.Transactions.GetOrderById(orderEvent.OrderId)
        for symbol, symbolData in data.items():
            for management in symbolData.moneyManagement:
                pos = 0
                for position in management.positions:
                    if position.stopOrder and position.stopOrder.OrderId == orderEvent.OrderId and order.Status == OrderStatus.Filled:
                        position.leave = order.StopPrice
                        self.Log("Filled {0}: {1}: {2}: Result:{3}".format(self.Time, order.Type, orderEvent,
                                                                           position.Result))
                        management.positions[pos] = position
                        management.close_orders(position.type)

                        break

                    pos += 1
