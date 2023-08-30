import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import talib as tl

# Conectar à plataforma MetaTrader 5
if not mt5.initialize():
    print("Falha ao conectar à plataforma!")
    mt5.shutdown()
    
# Especificar o símbolo do contrato a ser negociado
ativo = "win$n".upper()
selected = mt5.symbol_select(ativo)
if selected:
    print('Ativo Já Existe ou foi Incluido')
if not selected:
    print('Ativo não encontrado')

periodo = mt5.TIMEFRAME_M15
contratos = 5
capital_inicial = 5000
stop_loss = 250
take_profit = 500
breakeven = 200

# Datas
data_start = 200
data0 = datetime.today() - timedelta(days=data_start)
data1 = datetime.today()

# Busca dos dados do ativo
ativo_data = mt5.copy_rates_range(ativo, periodo, data0, data1)
ativo_df = pd.DataFrame(ativo_data)
ativo_df["time"] = pd.to_datetime(ativo_df["time"], unit="s")
ativo_df.set_index("time", inplace=True)
ativo_df = ativo_df.rename(columns={'real_volume':'volume'})

