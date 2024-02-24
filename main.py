# Import Module
from tkinter import *
from tkinter import filedialog as fd

from Analysis import Analytics


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
        self.root.geometry('600x600')
        self.logger_widget = None

    def select_file(self, file_name_var):
        filetypes = (
            ('xlsx files', '*.xlsx'),('csv files', '*.csv'),
            ('All files', '*.*')
        )
        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)

        file_name_var.set(filename)
        self.logger_widget.emit(f"File Selected : {filename}")


    def run_analysis(self, file_path,start_year,end_year, quartiles=80):
        data_analysis = Analytics(file_path=file_path,start_year=start_year,end_year=end_year,logger_ext=self.logger_widget)
        result = data_analysis.get_daily_range(quartiles)
        self.logger_widget.emit(f"Results \n{result}")

    def add_component(self):
        scrollbar = Scrollbar(self.root)
        text = Text(self.root, yscrollcommand=scrollbar.set)
        scrollbar.config(command=text.yview)
        self.logger_widget = WidgetLogger(text)

        header=Label(self.root, text="INDEX ANALYSIS", font=("Arial", 32))
        index_label = Label(self.root, text="CHOOSE INDEX : ", font=("Arial", 12))
        filepath_label = Label(self.root, text="CHOOSE FILE : ", font=("Arial", 12))
        start_year = Label(self.root, text="START YEAR : ", font=("Arial", 12))
        end_year = Label(self.root, text="END YEAR : ", font=("Arial", 12))

        index_var = StringVar()
        file_name_var = StringVar()
        file_name_var.set("/Users/sayarmendis/Downloads/NIFTY 50_Historical.csv")
        start_year_var = StringVar()
        start_year_var.set("2010")
        end_year_var = StringVar()
        end_year_var.set('2023')
        options = [
            'BANKEX',
            'FINNIFTY',
            'BANKNIFTY',
            'NIFTY50',
            'SENSEX'
        ]

        index_var.set("NIFTY50")
        index_drop = OptionMenu(self.root, index_var, *options)

        file_select = Button(self.root,text='Select Index Data',command=lambda : self.select_file(file_name_var))
        entry_file_name = Entry(self.root, textvariable=file_name_var, font=("Arial", 12))
        start_year_entry = Entry(self.root, textvariable=start_year_var, font=("Arial", 12))
        end_year_entry = Entry(self.root, textvariable=end_year_var, font=("Arial", 12))

        header.grid(column=0, row=0, columnspan=4, rowspan=2)
        index_label.grid(column=0, row=5)
        index_drop.grid(column=1, row=5)
        filepath_label.grid(column=0, row=6)
        entry_file_name.grid(column=1, row=6)
        file_select.grid(column=2, row=6)
        start_year.grid(column=0, row=7)
        start_year_entry.grid(column=1, row=7)
        end_year.grid(column=2, row=7)
        end_year_entry.grid(column=3, row=7)
        (Button(self.root, text="GET RANGE", command=lambda :self.run_analysis(file_name_var.get(),
                                                                              start_year_var.get(),
                                                                              end_year_var.get(),)).grid(column=1,
                                                                                                        row=8,
                                                                                                        columnspan=2))

        text.grid(row=10, column=0,columnspan=4, padx=10, pady=10)
        scrollbar.grid(row=10, column=4)


    def run_app(self):
        self.add_component()
        self.root.mainloop()


if __name__ == '__main__':
    gui = GUI()
    gui.run_app()
