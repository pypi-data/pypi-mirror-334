import unittest

from hu2.excel2 import ExcelTable


class TestExcel(unittest.TestCase):
    def test_excel(self):
        et = ExcelTable('excel.xlsx')
        et.set_column_width({'A': 10, 'B': 20, 'C': 30})
        et.set_head(['Aa', 'Bb', 'Cc'])
        et.set_body([['a', 'b', 'c'], (1, 2, 3)])

        et.save()



if __name__ == '__main__':
    unittest.main()