from utils import get_low, get_high


class StopLose:

    def __init__(self, algorithm, symbol, tenkan, kijun, senkou, period=15):
        pass

    # Calculate Average True Range based on High, Low and Close
    def calc_atr(self, data):
        atr = 0
        prevCandle = data[-2]
        for candle in data[-10:-2]:
            atr += max(data[-1].HL, (data[-1].Low - prevCandle.Close), (data[-1].High - prevCandle.Close))
            prevCandle = candle
        atr = atr/9
        return atr

    # Calculate Averate True Range based on High and Low
    def calc_hl_atr(self, data):
        atr = 0
        for candle in data[-10:-2]:
            atr += candle.HL
        atr = atr/9
        return atr

    # Calcualte DELTA for TAKE PROFITS based on STOP LOSE and Close price
    def calc_delta(self, data, sl):
        return abs(data[-1].Close - sl)# + atr

    # Calculate DELTA for TAKE PROFITS based on STOP LOSE and Close price and Average True Range
    def calc_delta_with_atr(self, data, sl):
        atr = self.calc_atr(data)

        return abs(data[-1].Close - sl)/2# + atr

    # Calculate STOP LOSE based on Ichimoku lines
    def calc_stop_lose(self, data, type):

        sl = data[-1].Kijun
        if data[-2].Kijun == data[-3].Kijun:
            low = get_low(data[-27:-2])
            high = get_high(data[-27:-2])
            if type == 1:
                sl = low
            if type == -1:
                sl = high

        if abs(data[-1].KijunSenkouA) < abs(data[-1].OC):
            sl = data[-1].SenkouA

        #atr = self.calc_atr(data)
        #if atr > 0.1:
        #    sl += -1 * type * atr

        #atr = self.calc_hl_atr(data)
        #if atr < 0.03:
        #    sl = data[-1].SenkouB

        return sl
