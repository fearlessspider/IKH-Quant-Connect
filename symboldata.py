from QuantConnect.Indicators import *
from QuantConnect import *
from QuantConnect.Data.Consolidators import *
from QuantConnect.Data.Market import *
from QuantConnect.Indicators.CandlestickPatterns import *

from candle import Candle


class SymbolData(object):

    symbol = "eurjpy"
    period = 15
    tenkan = 9
    kijun = 26
    senkou = 52

    bar = None
    candles = []
    ichimoku = None
    pattern_long = None
    pattern_short = None
    patterns = []

    moneyManagement = []
    moneyManagerType = "kijunpullback"

    def __init__(self, symbol, period, tenkan, kijun, senkou, manager="kijunpullback"):
        self.candles = []
        self.patterns = []
        self.symbol = symbol
        self.period = period
        self.tenkan = tenkan
        self.kijun = kijun
        self.senkou = senkou
        self.moneyManagerType = manager
        self.moneyManagement = []

        # Short
        self.patterns.append(ThreeBlackCrows(self.symbol + "ThreeBlackCrows" + str(self.period)))  # -1
        self.patterns.append(StalledPattern(self.symbol + "StalledPattern" + str(self.period)))  # -1
        self.patterns.append(OnNeck(self.symbol + "OnNeck" + str(self.period)))  # -1
        self.patterns.append(InNeck(self.symbol + "InNeck" + str(self.period)))  # -1
        self.patterns.append(IdenticalThreeCrows(self.symbol + "IdenticalThreeCrows" + str(self.period)))  # -1
        self.patterns.append(HangingMan(self.symbol + "HangingMan" + str(self.period)))  # -1
        self.patterns.append(EveningDojiStar(self.symbol + "EveningDojiStar" + str(self.period)))  # -1
        self.patterns.append(AdvanceBlock(self.symbol + "AdvanceBlock" + str(self.period)))  # -1
        self.patterns.append(DarkCloudCover(self.symbol + "DarkCloudCover" + str(self.period)))  # -1
        self.patterns.append(EveningStar(self.symbol + "EveningStar" + str(self.period)))  # -1
        self.patterns.append(ShootingStar(self.symbol + "ShootingStar" + str(self.period)))  # -1
        self.patterns.append(Thrusting(self.symbol + "Thrusting" + str(self.period)))  # -1
        self.patterns.append(UpsideGapTwoCrows(self.symbol + "UpsideGapTwoCrows" + str(self.period)))  # -1

        # Long
        self.patterns.append(UniqueThreeRiver(self.symbol + "UniqueThreeRiver" + str(self.period)))  # +1
        self.patterns.append(DragonflyDoji(self.symbol + "DragonflyDoji" + str(self.period)))  # +1
        self.patterns.append(MorningStar(self.symbol + "MorningStar" + str(self.period)))  # +1
        self.patterns.append(ConcealedBabySwallow(self.symbol + "ConcealedBabySwallow" + str(self.period)))  # +1
        self.patterns.append(Doji(self.symbol + "Doji" + str(self.period)))  # +1
        self.patterns.append(GravestoneDoji(self.symbol + "GravestoneDoji" + str(self.period)))  # +1
        self.patterns.append(Hammer(self.symbol + "Hammer" + str(self.period)))  # +1
        self.patterns.append(HomingPigeon(self.symbol + "HomingPigeon" + str(self.period)))  # +1
        self.patterns.append(InvertedHammer(self.symbol + "InvertedHammer" + str(self.period)))  # +1
        self.patterns.append(LadderBottom(self.symbol + "LadderBottom" + str(self.period)))  # +1
        self.patterns.append(LongLeggedDoji(self.symbol + "LongLeggedDoji" + str(self.period)))  # +1
        self.patterns.append(MatHold(self.symbol + "MatHold" + str(self.period)))  # +1
        self.patterns.append(MatchingLow(self.symbol + "MatchingLow" + str(self.period)))  # +1
        self.patterns.append(MorningDojiStar(self.symbol + "MorningDojiStar" + str(self.period)))  # +1
        self.patterns.append(Piercing(self.symbol + "Piercing" + str(self.period)))  # +1
        self.patterns.append(RickshawMan(self.symbol + "RickshawMan" + str(self.period)))  # +1
        self.patterns.append(StickSandwich(self.symbol + "StickSandwich" + str(self.period)))  # +1
        self.patterns.append(Takuri(self.symbol + "Takuri" + str(self.period)))  # +1
        self.patterns.append(ThreeStarsInSouth(self.symbol + "ThreeStarsInSouth" + str(self.period)))  # +1
        self.patterns.append(ThreeWhiteSoldiers(self.symbol + "ThreeWhiteSoldiers" + str(self.period)))  # +1
        self.patterns.append(TwoCrows(self.symbol + "TwoCrows" + str(self.period)))  # +1

        # Long/Short
        self.patterns.append(Engulfing(self.symbol + "Engulfing" + str(self.period)))  # +1 -1
        self.patterns.append(Marubozu(self.symbol + "Marubozu" + str(self.period)))  # +1 -1
        self.patterns.append(Harami(self.symbol + "Harami" + str(self.period)))  # +1 -1
        self.patterns.append(AbandonedBaby(self.symbol + "AbandonedBaby" + str(self.period)))  # +1 -1
        self.patterns.append(ClosingMarubozu(self.symbol + "ClosingMarubozu" + str(self.period)))  # +1 -1
        self.patterns.append(ThreeInside(self.symbol + "ThreeInside" + str(self.period)))  # +1 -1
        self.patterns.append(BeltHold(self.symbol + "BeltHold" + str(self.period)))  # +1 -1
        self.patterns.append(Breakaway(self.symbol + "Breakaway" + str(self.period)))  # +1 -1
        self.patterns.append(Counterattack(self.symbol + "Counterattack" + str(self.period)))  # +1 -1
        self.patterns.append(DojiStar(self.symbol + "DojiStar" + str(self.period)))  # +1 -1
        self.patterns.append(GapSideBySideWhite(self.symbol + "GapSideBySideWhite" + str(self.period)))  # +1 -1
        self.patterns.append(HaramiCross(self.symbol + "HaramiCross" + str(self.period)))  # +1 -1
        self.patterns.append(HighWaveCandle(self.symbol + "HighWaveCandle" + str(self.period)))  # +1 -1
        self.patterns.append(Hikkake(self.symbol + "Hikkake" + str(self.period)))  # +1 -1
        self.patterns.append(HikkakeModified(self.symbol + "HikkakeModified" + str(self.period)))  # +1 -1
        self.patterns.append(Kicking(self.symbol + "Kicking" + str(self.period)))  # +1 -1
        self.patterns.append(KickingByLength(self.symbol + "KickingByLength" + str(self.period)))  # +1 -1
        self.patterns.append(LongLineCandle(self.symbol + "LongLineCandle" + str(self.period)))  # +1 -1
        self.patterns.append(RiseFallThreeMethods(self.symbol + "RiseFallThreeMethods" + str(self.period)))  # +1 -1
        self.patterns.append(SeparatingLines(self.symbol + "SeparatingLines" + str(self.period)))  # +1 -1
        self.patterns.append(ShortLineCandle(self.symbol + "ShortLineCandle" + str(self.period)))  # +1 -1
        self.patterns.append(SpinningTop(self.symbol + "SpinningTop" + str(self.period)))  # +1 -1
        self.patterns.append(TasukiGap(self.symbol + "TasukiGap" + str(self.period)))  # +1 -1
        self.patterns.append(ThreeLineStrike(self.symbol + "ThreeLineStrike" + str(self.period)))  # +1 -1
        self.patterns.append(ThreeOutside(self.symbol + "ThreeOutside" + str(self.period)))  # +1 -1
        self.patterns.append(Tristar(self.symbol + "Tristar" + str(self.period)))  # +1 -1
        self.patterns.append(UpDownGapThreeMethods(self.symbol + "UpDownGapThreeMethods" + str(self.period)))  # +1 -1

    def check_candle_patterns_long(self):
        self.pattern_long = None
        for pattern in self.patterns:
            if pattern.Current.Value == 1.0:
                self.pattern_long = pattern
                break

    def check_candle_patterns_short(self):
        self.pattern_short = None
        for pattern in self.patterns:
            if pattern.Current.Value == -1.0:
                self.pattern_short = pattern
                break

    def update_candles(self):
        self.candles.append(Candle(self.bar, self.ichimoku.Tenkan.Current.Value,
                              self.ichimoku.Kijun.Current.Value,
                              self.ichimoku.SenkouA.Current.Value,
                              self.ichimoku.SenkouB.Current.Value,
                              self.pattern_long, self.pattern_short))
