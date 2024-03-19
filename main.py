# Import Module
import os.path
from tkinter import *
from tkinter import filedialog as fd

from Analysis import Analytics
from extract_data import DataExtraction
from PIL import ImageTk, Image


class WidgetLogger():
    def __init__(self, widget):
        self.widget = widget
        self.widget.config(state='disabled')

    def emit(self, record):
        self.widget.config(state='normal')
        self.widget.insert(END, record + '\n')
        self.widget.see(END)
        self.widget.config(state='disabled')


class GUI:
    def __init__(self):
        self.root = Tk()
        self.root.title("Index Range Analysis")
        self.root.geometry('800x600')
        self.logger_widget = None

    def select_file(self, file_name_var):
        filetypes = (
            ('xlsx files', '*.xlsx'), ('csv files', '*.csv'),
            ('All files', '*.*')
        )
        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)

        file_name_var.set(filename)
        self.logger_widget.emit(f"File Selected : {filename}")

    def run_analysis(self, file_path, quartiles=90):
        self.logger_widget.emit(f"File : \n{file_path}\n")
        data_analysis = Analytics(file_path=file_path,
                                  logger_ext=self.logger_widget)
        result, occurrence = data_analysis.get_daily_range(quartiles)
        self.logger_widget.emit(f"Results \n{result}\n")
        self.logger_widget.emit(f"Occurrence \n{occurrence}")

        report = './Results/report_.txt'
        with open(report,'a+') as f:
            f.write(f'\n{file_path}\n\n')
            f.write(result)
            f.write(occurrence)

    def get_data(self, file_path, start_year, end_year, index, timeframe='1d'):
        data_extraction = DataExtraction()
        # file_path_excel = data_extraction.get_data(start_year, end_year, index, timeframe)
        file_path_excel = data_extraction.get_data_yf(start_year, end_year, index, timeframe)
        file_path.set(file_path_excel)

    def add_component(self):
        scrollbar = Scrollbar(self.root)
        text = Text(self.root, yscrollcommand=scrollbar.set, width=100)
        scrollbar.config(command=text.yview)
        self.logger_widget = WidgetLogger(text)

        header = Label(self.root, text="INDEX ANALYSIS", font=("Arial", 32))
        index_label = Label(self.root, text="CHOOSE INDEX : ", font=("Arial", 12))
        timeframe_label = Label(self.root, text="CHOOSE TIMEFRAME : ", font=("Arial", 12))
        filepath_label = Label(self.root, text="CHOOSE FILE : ", font=("Arial", 12))
        start_year = Label(self.root, text="START DATE : ", font=("Arial", 12))
        end_year = Label(self.root, text="END DATE : ", font=("Arial", 12))

        index_var = StringVar()
        timeframe_var = StringVar()
        file_name_var = StringVar()
        file_name_var.set("/Users/sayarmendis/Downloads/NIFTY 50_Historical.csv")
        start_date_var = StringVar()
        start_date_var.set("2022-01-01")
        end_date_var = StringVar()
        end_date_var.set('2023-12-31')
        options = [
            'BANKEX',
            'FINNIFTY',
            'BANKNIFTY',
            'NIFTY50',
            'SENSEX'
        ]
        timeframes = ['5m','15m', '1h', '1d', '5d', '1wk', '1mo', '3mo']

        index_var.set("NIFTY50")
        timeframe_var.set('1d')
        index_drop = OptionMenu(self.root, index_var, *options)
        timeframe_drop = OptionMenu(self.root, timeframe_var, *timeframes)

        file_select = Button(self.root, text='Select Index Data', command=lambda: self.select_file(file_name_var))
        entry_file_name = Entry(self.root, textvariable=file_name_var, font=("Arial", 12), width=50)
        start_year_entry = Entry(self.root, textvariable=start_date_var, font=("Arial", 12))
        end_year_entry = Entry(self.root, textvariable=end_date_var, font=("Arial", 12))

        header.grid(column=0, row=0, columnspan=6, rowspan=2)
        index_label.grid(column=0, row=5)
        index_drop.grid(column=1, row=5)
        timeframe_label.grid(column=2, row=5)
        timeframe_drop.grid(column=3, row=5)

        # file_select.grid(column=2, row=6)
        start_year.grid(column=0, row=6)
        start_year_entry.grid(column=1, row=6)
        end_year.grid(column=2, row=6)
        end_year_entry.grid(column=3, row=6)
        filepath_label.grid(column=0, row=7)
        entry_file_name.grid(column=1, row=7)

        Button(self.root, text="GET DATA", command=lambda: self.get_data(file_name_var,
                                                                         start_date_var.get(),
                                                                         end_date_var.get(),
                                                                         index_var.get(),
                                                                         timeframe_var.get())).grid(column=0, row=8,
                                                                                                columnspan=2)
        Button(self.root, text="GET RANGE", command=lambda: self.run_analysis(file_name_var.get(), )).grid(column=2,
                                                                                                           row=8,
                                                                                                           columnspan=2)

        text.grid(row=10, column=0,columnspan=6, padx=10, pady=10)
        scrollbar.grid(row=10, column=8)

    def run_app(self):
        self.add_component()
        self.root.mainloop()


if __name__ == '__main__':
    gui = GUI()
    gui.run_app()
