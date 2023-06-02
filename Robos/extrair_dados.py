import MetaTrader5 as mt5
from datetime import datetime, timedelta
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

# connect to Metatrader 5
if not mt5.initialize():
    print("initializa() faliled")
    mt5.shutdown()


def buscahistorico(ativos):
    # ativos = input("Quais ativos você gostaria de puxar os dados? Separados por , :").upper()
    # tipo = int(input('Gostaria de puxar OHLC(1) ou BID-ASk(2)? Digite 1 ou 2.'))
    data_start = int(input("Quanto tempo você gostaria do historico?(Em dias)"))
    tipo = 1
    # data_start = 50
    data0 = datetime.today() - timedelta(days=data_start)
    data1 = datetime.today()
    if tipo == 1:
        # dados das barras OHLC
        tempo_grafico = int(input("Qual o tempo grafico?"))
        # tempo_grafico = 5
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
            # print(ativo)
            ticks = mt5.copy_rates_range(ativo, tempo, data0, data1)
            data_ticks = pd.DataFrame(ticks)
            data_ticks['time'] = pd.to_datetime(data_ticks['time'], utc=True, unit='s')
            data_ticks.set_index('time', inplace=True)
            data_ticks.to_csv(f"{ativo}-{data_start}dias-{tempo_grafico}min.csv")
            # print(data_ticks)
            # table = pa.Table.from_pandas(data_ticks)
            # writer = pq.ParquetWriter(f"{ativo}-{data_start}dias-{tempo_grafico}min.parquet", table.schema)
            # writer.write_table(table)
            # writer.close()
            return data_ticks

    elif tipo == 2:
        # dados dos ticks BID/ASK
        for ativo in ativos:
            ticks = mt5.copy_ticks_range(ativo, data0, data1, mt5.COPY_TICKS_TRADE)
            data_ticks = pd.DataFrame(ticks)
            data_ticks['time'] = pd.to_datetime(data_ticks['time'], utc=True, unit='s')
            data_ticks.set_index('time', inplace=True)
            # print(data_ticks)

            # função para achar as flags de agressão
            def buy_or_sell(flag):
                if (flag & 32) and (flag & 64):
                    return 'Ambos'
                elif flag & 32:
                    return 'Compra'
                elif flag & 64:
                    return 'Venda'

            data_ticks["flags"] = data_ticks["flags"].apply(buy_or_sell)
            table = pa.Table.from_pandas(data_ticks)
            # writer = pq.ParquetWriter(f"{ativo}-{data_start}dias-ticker.parquet", table.schema)

            # writer.write_table(table)
            # writer.close()
            return data_ticks


if __name__ == "__main__":
    buscahistorico('WINM23')
