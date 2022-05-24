import pandas as pd
import numpy as np
from numpy import ndarray
import warnings


class ExcelProcessing:
    """
    Examples
    --------
    ::

        excel_p = ExcelProcessing("excel.xlsx", sheet_name='Sheet1')
        all = excel_p.filter_data_horizontal('header1', 'header2', 'header3', 'header4')

        for one in all:
            header1, header2, header3, header4 = one
            pass
    """
    def __init__(self, excel_file_dir, sheet_name):
        """
        Excel processing package

        Parameters
        ----------
        excel_file_dir:
            Specify the Excel file or its directory
        sheet_name:
            Specify the sheet name
        """
        warnings.filterwarnings("ignore")

        self._data_target = list()
        self._tag_index = list()

        with open(excel_file_dir, 'rb') as file:
            self._data_xlsx = pd.read_excel(file, sheet_name=sheet_name)

    def get_excel_header(self) -> list:
        """
        Get the header of the Excel table
        """
        return [header for header in self._data_xlsx]

    def _get_index_tag_header(self, *args) -> list:
        excel_header = self.get_excel_header()
        for tag in args:
            if tag in excel_header:
                self._tag_index.append(excel_header.index(tag))
        return self._tag_index

    def filter_data_horizontal(self, *args) -> ndarray:
        """
        Filter data according to the information specified

        Parameters
        ----------
        args:
            Specify the headers you need

        """
        self._tag_index = self._get_index_tag_header(*args)
        for data_initial in self._data_xlsx.values:
            data_person = [data_initial[tag_index] for tag_index in self._tag_index]
            self._data_target.append(data_person)
        return np.array(self._data_target)

    def filter_data_vertical(self, *args) -> ndarray:
        """
        Filter data according to the information specified

        Parameters
        ----------
        args:
            Specify the headers you need

        """
        self.filter_data_horizontal(*args)
        data_target = [[self._data_target[i][j] for i in range(0, len(self._data_target))]
                       for j in range(0, len(args))]
        return np.array(data_target)
