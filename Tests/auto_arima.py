import yfinance as yf
import pmdarima as pm
import pandas
from datetime import datetime

def predict_vol(days=7):
    # data = yf.download('%5ENSEI', start='2014-01-01', end=datetime.now().strftime('%Y-%m-%d'))
    data = pandas.read_excel('./Data/NIFTYYF.xlsx')
    data.index = pandas.to_datetime(data['Date'])

    resulst = pm.auto_arima(data.Close,d=0,start_p=0,start_q=0,max_p=6,max_q=6,seasonal=True,m=12,D=4,start_P=1,start_Q=1,
                           max_P=6,max_Q=6,information_criterion='aic',trace=True,stepwise=True)

    print(resulst)



if __name__ == '__main__':
    start_date = '2014-01-01'
    end_date = datetime.now().strftime('%Y-%m-%d')
    predict_vol(7)