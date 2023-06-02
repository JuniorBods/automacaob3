import pandas as pd
import numpy as np

def relative_strength_index(close_prices, window_size=14):
    """
    Retorna o Índice de Força Relativa (IFR) para um conjunto de preços de fechamento.

    :param close_prices: uma lista ou array com preços de fechamento de um ativo financeiro.
    :param window_size: tamanho da janela deslizante para calcular o IFR. Padrão é 14.
    :return: uma lista com os valores do IFR.
    """

    deltas = np.diff(close_prices)
    seed = deltas[:window_size + 1]
    up = seed[seed >= 0].sum() / window_size
    down = -seed[seed < 0].sum() / window_size
    rs = up / down
    rsi = [100.0 - (100.0 / (1.0 + rs))]

    for i in range(0, len(deltas)):
        delta = deltas[i]
        if delta > 0:
            upval = delta
            downval = 0.0
        else:
            upval = 0.0
            downval = -delta

        up = (up * (window_size - 1) + upval) / window_size
        down = (down * (window_size - 1) + downval) / window_size

        rs = up / down
        rsi.append(100.0 - (100.0 / (1.0 + rs)))

    return rsi


def hull_moving_average(close_prices, window_size=20):
    """
    Retorna a Média Móvel de Hull (HMA) para um conjunto de preços de fechamento.

    :param close_prices: uma lista ou array com preços de fechamento de um ativo financeiro.
    :param window_size: tamanho da janela deslizante para calcular o HMA. Padrão é 20.
    :return: uma lista com os valores do HMA.
    """

    half_length = int(window_size / 2)
    sqrt_length = int(np.sqrt(window_size))

    wma1 = pd.Series(close_prices).rolling(window=half_length).mean()
    wma2 = pd.Series(close_prices).rolling(window=window_size).mean()
    diff = (2 * wma1 - wma2).fillna(0)
    hma = pd.Series(diff).rolling(window=sqrt_length).mean()

    return hma.tolist()


def hilo(high_prices, low_prices, close_prices):
    """
    Retorna os valores do HiLo (Máximo e Mínimo) para um conjunto de preços de alta, baixa e fechamento.

    :param high_prices: uma lista ou array com preços altos de um ativo financeiro.
    :param low_prices: uma lista ou array com preços baixos de um ativo financeiro.
    :param close_prices: uma lista ou array com preços de fechamento de um ativo financeiro.
    :return: uma tupla de duas listas: (máximo HiLo, mínimo HiLo).
    """

    hilo_high = [max(high_prices[i], close_prices[i - 1]) for i in range(1, len(close_prices))]
    hilo_low = [min(low_prices[i], close_prices[i - 1]) for i in range(1, len(close_prices))]

    return hilo_high, hilo_low


def commoditychannelindex(high_prices, low_prices, close_prices, window_size=20): 
    """ 
    Retorna o Commodity Channel Index (CCI) para um conjunto de preços de alta, 
    baixa e fechamento.
    :param high_prices: uma lista ou array com preços altos de um ativo financeiro.
    :param low_prices: uma lista ou array com preços baixos de um ativo financeiro.
    :param close_prices: uma lista ou array com preços de fechamento de um ativo financeiro.
    :param window_size: tamanho da janela deslizante para calcular o CCI. Padrão é 20.
    :return: uma lista com os valores do CCI.
"""
    typical_price = [(high + low + close) / 3 for high, low, close in zip(high_prices, low_prices, close_prices)]

    sma_tp = pd.Series(typical_price).rolling(window=window_size).mean()
    mad_tp = pd.Series(np.abs(typical_price - sma_tp)).rolling(window=window_size).mean()
    cci = (typical_price - sma_tp) / (0.015 * mad_tp)

    return cci.tolist()


def keltner_channels(high_prices, low_prices, close_prices, window_size=20, multiplier=2):
    """
    Retorna as Bandas de Keltner para um conjunto de preços de alta, baixa e fechamento.

    :param high_prices: uma lista ou array com preços altos de um ativo financeiro.
    :param low_prices: uma lista ou array com preços baixos de um ativo financeiro.
    :param close_prices: uma lista ou array com preços de fechamento de um ativo financeiro.
    :param window_size: tamanho da janela deslizante para calcular a média móvel. Padrão é 20.
    :param multiplier: multiplicador para definir a largura das Bandas de Keltner. Padrão é 2.
    :return: uma tupla de três listas: (banda inferior, banda média, banda superior).
    """

    typical_price = [(high + low + close) / 3 for high, low, close in zip(high_prices, low_prices, close_prices)]

    atr = [0] * window_size
    for i in range(window_size, len(typical_price)):
        atr.append(max(high_prices[i] - low_prices[i], abs(high_prices[i] - close_prices[i - 1]),
                       abs(low_prices[i] - close_prices[i - 1])))
    atr = pd.Series(atr).rolling(window=window_size).mean().tolist()

    keltner_mid = pd.Series(typical_price).rolling(window=window_size).mean().tolist()
    keltner_upper = [(keltner_mid[i] + multiplier * atr[i]) for i in range(len(keltner_mid))]
    keltner_lower = [(keltner_mid[i] - multiplier * atr[i]) for i in range(len(keltner_mid))]

    return keltner_lower, keltner_mid, keltner_upper


def daily_range(open_prices, high_prices, low_prices, close_prices):
    """
    Retorna a variação diária para um conjunto de preços de abertura, alta, baixa e fechamento.

    :param open_prices: uma lista ou array com preços de abertura de um ativo financeiro.
    :param high_prices: uma lista ou array com preços altos de um ativo financeiro.
    :param low_prices: uma lista ou array com preços baixos de um ativo financeiro.
    :param close_prices: uma lista ou array com preços de fechamento de um ativo financeiro.
    :return: uma lista com os valores da variação diária.
    """

    daily_range = [high - low for high, low in zip(high_prices, low_prices)]

    return daily_range

if __name__ == "__main__":
    pass