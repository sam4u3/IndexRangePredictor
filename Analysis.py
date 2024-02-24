import pandas


class Analytics:
    def __init__(self, file_path, start_year, end_year, logger_ext):
        self.file_path = file_path
        if '.xlsx' in file_path:
            self.data = pandas.read_excel(file_path)
        if '.csv' in file_path:
            self.data = pandas.read_csv(file_path)
        self.logger = logger_ext
        self.data['Day'] = self.data['Date'].apply(self.get_day)
        self.data['Year'] = self.data['Date'].apply(self.get_year)
        self.data['Month'] = self.data['Date'].apply(self.get_month)
        self.data['YearMonth'] = self.data['Date'].apply(self.get_year_month)
        self.date_filter_data = self.get_date_filter_data(start_year, end_year)

    def get_day(self, date):
        return pandas.to_datetime(date).day

    def get_year(self, date):
        return pandas.to_datetime(date).year

    def get_month(self, date):
        return pandas.to_datetime(date).month

    def get_year_month(self, date):
        return pandas.to_datetime(date).strftime('%Y-%m')

    def get_date_filter_data(self, start_year, end_year):
        self.logger.emit(f"Data Found : {self.data.shape}")
        self.logger.emit(f"Data Year Range  : {self.data['Year'].min()} -  {self.data['Year'].max()}")
        filter_data = self.data.loc[(self.data['Year'] >= int(start_year)) & (self.data['Year'] <= int(end_year))]
        self.logger.emit(f"Filter Data for Year {start_year} - {end_year} : {filter_data.shape}")
        return filter_data

    def find_ranges(self, data, range_type='DAY'):
        range_df = data.copy()
        cols = ["Date", "Open", "High", "Low", "Close"]
        range_df = range_df[cols]

        range_df[f'OPEN-HIGH_{range_type}'] = (range_df['Open'] - range_df['High']).abs()
        range_df[f'OPEN-LOW_{range_type}'] = (range_df['Open'] - range_df['Low']).abs()
        range_df[f'CLOSE-HIGH_{range_type}'] = (range_df['Close'] - range_df['High']).abs()
        range_df[f'CLOSE-LOW_{range_type}'] = (range_df['Close'] - range_df['Low']).abs()
        range_df[f'HIGH-LOW_{range_type}'] = (range_df['High'] - range_df['Low']).abs()
        range_df[f'OPEN-CLOSE_{range_type}'] = (range_df['Open'] - range_df['Close']).abs()
        return range_df

    def get_daily_range(self, quartiles):
        range_data = self.find_ranges(self.date_filter_data, 'DAY')
        cols_to_calculate = [col for col in list(range_data.columns) if '_DAY' in col]
        results = []

        for col in cols_to_calculate:
            day_quartiles = range_data[col].quantile(quartiles / 100)
            day_std = range_data[col].std()
            day_confidence_interval = 1.96 * day_std

            result = {"PredictType": col,
                      f"Quartile {quartiles}": day_quartiles,
                      "Standard Dev": day_std,
                      "Confidence Interval": day_confidence_interval}

            results.append(result)

        results = pandas.DataFrame(results).to_string(index=None)
        return results

    def monthly_range_analysis(self):
        pass
        # data_monthly = data.groupby('yearmonth').agg(min_month=pandas.NamedAgg(column="Low", aggfunc="min"),
        #                                          max_month=pandas.NamedAgg(column="High", aggfunc="max"))