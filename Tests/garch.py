from datetime import datetime, timedelta
from time import time

import pandas
import matplotlib.pyplot as plt
import statsmodels.tsa.arima_model
from arch import arch_model
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

import numpy as np
import yfinance as yf
import statsmodels.api as sm


def predict_vol():

    # to download online data for nifty

    # data = yf.download('%5ENSEI', start='2014-01-01', end=datetime.now().strftime('%Y-%m-%d'))
    # data.to_excel('./Data/NIFTYYF.xlsx')
    data = pandas.read_excel('./Data/NIFTYYF.xlsx')
    data.index = pandas.to_datetime(data['Date'])
    returns = 100 * data.Close.pct_change().dropna()

    plt.figure(figsize=(10, 4))
    plt.plot(returns)
    plt.ylabel('Pct Return', fontsize=16)
    plt.title('DIS Returns', fontsize=20)

    plot_acf(returns**2)
    plot_pacf(returns**2)
    plt.show()

    model = arch_model(returns,p=16,q=12)
    model_fit = model.fit()
    print(model_fit.summary())

    rolling_predictions = []
    test_size = 30

    for i in range(test_size):
        train = returns[:-(test_size - i)]
        model = arch_model(train, p=16, q=12)
        model_fit = model.fit(disp='off')
        pred = model_fit.forecast(horizon=1)
        rolling_predictions.append(np.sqrt(pred.variance.values[-1, :][0]))

    rolling_predictions = pandas.Series(rolling_predictions, index=returns.index[-30:])

    plt.figure(figsize=(10, 4))
    true, = plt.plot(returns[-365:])
    preds, = plt.plot(rolling_predictions)
    plt.title('Volatility Prediction - Rolling Forecast', fontsize=20)
    plt.legend(['True Returns', 'Predicted Volatility'], fontsize=16)
    plt.show()


if __name__ == '__main__':
    predict_vol()