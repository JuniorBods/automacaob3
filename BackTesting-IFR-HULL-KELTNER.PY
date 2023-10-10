import pandas as pd
import numpy as np
import vectorbt as vbt
import talib

# Load your data into a DataFrame
data = pd.read_csv(r'BackTesting\WINQ23-200dias-5min.csv')

# Buy in Hold
# pf = vbt.Portfolio.from_holding(data.close, init_cash=5000)
# buyinhold = pf.total_profit()
# print(buyinhold)

# Define the period range
windows = np.arange(5, 31, 5)
fast_ma, slow_ma = vbt.MA.run_combs(data.close, window=windows, r=2, short_names=['fast', 'slow'])
entries = fast_ma.ma_crossed_above(slow_ma)
exits = fast_ma.ma_crossed_below(slow_ma)

pf_kwargs = dict(size=1, fees=0.005, freq='5t')
pf = vbt.Portfolio.from_signals(data.close, entries, exits, **pf_kwargs, init_cash=5000)

fig = pf.returns_stats()
print(fig)