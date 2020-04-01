from decimal import Decimal


class Candle(object):
    bar = None
    tenkan = 0.0
    kijun = 0.0
    senkouA = 0.0
    senkouB = 0.0
    pattern_long = None
    pattern_short = None

    def __init__(self, bar, tenkan, kijun, senkouA, senkouB, pattern_long=None, pattern_short=None):
        self.bar = bar
        self.tenkan = tenkan
        self.kijun = kijun
        self.senkouA = senkouA
        self.senkouB = senkouB
        self.pattern_long = pattern_long
        self.pattern_short = pattern_short

    @property
    def Open(self):
        return self.bar.Open

    @property
    def High(self):
        return self.bar.High

    @property
    def Low(self):
        return self.bar.Low

    @property
    def Close(self):
        return self.bar.Close

    @property
    def Time(self):
        return self.bar.EndTime

    @property
    def Tenkan(self):
        return self.tenkan

    @property
    def Kijun(self):
        return self.kijun

    @property
    def SenkouA(self):
        return self.senkouA

    @property
    def SenkouB(self):
        return self.senkouB

    @property
    def Chikou(self):
        return self.bar.Close

    @property
    def OC(self):
        return self.bar.Close - self.bar.Open

    @property
    def HL(self):
        return self.bar.High - self.bar.Low

    @property
    def Kumo(self):
        return self.SenkouA - self.SenkouB

    @property
    def KijunSenkouA(self):
        return self.Kijun - self.SenkouA

    @property
    def KijunSenkouB(self):
        return self.Kijun - self.SenkouB

    @property
    def KijunTenkan(self):
        return abs(self.Kijun - self.Tenkan)

    @property
    def KijunClose(self):
        return abs(self.Kijun - self.Close)

    @property
    def KijunOpen(self):
        return abs(self.Kijun - self.Open)

    @property
    def SenkouAOpen(self):
        return abs(self.SenkouA - self.Open)

    @property
    def SenkouBOpen(self):
        return abs(self.SenkouA - self.Open)

    @property
    def isCloseBelowTenkan(self):
        return self.Close < self.Tenkan

    @property
    def isCloseBelowKijun(self):
        return self.Close < self.Kijun

    @property
    def isCloseAboveTenkan(self):
        return self.Close > self.Tenkan

    @property
    def isCloseAboveKijun(self):
        return self.Close > self.Kijun

    @property
    def isOpenBelowTenkan(self):
        return self.Open < self.Tenkan

    @property
    def isOpenBelowKijun(self):
        return self.Open < self.Kijun

    @property
    def isOpenAboveTenkan(self):
        return self.Open > self.Tenkan

    @property
    def isOpenAboveKijun(self):
        return self.Open > self.Kijun

    @property
    def isTenkanBelowKijun(self):
        return self.Tenkan < self.Kijun

    @property
    def isTenkanAboveKijun(self):
        return self.Tenkan > self.Kijun

    @property
    def MiddleOfBody(self):
        if (self.HL - abs(self.OC)) < (self.HL * Decimal(0.4)):
            thirty = abs(self.OC) / Decimal(3)
            return (self.Low + thirty), (self.High - thirty)
        return None

    @property
    def patternLongValue(self):
        if self.pattern_long:
            return self.pattern_long.Current.Value
        return 0

    @property
    def patternShortValue(self):
        if self.pattern_short:
            return self.pattern_short.Current.Value
        return 0

    @property
    def isPatternDown(self):
        return self.patternShortValue == -1.0 and self.OC <= 0.0

    @property
    def isPatternUp(self):
        return self.patternLongValue == 1.0 and self.OC >= 0.0

    # close and ichimoku
    @property
    def isDown(self):
        return self.OC < 0

    @property
    def isUp(self):
        return self.OC > 0
