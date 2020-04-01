import pandas as pd

# Check lenght of Chikou Span
def distance_chikou_price(chikou, data):
    distance = 0
    for candle in data:
        if (candle.Close <= chikou <= candle.Open) or (candle.Open <= chikou <= candle.Close):
            break
        distance += 1
    return distance

# Check lenght of flat Kijun
def kijun_flat_distance(data):
    distance = 0
    for candle in reversed(data):
        if candle.Kijun != data[-1].Kijun:
            break
        distance += 1
    return distance

# Check lenght of flat Senkou B
def senkou_b_flat_distance(data):
    distance = 0
    for candle in reversed(data):
        if candle.SenkouB != data[-1].SenkouB:
            break
        distance += 1
    return distance

# Get HIGH from series
def get_high(candles):
    prices = []
    for candle in candles:
        prices.append(candle.High)

    return pd.Series(prices).max()

# Get LOW from series
def get_low(candles):
    prices = []
    for candle in candles:
        prices.append(candle.Low)

    return pd.Series(prices).min()
