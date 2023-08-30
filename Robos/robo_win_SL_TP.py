import pandas as pd
import MetaTrader5 as mt5
from datetime import datetime
import time
from datetime import datetime, timedelta
import pandas as pd
# from extrair_dados import buscahistorico
import indicadores_modulo as ind


# Conectar à plataforma MetaTrader 5
if not mt5.initialize():
    print("Falha ao conectar à plataforma!")
    mt5.shutdown()

# Especificar o símbolo do contrato a ser negociado
symbol_buy = "winq23".upper()
selected = mt5.symbol_select(symbol_buy)
if selected:
    print('Ativo Já Existe ou foi Incluido')
if not selected:
    print('Ativo não encontrado')

# Especificar o número base de pontos do ativo
point1 = mt5.symbol_info(symbol_buy).point

# Especificar preço de compra e venda do ativo
ask1 = mt5.symbol_info_tick(symbol_buy).ask
bid1 = mt5.symbol_info_tick(symbol_buy).bid

# Especificar os níveis de stop loss e take profit (em pontos)
stop_loss = 100
take_profit = 100
print(f'StopLoss: {stop_loss}', f'TakeProfit: {take_profit}')

# Especificar o número de contratos a serem negociados
lote = 5
lot = float(lote)
lot_sell = lot

# Periodo do RSI e das Medias Móveis
rsi_period = 14
media_curta_period = 9



def position_get():
    position = mt5.positions_total()
    # print('Positions:', position)
    return position


def buy_order(symbol, lote):
    price = mt5.symbol_info_tick(symbol).last
    ponto = mt5.symbol_info(symbol).point
    requests = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lote,
        "type": mt5.ORDER_TYPE_BUY,
        "price": ask1,
        "sl": price - stop_loss,
        "tp": price + take_profit,
        "deviation": 0,
        "magic": 42525,
        "comment": "Python Win - Compra",
        "type_time": mt5.ORDER_TIME_DAY,
        "type_filling": mt5.ORDER_FILLING_RETURN
    }
    resultado_buy = mt5.order_send(requests)
    print(resultado_buy)


def sell_order(symbol, lote):
    price = mt5.symbol_info_tick(symbol).last
    ponto = mt5.symbol_info(symbol).point
    requests = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lote,
        "type": mt5.ORDER_TYPE_SELL,
        "price": bid1,
        "sl": price + stop_loss,
        "tp": price - take_profit,
        "deviation": 0,
        "magic": 42520,
        "comment": "Python Win - Venda",
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
            "price": mt5.symbol_info_tick(ativo).bid,
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
            "price": mt5.symbol_info_tick(ativo).ask,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN
        }

        resultado = mt5.order_send(request_fechamento)
        print(resultado)


def buscahistorico(ativos):
    tipo = 1
    data_start = 50
    data0 = datetime.today() - timedelta(days=data_start)
    data1 = datetime.today()
    if tipo == 1:
        # dados das barras OHLC
        # tempo_grafico = int(input("Qual o tempo grafico?"))
        tempo_grafico = 1
        if tempo_grafico == 1:
            tempo = mt5.TIMEFRAME_M1
        elif tempo_grafico == 5:
            tempo = mt5.TIMEFRAME_M5
        elif tempo_grafico == 10:
            tempo = mt5.TIMEFRAME_M10
        elif tempo_grafico == 60:
            tempo = mt5.TIMEFRAME_H1
        elif tempo_grafico == 24:
            tempo = mt5.TIMEFRAME_D1
        ativos = ativos.split(",")
        for ativo in ativos:
            ticks = mt5.copy_rates_range(ativo, tempo, data0, data1)
            data_ticks = pd.DataFrame(ticks)
            data_ticks['time'] = pd.to_datetime(data_ticks['time'], utc=True, unit='s')
            data_ticks.set_index('time', inplace=True)
            return data_ticks
        
        
