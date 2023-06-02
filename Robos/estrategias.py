def rsi_hull():
    # RSI
    rsi = ind.relative_strength_index(data.close, rsi_period)
    # rsi = rsi.dropna()
    print(f"IFR: {rsi[-1]:.2f}")
    print(mt5.symbol_info_tick(symbol_buy).last)

    # MEDIA MÓVEL
    media_hull = ind.hull_moving_average(data.close, media_curta_period)
    print(f"Media HULL:{media_hull[-1]:.0f}")

    if rsi[-1] >= 40 and data.close[-1] < media_hull[-1]:
        print(f"IFR Compra: {rsi[-1]:.2f}")
        return 1
    else:
        print('ainda nada1')
    if rsi[-1] >= 70 and data.close[-1] < media_hull[-1]:
        print(f"IFR Venda: {rsi[-1]:.2f}")
        return 0
    else:
        print('ainda nada2')
        

def max_min():

    if data.close[-1] < data.close[-2] and data.low[-1] < data.low[-2] and data.close[0] > data.open[-1]:
        print(f"IFR Compra: {rsi[-1]:.2f}")
        return 1
    else:
        print('ainda nada1')
    if data.close[-1] > data.close[-2] and data.high[-1] > data.high[-2] and data.close[0] < data.open[-1]:
        print(f"IFR Venda: {rsi[-1]:.2f}")
        return 0
    else:
        print('ainda nada2')