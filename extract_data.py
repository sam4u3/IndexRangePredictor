import pandas
from bs4 import BeautifulSoup

from Analysis import Analytics

# Nifty_Weekly.xlsx
# https://in.investing.com/indices/s-p-cnx-nifty-historical-data?end_date=1706293800&interval_sec=weekly&st_date=1264530600



if __name__ == '__main__':
    content = ''

    with open('niftyweekly.html') as file:
        content=file.read()

    bs4 = BeautifulSoup(content)
    table = bs4.find('table').find('tbody')

    columns = ['Date','Close','Open','High','Low','Volume','Change']
    data = []

    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        vals = []
        for col in cols:
            vals.append(col.text.replace('\n',''))

        row_data = dict(zip(columns, vals))
        data.append(row_data)

    df = pandas.DataFrame(data)

    for col in columns:
        if col == 'Date':
            df['Date'] = pandas.to_datetime(df['Date'])
        if col in ['Close','Open','High','Low','Volume']:
            df[col] = df[col].str.replace(',','')


    df.to_excel('Nifty_Weekly.xlsx',index=False)
    # ans = Analytics('Nifty_Weekly.xlsx',start_year=2014,end_year=2023,'NIFTY',)
