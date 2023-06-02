import pandas as pd
import MetaTrader5 as mt5
from datetime import datetime
import time

# Conectar à plataforma MetaTrader 5
if not mt5.initialize():
    print("Falha ao conectar à plataforma!")
    mt5.shutdown()

# Especificar o símbolo do contrato a ser negociado
symbol_buy = "petr3".upper()
symbol_sell = "petr4".upper()
selected = mt5.symbol_select(symbol_buy, symbol_sell)
if selected:
    print('Ativo Já Existe ou foi Incluido')
if not selected:
    print('Ativo não encontrado')

# Especificar preço de compra e venda do ativo
ask1 = mt5.symbol_info_tick(symbol_buy).ask
bid2 = mt5.symbol_info_tick(symbol_sell).bid
# print(ask1, bid2)

# Especificar os níveis de stop loss e take profit (em pontos)
stop_loss = -500
take_profit = 50

# Especificar o número de contratos a serem negociados
lot = float(5000.0)
lot_sell = lot


def position_get():
    position = mt5.positions_total()
    # print('Positions:', position)
    return position


def buy_order(symbol, lote):
    requests = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lote,
        "type": mt5.ORDER_TYPE_BUY,
        "price": ask1,
        "deviation": 0,
        "magic": 42525,
        "comment": "Python Arbitragem - Compra",
        "type_time": mt5.ORDER_TIME_DAY,
        "type_filling": mt5.ORDER_FILLING_RETURN
    }
    resultado_buy = mt5.order_send(requests)
    print(resultado_buy)


def sell_order(symbol, lote):
    requests = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lote,
        "type": mt5.ORDER_TYPE_SELL,
        "price": bid2,
        "deviation": 0,
        "magic": 42520,
        "comment": "Python Arbitragem - Venda",
        "type_time": mt5.ORDER_TIME_DAY,
        "type_filling": mt5.ORDER_FILLING_RETURN
    }
    resultado = mt5.order_send(requests)
    print(resultado)


def ordem_fechamento(ativo, quantidade, ticket, type_order, magic, deviation):
    if type_order == 0:
        print("ORDEM DE VENDA - FECHAMENTO")
        request_fechamento = {
            "action": mt5.TRADE_ACTION_DEAL,
            "position": ticket,
            "symbol": ativo,
            "volume": quantidade,
            "deviation": deviation,
            "magic": magic,
            "type": mt5.ORDER_TYPE_SELL,
            "price": mt5.symbol_info_tick(ativo).bid - 0.01,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN
        }

        resultado = mt5.order_send(request_fechamento)
        print(resultado)
    else:
        print("ORDEM DE COMPRA - FECHAMENTO")
        request_fechamento = {
            "action": mt5.TRADE_ACTION_DEAL,
            "position": ticket,
            "symbol": ativo,
            "volume": quantidade,
            "deviation": deviation,
            "magic": magic,
            "type": mt5.ORDER_TYPE_BUY,
            "price": mt5.symbol_info_tick(ativo).ask + 0.01,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN
        }

        resultado = mt5.order_send(request_fechamento)
        print(resultado)


def open_position():
    if 8 <= datetime.now().hour <= 16:
        if position_get() == 0:
            buy_order(symbol_buy, lot)
            print(lot)
            sell_order(symbol_sell, lot_sell)

            strategy()
        else:
            print('Você já tem posições abertas')
            strategy()
    else:
        print('Já Acabou o dia!')


def strategy():
    while True:
        time.sleep(0.5)
        info_posicoes = mt5.positions_get()
        data_posicoes = pd.DataFrame(list(info_posicoes), columns=info_posicoes[0]._asdict().keys())
        data_posicoes['time'] = pd.to_datetime(data_posicoes['time'], unit='s')
        data_posicoes['time_msc'] = pd.to_datetime(data_posicoes['time_msc'])
        data_posicoes['time_update'] = pd.to_datetime(data_posicoes['time_update'], unit='s')
        data_posicoes['time_update_msc'] = pd.to_datetime(data_posicoes['time_update_msc'])

        lucroAtivo01 = data_posicoes['profit'][0]
        lucroAtivo02 = data_posicoes['profit'][1]

        profit_total = lucroAtivo01 + lucroAtivo02
        # print(profit_total)
        if profit_total >= 0:
            print(f'Seu lucro é de {profit_total}')
        else:
            print(f'Seu prejuizo é de {profit_total}')

        if profit_total >= take_profit:

            print(ordem_fechamento(str(data_posicoes['symbol'][0]),
                                   float(data_posicoes['volume'][0]),
                                   int(data_posicoes['ticket'][0]),
                                   data_posicoes['type'][0],
                                   int(data_posicoes['magic'][0]),
                                   0))

            print(ordem_fechamento(str(data_posicoes['symbol'][1]),
                                   float(data_posicoes['volume'][1]),
                                   int(data_posicoes['ticket'][1]),
                                   data_posicoes['type'][1],
                                   int(data_posicoes['magic'][1]),
                                   0))
            break
        if profit_total <= stop_loss:
            print(ordem_fechamento(str(data_posicoes['symbol'][0]),
                                   float(data_posicoes['volume'][0]),
                                   int(data_posicoes['ticket'][0]),
                                   data_posicoes['type'][0],
                                   int(data_posicoes['magic'][0]),
                                   0))

            print(ordem_fechamento(str(data_posicoes['symbol'][1]),
                                   float(data_posicoes['volume'][1]),
                                   int(data_posicoes['ticket'][1]),
                                   data_posicoes['type'][1],
                                   int(data_posicoes['magic'][1]),
                                   0))
            break
        if datetime.now().hour >= 16:
            print('Fechando Posições Por Horario')
            print(ordem_fechamento(str(data_posicoes['symbol'][0]),
                                   float(data_posicoes['volume'][0]),
                                   int(data_posicoes['ticket'][0]),
                                   data_posicoes['type'][0],
                                   int(data_posicoes['magic'][0]),
                                   0))

            print(ordem_fechamento(str(data_posicoes['symbol'][1]),
                                   float(data_posicoes['volume'][1]),
                                   int(data_posicoes['ticket'][1]),
                                   data_posicoes['type'][1],
                                   int(data_posicoes['magic'][1]),
                                   0))
            break


if __name__ == "__main__":
    while True:
        open_position()
