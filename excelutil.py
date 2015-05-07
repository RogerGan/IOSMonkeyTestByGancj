# -*- coding:UTF-8 -*-
__author__ = 'roger'

import xlrd
import xlsxwriter

def readfromexcel(filepath = './urls.xls'):
      table = xlrd.open_workbook(filepath).sheets()[0]
      nrows = table.nrows
      data = []
      for i in range(nrows):
        if table.row_values(i) != ['']:
            data.append(table.row_values(i))
      return data

def insertdata(xlsxname, sheetname, list):
    workbook = xlsxwriter.Workbook(xlsxname)
    worksheet = workbook.add_worksheet(sheetname)
    rows = len(list)
    for i in xrange(rows):
        worksheet.set_row(i, 100)
        colum = len(list[i])
        for j in xrange(colum):
            worksheet.set_column(j, 100)
            worksheet.write(i, j, list[i][j])
    workbook.close()