def indicadores():
    # Buscar os dados do ativo
    data = buscahistorico(symbol_buy)
    if data.high[-3] > data.high[-4]:
    # if data.high[-3] < data.high[-4] and data.low[-3] < data.low[-4] and data.close[-2] > data.open[-3]:
        print(f"Compra: {data.close[-1]}")
        return 1

    elif data.low[-3] < data.low[-4]:
    # elif data.low[-3] > data.low[-4] and data.high[-3] > data.high[-4] and data.close[-2] < data.open[-3]:
        print(f"Venda: {data.close[-1]}")
        return 0
    else:
        pass


def open_position():
    if 8 <= datetime.now().hour <= 18:
        if indicadores() == 1:
            print(indicadores)
            buy_order(symbol_buy, lot)
            print('ORDEM DE COMPRA ABERTA')
            strategy()
        elif indicadores() == 0:
            sell_order(symbol_buy, lot_sell)
            print('ORDEM DE VENDA ABERTA')
            strategy()
    else:
        print('Já Acabou o dia!')


def strategy():
    while True:
        time.sleep(0.5)
        if position_get() >= 1:
            info_posicoes = mt5.positions_get()
            data_posicoes = pd.DataFrame(list(info_posicoes), columns=info_posicoes[0]._asdict().keys())
            data_posicoes['time'] = pd.to_datetime(data_posicoes['time'], unit='s')
            data_posicoes['time_msc'] = pd.to_datetime(data_posicoes['time_msc'])
            data_posicoes['time_update'] = pd.to_datetime(data_posicoes['time_update'], unit='s')
            data_posicoes['time_update_msc'] = pd.to_datetime(data_posicoes['time_update_msc'])

            for index, value in enumerate(data_posicoes['symbol']):
                # print(value)
                if value == symbol_buy:
                    lucroAtivo01 = data_posicoes['profit'][index]
                    print(lucroAtivo01)
            
            profit_total = lucroAtivo01
            # print(profit_total)
            if profit_total >= 0:
                print(f'Seu lucro é de {profit_total}')
            else:
                print(f'Seu prejuizo é de {profit_total}')
            
            if datetime.now().hour > 16:
                print('Fechando Posições Por Horario')
                print(ordem_fechamento(str(data_posicoes['symbol'][0]),
                                       float(data_posicoes['volume'][0]),
                                       int(data_posicoes['ticket'][0]),
                                       data_posicoes['type'][0],
                                       int(data_posicoes['magic'][0]),
                                       0))
        else:
            print('Não tem posições abertas')
            break
        
# aguarda 250 pontos de ganho para mover o stoploss para breakeven
# def Breakeven():
#     while True:
#         position = mt5.positions_get(symbol=symbol)[0]
#         if position.profit > 50 * mt5.symbol_info(symbol).point:
#             request = {
#                 "action": mt5.TRADE_ACTION_SLTP,
#                 "symbol": symbol,
#                 "type": mt5.ORDER_TYPE_BUY,
#                 "position": position.ticket,
#                 "sl": position.open_price,
#                 "price": position.open_price,
#                 "magic": magic_number,
#                 "deviation": deviation
#             }
#             result = mt5.order_send(request)
#             if result.retcode != mt5.TRADE_RETCODE_DONE:
#                 print("order_send failed, retcode =", result.retcode)
#                 print("result", result)
#             else:
#                 print("order_send done, ", result)
#             break

# # define o stopmóvel com passo de 50 pontos
# def stopmove():
#     while True:
#         position = mt5.positions_get(symbol=symbol)[0]
#         if position.profit > 50 * mt5.symbol_info(symbol).point:
#             sl = position.open_price + 50 * mt5.symbol_info(symbol).point
#             request = {
#                 "action": mt5.TRADE_ACTION_SLTP,
#                 "symbol": symbol,
#                 "type": mt5.ORDER_TYPE_BUY,
#                 "position": position.ticket,
#                 "sl": sl,
#                 "price": position.open_price,
#                 "magic": magic_number,
#                 "deviation": deviation
#             }
#             result = mt5.order_send(request)
#             if result.retcode != mt5.TRADE_RETCODE_DONE:
#                 print("order_send failed, retcode =", result.retcode)
#                 print("result", result)
#             else:
#                 print("order_send done, ", result)
#         mt5.sleep(1000) # aguarda 1 segundo antes de verificar novamente



if __name__ == "__main__":
    while True:
        time.sleep(2)
        open_position()
