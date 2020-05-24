import wx
import wx.grid
import numpy as np
import query_database as db
import datetime

class Tabla:
    def __init__(self, parent):
        #self.panel_grid = wx.Panel(parent)
        self.parent = parent
        tabla_header = ['Tienda', 'Distribuidor', 'Cliente', 'Folio', 'Compra', 'Q_Actual', 'Q_Totales', 'Minimo', 'Fecha_Compra', 'Fecha_incio', 'Mi_Comision', 'Comision_Distr']
        header_col_size = [[0,95], [1,90], [2,270],[3,65],[4,70],[5,80],[6,80],[7,80],[8,100],[9,100],[10,80],[11,100]]

        self.myGrid = wx.grid.Grid(parent, -1, style=wx.BORDER_THEME)
        self.myGrid.CreateGrid(0, 12)
        self.myGrid.SetLabelFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.FONTWEIGHT_BOLD))

        col = 0
        for header_col in tabla_header:
            self.myGrid.SetColLabelValue(col, header_col)
            col += 1
        
        for size in header_col_size:
            self.myGrid.SetColSize(size[0], size[1])

 
    def update_tabla_dist(self, data_):
        font_size = 9
        _data = np.asarray(data_)
        unique_tiendas = np.unique(_data[:,1])
        rows = self.myGrid.GetNumberRows()
        if rows > 0:
            self.myGrid.DeleteRows(0,rows)
        init_rows = 0
        max_rows = 0
        totales_ = []
        for tienda in unique_tiendas:
            data = _data[np.where(_data[:,1] == tienda)]
            max_rows = data.shape[0]
            max_cols = data.shape[1]
            self.myGrid.AppendRows(max_rows+5)
            for row in range(0, max_rows):
                for col in range(0, max_cols-1):
                    if col == 10:
                        self.myGrid.SetCellValue(init_rows+row, col+1, str(data[row,col+1])+' %') 
                        self.myGrid.SetCellAlignment(init_rows+row, col+1, wx.ALIGN_LEFT, wx.ALIGN_CENTER) 
                    else:
                        if col == 5 or col == 6:
                            self.myGrid.SetCellValue(init_rows+row, col, str(data[row,col+1]))
                            self.myGrid.SetCellAlignment(init_rows+row, col, wx.ALIGN_CENTER, wx.ALIGN_CENTER) 
                        else: 
                            if col == 4:
                                self.myGrid.SetCellValue(init_rows+row, col, '$'+ "{0:.2f}".format(data[row,col+1]).rjust(7))
                                self.myGrid.SetCellAlignment(init_rows+row, col, wx.ALIGN_RIGHT, wx.ALIGN_CENTER) 
                            if col == 7:
                                if tienda == 'MODERNA' and data[row,6] == 1: 
                                    self.myGrid.SetCellValue(init_rows+row, col, '$!'+ "{0:.2f}".format(data[row,col+1]+24).rjust(7))
                                else:
                                    self.myGrid.SetCellValue(init_rows+row, col, '$'+ "{0:.2f}".format(data[row,col+1]).rjust(7))
                                self.myGrid.SetCellAlignment(init_rows+row, col, wx.ALIGN_RIGHT, wx.ALIGN_CENTER)   
                            else:
                                if col == 8 or col == 9:
                                    _date = datetime.datetime.strftime(data[row,col+1], "%d_%b_%Y")
                                    self.myGrid.SetCellValue(init_rows+row, col, _date.upper())
                                    self.myGrid.SetCellAlignment(init_rows+row, col, wx.ALIGN_RIGHT, wx.ALIGN_CENTER) 
                                else:  
                                    if col == 0:
                                        self.myGrid.SetRowLabelValue(init_rows+row, str(data[row,col]))
                                    self.myGrid.SetCellValue(init_rows+row, col, str(data[row][col+1]).encode('utf8').upper())
                    self.myGrid.SetReadOnly(init_rows+row, col, True)
                    self.myGrid.SetCellFont(init_rows+row, col, wx.Font(font_size, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

            self.myGrid.SetRowLabelValue(init_rows+max_rows, '')
            self.myGrid.SetRowLabelValue(init_rows+max_rows+1, '')
            self.myGrid.SetCellSize(init_rows+max_rows+1, 4, 1, 3)
            self.myGrid.SetCellValue(init_rows+max_rows+1, 4, 'TOTAL MINIMOS:')
            self.myGrid.SetCellFont(init_rows+max_rows+1, 4, wx.Font(font_size, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
            self.myGrid.SetCellAlignment(init_rows+max_rows+1, 4, wx.ALIGN_RIGHT, wx.ALIGN_CENTER) 
            self.myGrid.SetReadOnly(init_rows+max_rows+1, 4, True)
            self.myGrid.SetCellValue(init_rows+max_rows+1, 7, '$' + "{0:.2f}".format(np.sum(data[:,8])).rjust(7))
            self.myGrid.SetCellFont(init_rows+max_rows+1, 7, wx.Font(font_size, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
            self.myGrid.SetCellAlignment(init_rows+max_rows+1, 7, wx.ALIGN_RIGHT, wx.ALIGN_CENTER) 
            self.myGrid.SetReadOnly(init_rows+max_rows+1, 7, True)

            self.myGrid.SetRowLabelValue(init_rows+max_rows+2, '')
            self.myGrid.SetCellSize(init_rows+max_rows+2, 4, 1, 3)
            self.myGrid.SetCellValue(init_rows+max_rows+2, 4, 'TOTAL COMISIONES:')
            self.myGrid.SetCellFont(init_rows+max_rows+2, 4, wx.Font(font_size, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
            self.myGrid.SetCellAlignment(init_rows+max_rows+2, 4, wx.ALIGN_RIGHT, wx.ALIGN_CENTER) 
            self.myGrid.SetReadOnly(init_rows+max_rows+2, 4, True)
            self.myGrid.SetCellValue(init_rows+max_rows+2, 7, '$' + "{0:.2f}".format(np.sum(data[:,8]*(data[:,11]/100.0))).rjust(7))
            self.myGrid.SetCellFont(init_rows+max_rows+2, 7, wx.Font(font_size, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
            self.myGrid.SetCellAlignment(init_rows+max_rows+2, 7, wx.ALIGN_RIGHT, wx.ALIGN_CENTER) 
            self.myGrid.SetReadOnly(init_rows+max_rows+2, 7, True)
            self.myGrid.SetCellValue(init_rows+max_rows+2, 8, "{0:.1f}".format(np.max(data[:,11])) + "%".rjust(7))
            self.myGrid.SetCellFont(init_rows+max_rows+2, 8, wx.Font(font_size, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
            self.myGrid.SetCellAlignment(init_rows+max_rows+2, 8, wx.ALIGN_RIGHT, wx.ALIGN_CENTER) 
            self.myGrid.SetReadOnly(init_rows+max_rows+2, 8, True)

            self.myGrid.SetRowLabelValue(init_rows+max_rows+3, '')
            self.myGrid.SetRowLabelValue(init_rows+max_rows+4, '')
            self.myGrid.SetCellSize(init_rows+max_rows+3, 4, 1, 3)
            self.myGrid.SetCellValue(init_rows+max_rows+3, 4, 'TOTAL A PAGAR:')
            self.myGrid.SetCellFont(init_rows+max_rows+3, 4, wx.Font(font_size, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
            self.myGrid.SetCellAlignment(init_rows+max_rows+3, 4, wx.ALIGN_RIGHT, wx.ALIGN_CENTER) 
            self.myGrid.SetReadOnly(init_rows+max_rows+3, 4, True)
            self.myGrid.SetCellValue(init_rows+max_rows+3, 7, '$' + "{0:.2f}".format(np.sum(data[:,8]) - np.sum(data[:,8]*(data[:,11]/100.0))).rjust(7))
            totales_.append([tienda, round(np.sum(data[:,8]) - np.sum(data[:,8]*(data[:,11]/100.0)),2)])
            self.myGrid.SetCellFont(init_rows+max_rows+3, 7, wx.Font(font_size, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
            self.myGrid.SetCellAlignment(init_rows+max_rows+3, 7, wx.ALIGN_RIGHT, wx.ALIGN_CENTER) 
            self.myGrid.SetReadOnly(init_rows+max_rows+3, 7, True)

            init_rows = init_rows + max_rows + 5
        
        self.myGrid.AppendRows(len(totales_)+2)
        totales_ = np.asarray(totales_)
        for row in range(0, totales_.shape[0]):
            self.myGrid.SetRowLabelValue(init_rows+row, '')
            self.myGrid.SetCellSize(init_rows+row, 4, 1, 3)
            self.myGrid.SetCellValue(init_rows+row, 4, totales_[row,0]+':')
            self.myGrid.SetCellFont(init_rows+row, 4, wx.Font(font_size, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
            self.myGrid.SetCellAlignment(init_rows+row, 4, wx.ALIGN_RIGHT, wx.ALIGN_CENTER) 
            self.myGrid.SetReadOnly(init_rows+row, 4, True)
            self.myGrid.SetCellValue(init_rows+row, 7, '$' + "{0:.2f}".format(float(totales_[row,1])).rjust(7))
            self.myGrid.SetCellFont(init_rows+row, 7, wx.Font(font_size, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
            self.myGrid.SetCellAlignment(init_rows+row, 7, wx.ALIGN_RIGHT, wx.ALIGN_CENTER) 
            self.myGrid.SetReadOnly(init_rows+row, 7, True)
        
        self.myGrid.SetRowLabelValue(init_rows+row+1, '')
        self.myGrid.SetCellSize(init_rows+row+1,  5, 1, 2)
        self.myGrid.SetCellValue(init_rows+row+1, 5, 'SUMA DE TOTALES:')
        self.myGrid.SetCellFont(init_rows+row+1,  5, wx.Font(font_size, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.myGrid.SetCellAlignment(init_rows+row+1, 5, wx.ALIGN_RIGHT, wx.ALIGN_CENTER) 
        self.myGrid.SetReadOnly(init_rows+row+1, 5, True)
        self.myGrid.SetCellValue(init_rows+row+1, 7, '$' + "{0:.2f}".format(np.sum(totales_[:,1].astype(np.float))).rjust(7))
        self.myGrid.SetCellFont(init_rows+row+1, 7, wx.Font(font_size, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.myGrid.SetCellAlignment(init_rows+row+1, 7, wx.ALIGN_RIGHT, wx.ALIGN_CENTER) 
        self.myGrid.SetReadOnly(init_rows+row+1, 7, True)
        self.myGrid.SetRowLabelValue(init_rows+row+2, '')
        

    def update_tabla_tiendas(self, data_, mis_comisiones ,fecha_str):
        font_size = 9
        fecha_obj = datetime.datetime.strptime(fecha_str, "%d_%b_%Y")
        data = np.asarray(data_)
        max_rows = data.shape[0]
        max_cols = data.shape[1]
        rows = self.myGrid.GetNumberRows()
        if rows > 0:
            self.myGrid.DeleteRows(0,rows)
        self.myGrid.AppendRows(max_rows+1)

        for row in range(0, max_rows):
            if data[row][10] > fecha_obj.date():
                self.myGrid.SetCellBackgroundColour(row, 9, wx.RED)
                self.myGrid.SetCellTextColour(row, 7, wx.RED)
            for col in range(0, max_cols-1):
                if col == 10:
                    comision = np.where(mis_comisiones == data[row][1])[0][0]
                    self.myGrid.SetCellValue(row, col, str(mis_comisiones[comision,2]) + ' %')
                    self.myGrid.SetCellValue(row, col+1, str(data[row][col+1]) + ' %')
                    self.myGrid.SetReadOnly(row, col, True)
                    self.myGrid.SetReadOnly(row, col+1, True)
                else:
                    if col == 4:
                        self.myGrid.SetCellValue(row, col, '$ '+ str(data[row][col+1])) 
                        self.myGrid.SetReadOnly(row, col, False) 
                    if col == 7:
                        if data[row][1] == 'MODERNA' and data[row][6] == 1: 
                            self.myGrid.SetCellValue(row, col, '$! '+ str(data[row][col+1]+28))
                        else:
                            self.myGrid.SetCellValue(row, col, '$ '+ str(data[row][col+1]))
                        self.myGrid.SetReadOnly(row, col, False)
                    else:
                        if col == 8 or col == 9:
                            _date = datetime.datetime.strftime(data[row][col+1], "%d_%b_%Y")
                            self.myGrid.SetCellValue(row, col, str(_date).upper())  
                            self.myGrid.SetReadOnly(row, col, True)
                        else:    
                            if col == 5 or col == 6:
                                self.myGrid.SetCellValue(row, col, str(data[row][col+1]).encode('utf8').upper()) 
                                self.myGrid.SetReadOnly(row, col, False)
                            else: 
                                if col == 0:
                                    self.myGrid.SetRowLabelValue(row, str(data[row][col]))
                                self.myGrid.SetCellValue(row, col, str(data[row][col+1]).encode('utf8').upper())
                                self.myGrid.SetReadOnly(row, col, True)
                self.myGrid.SetCellFont(row, col, wx.Font(font_size, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        