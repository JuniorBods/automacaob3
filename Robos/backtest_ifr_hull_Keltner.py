import MetaTrader5 as mt5
from extrair_dados import buscahistorico
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import talib

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
data = buscahistorico(symbol_buy)
data = data.rename(columns={'open':'Open', 'high':'High', 'low':'Low', 'close':'Close', 'real_volume':'Volume'})

# print(data)

class RSI(Strategy):
    
    upper_bound = 70
    lower_bound = 30
    rsi_window = 14
    
    def init(self):
        self.rsi = self.I(talib.RSI, data['Close'], timeperiod= self.rsi_window)
    
    def next(self):
        if crossover(self.rsi, self.upper_bound):
            self.position.close()
            
        elif crossover(self.lower_bound, self.rsi):
            self.buy()

bt = Backtest(data, RSI, cash = 200000)

stats = bt.run()
print(stats)
bt.plot()