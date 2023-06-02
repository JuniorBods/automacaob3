import MetaTrader5 as mt5
import time

# conecta-se ao terminal MetaTrader 5
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# define os parâmetros da ordem de compra
symbol = "WINM23"
action = mt5.TRADE_ACTION_DEAL
volume = 5.0
price = mt5.symbol_info_tick(symbol).ask
sl = price - 250 * mt5.symbol_info(symbol).point
tp = price + 500 * mt5.symbol_info(symbol).point
deviation = 10
magic_number = 123456

# envia a ordem de compra
request = {
    "action": action,
    "symbol": symbol,
    "volume": volume,
    "type": mt5.ORDER_TYPE_BUY,
    "price": price,
    "sl": sl,
    "tp": tp,
    "deviation": deviation,
    "magic": magic_number,
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_IOC,
    "comment": "Breakeven",
    "position": 0
}

result = mt5.order_send(request)

if result.retcode != mt5.TRADE_RETCODE_DONE:
    print("order_send failed, retcode =", result.retcode)
    print("result", result)
else:
    print("order_send done, ", result)
    
# aguarda 250 pontos de ganho para mover o stoploss para breakeven
while True:
    
    position = mt5.positions_get(symbol=symbol)[0]
    if position.profit > 50 * mt5.symbol_info(symbol).point:
        request = {
            "action": mt5.TRADE_ACTION_SLTP,
            "symbol": symbol,
            "type": mt5.ORDER_TYPE_BUY,
            "position": position.ticket,
            "sl": position.price_open,
            "price": position.price_open,
            "magic": magic_number,
            "deviation": deviation
        }
        result = mt5.order_send(request)

        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print("order_send failed, retcode =", result.retcode)
            print("result", result)
        else:
            print("order_send done, ", result)
        break
    # calcula e imprime o resultado financeiro da operação
    price = mt5.symbol_info_tick(symbol).bid
    profit = position.profit if position.type == mt5.ORDER_TYPE_BUY else -position.profit
    print(profit)
    time.sleep(2) # aguarda 10 segundo antes de verificar novamente

# define o stopmóvel com passo de 50 pontos
while True:
    position = mt5.positions_get(symbol=symbol)[0]
    if position.profit > 50 * mt5.symbol_info(symbol).point:
        sl = position.price_open + 50 * mt5.symbol_info(symbol).point
        request = {
            "action": mt5.TRADE_ACTION_SLTP,
            "symbol": symbol,
            "type": mt5.ORDER_TYPE_BUY,
            "position": position.ticket,
            "sl": sl,
            "price": position.price_open,
            "magic": magic_number,
            "deviation": deviation
        }
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print("order_send failed, retcode =", result.retcode)
            print("result", result)
        else:
            print("order_send done, ", result)

    time.sleep(2) # aguarda 10 segundo antes de verificar novamente

