import MetaTrader5 as mt5
import Robos.indicadores_modulo as ind
from extrair_dados import buscahistorico
import pyarrow.parquet as pq
from tkinter import filedialog
import plotly.graph_objects as go

# Conectar à plataforma MetaTrader 5
if not mt5.initialize():
    print("Falha ao conectar à plataforma!")
    mt5.shutdown()
# Especificar o símbolo do contrato a ser negociado
symbol_buy = "win$n".upper()
selected = mt5.symbol_select(symbol_buy)
if selected:
    print('Ativo Já Existe ou foi Incluido')
if not selected:
    print('Ativo não encontrado')

# Busca Historico do ativo
historico_ativo = input('Você ja tem um historico? Sim(S) ou Não(N)').upper()
if historico_ativo == 'S':
    arquivo = filedialog.askopenfilename()
    data = pq.ParquetFile(f"{arquivo}").read().to_pandas()
    # print(data)
if historico_ativo == 'N':
    data = buscahistorico(symbol_buy)

# Indicadores
IFR = ind.relative_strength_index(data.close, 20)
data['IFR'] = IFR
HMA = ind.hull_moving_average(data.close, 20)
data['HMA'] = HMA
KELTNER = ind.keltner_channels(data.high, data.low, data.close, 20)
data['KELTNER_INF'] = KELTNER[0]
data['KELTNER_MED'] = KELTNER[1]
data['KELTNER_SUP'] = KELTNER[2]
data = data.dropna()

# Sinal de Compra
previous_HMA = data['HMA'].shift(1)
previous_IFR = data['IFR'].shift(1)
previous_close = data['close'].shift(1)
# data['buy'] = previous_close < previous_HMA
data['buy'] = data['close'] > data['HMA']
data['buy'] &= previous_IFR < 30
data['buy'] &= data['IFR'] > 30
data['buy'] &= data['close'] < data['KELTNER_INF']
print(data)

# fig = go.Figure(go.Candlestick(name='WIN', x=data.index, open=data.open, high=data.high,
#                                 low=data.low, close=data.close))
# fig.add_trace(go.Bar(name='IFR', x=data.index, y=data['IFR']))
# fig.add_trace(go.Scatter(name='HMA', x=data.index, y=data['HMA']))
# fig.add_trace(go.Scatter(name='KELTNER_INF', x=data.index, y=data['KELTNER_INF']))
# fig.add_trace(go.Scatter(name='KELTNER_MED', x=data.index, y=data['KELTNER_MED']))
# fig.add_trace(go.Scatter(name='KELTNER_SUP', x=data.index, y=data['KELTNER_SUP']))
# fig.update_layout(title='WIN', xaxis_rangeslider_visible=False, margin=dict(l=120, r=20, t=20, b=20),
#                   template= 'simple_white', width=1200, height=600,)
# fig.show()