import datetime
import os.path
import traceback

import pandas
from bs4 import BeautifulSoup
from selenium.webdriver.common import by
from selenium.webdriver.common.by import By

from Analysis import Analytics
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import yfinance as yf

class DataExtraction:
    def __init__(self):
        self.urls = {
            'BANKEX': 'https://in.investing.com/indices/s-p-bse-bankex-historical-data',
            'FINNIFTY': 'https://in.investing.com/indices/cnx-finance-historical-data',
            'BANKNIFTY': 'https://in.investing.com/indices/bank-nifty-historical-data',
            'NIFTY50': 'https://in.investing.com/indices/s-p-cnx-nifty-historical-data',
            'SENSEX': 'https://in.investing.com/indices/sensex-historical-data'
        }
        self.yf = {
            'BANKEX': 'BSE-BANK.BO',
            'FINNIFTY': 'NIFTY_FIN_SERVICE.NS',
            'BANKNIFTY': '%5ENSEBANK',
            'NIFTY50': '%5ENSEI',
            'SENSEX': '%5EBSESN'
        }
        # self.driver_path = ChromeDriverManager().install()
        # self.driver = webdriver.Chrome()

    def get_data(self, start_date, end_date, index, timeframe):
        try:
            if timeframe == 'Daily':
                self.driver.get(self.urls.get(index, None))
            if timeframe == 'Weekly':
                self.driver.get(self.urls.get(index, None) + '?interval_sec=weekly')
            if timeframe == 'Monthly':
                self.driver.get(self.urls.get(index, None) + '?interval_sec=monthly')
            self.driver.fullscreen_window()
            self.driver.find_element(By.XPATH, '//button[@class="js-dropdown-display select"]').click()
            from_date = self.driver.find_element(By.XPATH, '//input[@class="select js-date-from"]')
            from_date.clear()
            from_date.send_keys(pandas.to_datetime(start_date).strftime('%m/%d/%Y'))
            to_date = self.driver.find_element(By.XPATH, '//input[@class="select js-date-to"]')
            to_date.clear()
            to_date.send_keys(pandas.to_datetime(end_date).strftime('%m/%d/%Y'))
            self.driver.find_element(By.XPATH, '//button[@class="js-apply-button common-button"]').click()
            # self.driver.find_element(By.XPATH,f'//li[@data-time-frame="{timeframe.lower()}"]').click()
            self.driver.implicitly_wait(5)
            data = self.extract_data(self.driver.page_source)
            file_path = os.path.abspath(f'./Data/{index}_{timeframe}.xlsx')
            data.to_excel(file_path, index=False)
            return file_path
        except:
            print(traceback.format_exc())
        finally:
            self.driver.close()
            self.driver.quit()

    def extract_data(self, content):
        bs4 = BeautifulSoup(content, features="html.parser")
        table = bs4.find('table').find('tbody')

        columns = ['Date', 'Close', 'Open', 'High', 'Low', 'Volume', 'Change']
        data = []

        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            vals = []
            for col in cols:
                vals.append(col.text.replace('\n', ''))

            row_data = dict(zip(columns, vals))
            data.append(row_data)

        df = pandas.DataFrame(data)

        for col in columns:
            if col == 'Date':
                df['Date'] = pandas.to_datetime(df['Date']).dt.date
            if col in ['Close', 'Open', 'High', 'Low', 'Volume']:
                df[col] = df[col].str.replace(',', '')

        return df

    def get_data_yf(self,start_date,end_date,index,timeframe):
        index_ticker = self.yf.get(index)
        data = yf.download(index_ticker, start=start_date, end=end_date, interval=timeframe)
        file_name = os.path.abspath(f'./data/{index}_{timeframe}_{start_date}_{end_date}.xlsx')
        data.to_excel(file_name)
        return file_name
