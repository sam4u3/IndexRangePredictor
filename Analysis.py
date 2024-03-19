import datetime

import pandas
from ydata_profiling import profile_report


class Analytics:
    def __init__(self, file_path, logger_ext):
        self.file_path = file_path
        if '.xlsx' in file_path:
            self.data = pandas.read_excel(file_path)
        if '.csv' in file_path:
            self.data = pandas.read_csv(file_path, encoding='utf8')

        self.logger = logger_ext
        self.logger.emit(self.data.head().to_string(index=False, col_space=4, show_dimensions=True))
        self.data.columns = [column.strip() for column in self.data.columns]
        self.data['Day'] = self.data['Date'].apply(self.get_day)
        self.data['Year'] = self.data['Date'].apply(self.get_year)
        self.data['Month'] = self.data['Date'].apply(self.get_month)
        self.data['YearMonth'] = self.data['Date'].apply(self.get_year_month)

    def get_day(self, date):
        return pandas.to_datetime(date).day

    def get_year(self, date):
        return pandas.to_datetime(date).year

    def get_month(self, date):
        return pandas.to_datetime(date).month

    def get_year_month(self, date):
        return pandas.to_datetime(date).strftime('%Y-%m')

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

    def get_gap_up_down(self, data):
        gap_data = data.copy()
        gap = []
        for index, row in gap_data.iterrows():
            day_of_week = pandas.to_datetime(row['Date']).day_of_week
            if day_of_week == 0:
                date_check = pandas.to_datetime(row['Date']) - datetime.timedelta(3)
            else:
                date_check = pandas.to_datetime(row['Date']) - datetime.timedelta(1)
            last_close = list(gap_data[pandas.to_datetime(gap_data['Date']) == pandas.to_datetime(date_check)]['Close'])

            if len(last_close) > 0:
                gap.append(row['Open'] - last_close[0])
            else:
                gap.append(0)
        gap_data['GAP'] = gap
        return gap_data

    def get_daily_range(self, quartiles):
        range_data = self.find_ranges(self.data, 'DAY')
        gap_data = self.get_gap_up_down(self.data)[['Date', 'GAP']]
        range_data_final = pandas.merge(range_data, gap_data, on='Date')
        profile = profile_report.ProfileReport(range_data_final)
        cols_to_calculate = [col for col in list(range_data_final.columns) if '_DAY' in col]
        results = []
        occurrences = []

        # Confidence interval
        for col in cols_to_calculate:
            day_std = range_data_final[col].std()

            day_confidence_interval_95 = 1.96 * day_std
            day_confidence_interval_99 = 2.576 * day_std
            day_confidence_interval_80 = 1.28 * day_std

            cob_out_80 = range_data_final[range_data_final[col] >= day_confidence_interval_80]
            cob_out_95 = range_data_final[range_data_final[col] >= day_confidence_interval_95]
            cob_out_99 = range_data_final[range_data_final[col] >= day_confidence_interval_99]
            cob_in_80 = range_data_final[range_data_final[col] < day_confidence_interval_80]
            cob_in_95 = range_data_final[range_data_final[col] < day_confidence_interval_95]
            cob_in_99 = range_data_final[range_data_final[col] < day_confidence_interval_99]

            result = {"PredictType": col,
                      "ConfidenceInterval-80": day_confidence_interval_80,
                      "ConfidenceInterval-95": day_confidence_interval_95,
                      "ConfidenceInterval-99": day_confidence_interval_99,
                      }

            occurrence = {"PredictType": col,
                          "TotalCount": len(range_data_final),
                          "COB-80-IN/OUT": f"{len(cob_in_80)}/{len(cob_out_80)}",
                          "COB-95-IN/OUT": f"{len(cob_in_95)}/{len(cob_out_95)}",
                          "COB-99-IN/OUT": f"{len(cob_in_99)}/{len(cob_out_99)}",

                          }
            occurrences.append(occurrence)

            import matplotlib.pyplot as plt
            plt.hist(range_data_final[col], bins=20, facecolor="blue", alpha=0.5)
            plt.savefig(f'./Data/Img/{col}.png')
            results.append(result)

        results = pandas.DataFrame(results).to_string(index=False, col_space=4, show_dimensions=True)
        occurrences = pandas.DataFrame(occurrences).to_string(index=False, col_space=4, show_dimensions=True)
        return results, occurrences

