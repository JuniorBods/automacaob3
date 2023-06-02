import pandas as pd
import numpy as np
import backtrader as bt
import MetaTrader5 as mt5
from backtrader import indicators
from datetime import datetime, timedelta

class MyStrategy(bt.Strategy):
    params = (
        ('initial_capital', 10000.0),
        ('stop_loss', 250),  # 2% stop loss
        ('stop_gain', 500),  # 5% stop gain
        ('breakeven', 250),  # 2% breakeven
        ('stop_movel', 100), # 1% stop móvel
        ('cci_period', 14),
        ('keltner_period', 20),
        ('keltner_dev', 2),
        ('ifr_period', 14),
        ('cci_level', 50),
        ('ifr_level_low', 30),
        ('ifr_level_high', 70)
    )

    def __init__(self):
        self.data_close = self.datas[0].close
        self.data_high = self.datas[0].high
        self.data_low = self.datas[0].low
        self.data_volume = self.datas[0].volume
        print('init')

        self.ifr = bt.indicators.StochasticFull(self.data_high, self.data_low, self.data_close, period=self.params.ifr_period)
        self.keltner = indicators.KeltnerChannels(self.data_high, self.data_low, self.data_close, period=self.params.keltner_period, devfactor=self.params.keltner_dev)
        self.cci = indicators.CommodityChannelIndex(self.data_high, self.data_low, self.data_close, period=self.params.cci_period)

        self.order = None
        self.price = None
        self.comm = None

    def next(self):
        print('next')
        if self.order:
            return

        if self.ifr.lines.percK[0] < self.params.ifr_level_low and self.cci.lines.cci[0] < self.params.cci_level and self.data_close[0] < self.keltner.lines.bot[0]: 
            self.order = self.buy()
            self.price = self.data_close[0]
        elif self.ifr.lines.percK[0] > self.params.ifr_level_high and self.cci.lines.cci[0] > self.params.cci_level and self.data_close[0] > self.keltner.lines.top[0]:
            self.order = self.sell()
            self.price = self.data_close[0]

        if self.order:
            self.comm = abs(self.position.size) * self.params.comm_info[0]
            self.log('Open %s position: Size %s, Price %s' %
                     ('Buy' if self.position.size > 0 else 'Sell', abs(self.position.size), self.price))

        if self.position.size > 0:
            if self.data_close[0] - self.params.breakeven > self.price:
                self.sell(exectype=bt.Order.Stop, price=self.price + self.params.breakeven, transmit=True)
            elif self.data_close[0] - self.params.stop_gain > self.price:
                self.sell(exectype=bt.Order.Limit, price=self.price + self.params.stop_gain, transmit=True)
            elif self.data_close[0] + self.params.stop_loss < self.price:
                self.sell(exectype=bt.Order.Stop, price=self.price - self.params.stop_loss, transmit=True)
            elif self.data_close[0] - self.params.stop_movel > self.price:
                self.sell(exectype=bt.Order.StopTrail, trailpercent=self.params.stop_movel, transmit=True)

def stop(self):
    pnl = round(self.broker.getvalue() - self.params.initial_capital, 2)
    self.log('Ending Value {:.2f}'.format(self.broker.getvalue()))
    self.log('Profit/Loss {:.2f}'.format(pnl))
    df = pd.readcsv('WINM23-200dias-5min.csv', indexcol='datetime', parse_dates=True)
 
    cerebro = bt.Cerebro()
    cerebro.addstrategy(MyStrategy)
    data_feed = bt.feeds.PandasData(dataname=df)
    cerebro.adddata(data_feed)
    cerebro.broker.setcash(10000.0)
    cerebro.addsizer(bt.sizers.FixedSize, stake=1000)
    cerebro.broker.setcommission(commission=0.0)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    mt5.shutdown()
    
    if __name__ == '__main__':
        next()