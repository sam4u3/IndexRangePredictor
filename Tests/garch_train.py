from datetime import datetime, timedelta
import pandas
import matplotlib.pyplot as plt
from arch import arch_model
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import numpy as np
import yfinance as yf


def predict_vol(days=7):
    data = yf.download('%5ENSEI', start='2014-01-01', end=datetime.now().strftime('%Y-%m-%d'))
    data = pandas.read_excel('./Data/NIFTYYF.xlsx')
    data.index = pandas.to_datetime(data['Date'])
    returns = 100 * data.Close.pct_change().dropna()

    model = arch_model(returns,p=16,q=12)
    model_fit = model.fit(disp='off')
    pred = model_fit.forecast(horizon=days)
    future_dates = [returns.index[-1] + timedelta(days=i) for i in range(1, days+1)]
    pred = pandas.Series(np.sqrt(pred.variance.values[-1, :]), index=future_dates)

    plt.figure(figsize=(10, 4))
    plt.plot(pred)
    plt.title('Volatility Prediction - Next 9 Days', fontsize=20)

    plt.show()


if __name__ == '__main__':
    start_date = '2014-01-01'
    end_date = datetime.now().strftime('%Y-%m-%d')
    predict_vol(7)