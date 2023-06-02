import numpy as np
import pandas as pd
import MetaTrader5 as mt5
from datetime import datetime
import pytz
import time

# Conectar à plataforma MetaTrader 5
if not mt5.initialize():
    print("Falha ao conectar à plataforma!")
    mt5.shutdown()

# Especificar o símbolo do contrato a ser negociado
ativo = "PETR3"
stop_loss = 10
take_profit = 20
qt_contratos = float(100)


def compra(quantidade):
    print("ORDEM DE COMPRA ENVIADA")
    lot = float(100.0)
    symbol = ativo
    point = mt5.symbol_info(symbol).point
    print(point)
    price = mt5.symbol_info_tick(symbol).last
    print(price)
    deviation = 5
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": quantidade,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "sl": price - stop_loss * point,
        "tp": price + take_profit * point,
        "deviation": deviation,
        "magic": 23121987,
        "comment": "Ordem de Compra Enviada",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN
    }
    resultado = mt5.order_send(request)
    print(resultado)


compra(qt_contratos)