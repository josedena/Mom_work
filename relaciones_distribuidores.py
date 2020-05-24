import wx
import Tablas
import query_database as db
import numpy as np
import manage_cliente_dialogs as mcd
import datetime
import imprimir_relaciones as print_rel
import math
import xlwt

class relaciones_distribuidores(wx.Panel):
    def __init__(self, main_window):
        wx.Panel.__init__(self, parent=main_window)
        self.main_window = main_window
        self.SetBackgroundColour('green')
        self.fechas = db.fetch_all_tables() 
        self.all_clientes = db.fetch_data_clientes(self.fechas[0])
        self.distribuidores = np.unique(self.all_clientes[:,2])
        self.clientes_distr = self.all_clientes[np.where(self.all_clientes[:,2] == self.distribuidores[0])]
        self.tiendas_distr = self.clientes_distr[:,1]
        self.tiendas_distr = np.insert(self.tiendas_distr, 0, 'TODAS', axis=0)
        #############################   HEADER PANEL   #######################################
        font = wx.Font(10, wx.FONTFAMILY_MODERN, wx.NORMAL, wx.FONTWEIGHT_BOLD)

        st_fechas = wx.StaticText(self, label='Fechas:')
        st_fechas.SetFont(font)
        st_fechas.Wrap(20)
        st_fechas.SetForegroundColour(wx.BLACK)
        st_distrs = wx.StaticText(self, label='Distribuidores:')
        st_distrs.SetFont(font)
        st_distrs.Wrap(20)
        st_distrs.SetForegroundColour(wx.BLACK)
        st_tiendas = wx.StaticText(self, label='Tiendas distribuidor:')
        st_tiendas.SetFont(font)
        st_tiendas.Wrap(20)
        st_tiendas.SetForegroundColour(wx.BLACK)
        st_edit_client = wx.StaticText(self, label='Editar Cliente:')
        st_edit_client.SetFont(font) 
        st_edit_client.Wrap(20)       
        st_edit_client.SetForegroundColour(wx.BLACK)
        st_print = wx.StaticText(self, label='Imprimir Tabla:')
        st_print.SetFont(font)
        st_print.Wrap(30)
        st_print.SetForegroundColour(wx.BLACK)

        self.cb_fechas = wx.ComboBox(self, choices=self.fechas, style=wx.CB_READONLY)
        self.cb_distrs = wx.ComboBox(self, choices=self.distribuidores, style=wx.CB_READONLY)
        self.cb_tiendas = wx.ComboBox(self, choices=self.tiendas_distr, style=wx.CB_READONLY)
        btn_edit_client = wx.Button(self, label='Editar')
        btn_print = wx.Button(self, id=wx.ID_PRINT , label='Imprimir')

        self.cb_fechas.Bind(wx.EVT_COMBOBOX, self.CB_fechas_OnSelect)
        self.cb_fechas.SetSelection(0) 
        self.cb_distrs.Bind(wx.EVT_COMBOBOX, self.CB_distrs_OnSelect)
        self.cb_distrs.SetSelection(0) 
        self.cb_tiendas.Bind(wx.EVT_COMBOBOX, self.CB_tiendas_OnSelect)
        self.cb_tiendas.SetSelection(0) 
        btn_edit_client.Bind(wx.EVT_BUTTON, self.OnEditClient)
        btn_print.Bind(wx.EVT_BUTTON, self.OnPrint, id=wx.ID_PRINT)

        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox1.Add(st_fechas, 0, wx.ALIGN_CENTER|wx.TOP, 10)
        vbox1.Add(self.cb_fechas, 0, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 10)

        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox2.Add(st_distrs, 0, wx.ALIGN_CENTER|wx.TOP, 10)
        vbox2.Add(self.cb_distrs, 0, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 10)

        vbox3 = wx.BoxSizer(wx.VERTICAL)
        vbox3.Add(st_tiendas, 0, wx.ALIGN_CENTER|wx.TOP, 10)
        vbox3.Add(self.cb_tiendas, 0, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 10)

        vbox4 = wx.BoxSizer(wx.VERTICAL)
        vbox4.Add(st_edit_client, 0, wx.ALIGN_CENTER|wx.TOP, 10)
        vbox4.Add(btn_edit_client, 0, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 10)
        
        vbox5 = wx.BoxSizer(wx.VERTICAL)
        vbox5.Add(st_print, 0, wx.ALIGN_CENTER|wx.TOP, 10)
        vbox5.Add(btn_print, 0, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 10)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(vbox1, 1)
        hbox.Add(vbox2, 1)
        hbox.Add(vbox3, 1)
        hbox.Add(vbox4, 1)
        hbox.Add(vbox5, 1)   

        #############################   GRID PANEL  ########################################

        self.tabla_distrdores = Tablas.Tabla(self)
        self.tabla_distrdores.update_tabla_dist(self.clientes_distr)

        ############################### PANEL ORGANIZER #######################################
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox1.Add(hbox, 0, wx.EXPAND | wx.ALL, 10)
        vbox1.Add(self.tabla_distrdores.myGrid, 1)
        self.SetSizer(vbox1) 

    ############################### CALLBACK FUNCTIONS #######################################
    def update_all(self):
        self.fechas = db.fetch_all_tables() 
        self.cb_fechas.Clear()
        for fecha in self.fechas:
            self.cb_fechas.Append(fecha)
        self.cb_fechas.SetSelection(0)

        self.all_clientes = db.fetch_data_clientes(self.fechas[0])
        self.distribuidores = np.unique(self.all_clientes[:,2])
        self.cb_distrs.Clear()
        for distr in self.distribuidores:
            self.cb_distrs.Append(distr)
        self.cb_distrs.SetSelection(0)

        self.clientes_distr = self.all_clientes[np.where(self.all_clientes[:,2] == self.distribuidores[0])]

        self.tiendas_distr = np.unique(self.clientes_distr[:,1])
        self.cb_tiendas.Clear()
        for tienda in self.tiendas_distr:
            self.cb_tiendas.Append(tienda)
        self.cb_tiendas.SetSelection(0)

        self.tabla_distrdores.update_tabla_dist(self.clientes_distr)

    def export_data_from_cells(self, pathname):
        style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on', num_format_str='#,##0.00')
        style1 = xlwt.easyxf(num_format_str='D-MMM-YY')
        style2 = xlwt.easyxf('font: name Times New Roman, height 180, bold on')
        style3 = xlwt.easyxf('font: name Times New Roman, height 180')

        wb = xlwt.Workbook()
        ws = wb.add_sheet('A Test Sheet')
        ws.col(0).width = 800
        ws.col(2).width = 7000
        ws.col(3).width = 2000
        ws.col(4).width = 2000
        ws.col(5).width = 2000
        ws.col(6).width = 2000
        ws.col(7).width = 2000

        title = 'Relacion del distribuidor "' + self.cb_distrs.GetStringSelection() + '" con fecha a pagar del "' + self.cb_fechas.GetStringSelection()+'"'
        ws.write(0, 2, title, style2)

        cols = self.tabla_distrdores.myGrid.GetNumberCols()
        rows = self.tabla_distrdores.myGrid.GetNumberRows()

        ws.write(2, 0, "No.", style2)
        columna = 1
        for col in range(0,cols):
            if col == 0 or col == 2 or col == 3 or col == 4 or col == 7 or col == 5 or col == 6 or col == 8:
                ws.write(2, columna, str(self.tabla_distrdores.myGrid.GetColLabelValue(col)), style2)
                columna = columna + 1
        
        no_cliente = 1
        renglon = 2
        for row in range(0,rows):
            columna = 0
            renglon = renglon + 1
            for col in range(0,cols):
                if col == 0: 
                    if self.tabla_distrdores.myGrid.GetCellValue(row,0):
                        ws.write(renglon, columna, str(no_cliente), style3)
                        columna = columna + 1
                        ws.write(renglon, columna, str(self.tabla_distrdores.myGrid.GetCellValue(row,col)), style3)
                        columna = columna + 1
                        no_cliente += 1
                if col == 2 or col == 3 or col == 4 or col == 7 or col == 5 or col == 6 or col == 8:
                    ws.write(renglon, columna, str(self.tabla_distrdores.myGrid.GetCellValue(row,col)), style3)
                    columna = columna + 1
        wb.save(pathname+'_'+self.cb_fechas.GetStringSelection()+'.xls')

    def get_data_from_cells(self):
        cols = self.tabla_distrdores.myGrid.GetNumberCols()
        rows = self.tabla_distrdores.myGrid.GetNumberRows()
        #cols_data = []
        all_data = []
        for col in range(0,cols):
            if col == 0:
                cols_data = str("No.").ljust(4)
                cols_data = cols_data + str(self.tabla_distrdores.myGrid.GetColLabelValue(col)).ljust(11)
            if col == 2:
                cols_data = cols_data + str(self.tabla_distrdores.myGrid.GetColLabelValue(col)).ljust(31)
            if col == 3 or col == 4 or col == 7:
                cols_data = cols_data + str(self.tabla_distrdores.myGrid.GetColLabelValue(col)).ljust(10)
            if col == 5:
                cols_data = cols_data + str(self.tabla_distrdores.myGrid.GetColLabelValue(col)).ljust(13)
            if col == 6:
                cols_data = cols_data + str(self.tabla_distrdores.myGrid.GetColLabelValue(col)).ljust(14)
            if col == 8:
                cols_data = cols_data + str(self.tabla_distrdores.myGrid.GetColLabelValue(col)).ljust(15)
        
        all_data.append(cols_data)
        no_cliente = 1
        for row in range(0,rows):
            for col in range(0,cols):
                if col == 0: 
                    if self.tabla_distrdores.myGrid.GetCellValue(row,0):
                        cols_data = str(no_cliente).ljust(4)
                        cols_data = cols_data + "{:.10s}".format(self.tabla_distrdores.myGrid.GetCellValue(row,col)).ljust(11)
                        no_cliente += 1
                    else:
                        cols_data = ''.ljust(4)
                if col == 2:
                    cols_data = cols_data + "{:.30s}".format(self.tabla_distrdores.myGrid.GetCellValue(row,col)).ljust(31)
                if col == 3 or col == 4 or col == 7:
                    cols_data = cols_data + str(self.tabla_distrdores.myGrid.GetCellValue(row,col)).ljust(10)
                if col == 5:
                    cols_data = cols_data + str(self.tabla_distrdores.myGrid.GetCellValue(row,col)).center(13)
                if col == 6:  
                    cols_data = cols_data + str(self.tabla_distrdores.myGrid.GetCellValue(row,col)).center(14)
                if col == 8:
                    cols_data = cols_data + str(self.tabla_distrdores.myGrid.GetCellValue(row,col)).ljust(15)
            all_data.append(cols_data)
            cols_data = ''
        
        for row in range(0, len(all_data)):
            if ':' in all_data[row]:
                split = all_data[row].partition(':')
                all_data[row] = split[0].lstrip().rjust(90) + split[1] + split[2].lstrip().rstrip().rjust(10)

        all_data.insert(0, ''.rjust(90))        
        title = 'Relacion del distribuidor "' + self.cb_distrs.GetStringSelection() + '" con fecha a pagar del "' + self.cb_fechas.GetStringSelection()+'"'
        all_data.insert(0, title.center(110))

        return all_data


    def OnPrint(self, event):
        # initialize the print data and set some default values
        pdata = wx.PrintData()
        pdata.SetPaperId(wx.PAPER_LETTER)
        pdata.SetOrientation(wx.PORTRAIT)
        margins = (wx.Point(4.0, 4.0), wx.Point(4.0, 4.0))

        #------------

        text = self.get_data_from_cells()
        printout = print_rel.TextDocPrintout(text, "Imprimir Relaciones", margins)
        data = wx.PrintDialogData(pdata)
        data.SetMinPage(1)
        data.SetMaxPage(math.ceil(len(text)/96))
        printer = wx.Printer(data)  
        useSetupDialog = True
        if not printer.Print(self.main_window, printout, useSetupDialog) \
           and printer.GetLastError() == wx.PRINTER_ERROR:
            wx.MessageBox(
                "Hubo un problema al imprimir.\n"
                "Quiza la imporesora no esta instalada correctamente?",
                "Error al imprimir", wx.OK)
        else:
            data = printer.GetPrintDialogData()
            pdata = wx.PrintData(data.GetPrintData()) # force a copy
        printout.Destroy()   

    def CB_fechas_OnSelect(self, e):
        i = e.GetString()
        
        self.all_clientes = db.fetch_data_clientes(i)
        self.distribuidores = np.unique(self.all_clientes[:,2])
        self.cb_distrs.Clear()
        for distr in self.distribuidores:
            self.cb_distrs.Append(distr)
        self.cb_distrs.SetSelection(0)

        self.clientes_distr = self.all_clientes[np.where(self.all_clientes[:,2] == self.distribuidores[0])]

        self.tiendas_distr = np.unique(self.clientes_distr[:,1])
        self.cb_tiendas.Clear()
        self.cb_tiendas.Append('TODAS')
        for tienda in self.tiendas_distr:
            self.cb_tiendas.Append(tienda)
        self.cb_tiendas.SetSelection(0)

        self.tabla_distrdores.update_tabla_dist(self.clientes_distr)

    def CB_distrs_OnSelect(self, e):
        i = e.GetString()

        self.clientes_distr = self.all_clientes[np.where(self.all_clientes[:,2] == i)]

        self.tiendas_distr = np.unique(self.clientes_distr[:,1])
        self.cb_tiendas.Clear()
        self.cb_tiendas.Append('TODAS')
        for tienda in self.tiendas_distr:
            self.cb_tiendas.Append(tienda)
        self.cb_tiendas.SetSelection(0)

        self.tabla_distrdores.update_tabla_dist(self.clientes_distr)
    
    def CB_tiendas_OnSelect(self, e):
        i = e.GetString()
        if i == 'TODAS':
            clientes_distr_tienda = self.all_clientes[np.where(self.all_clientes[:,2] == self.cb_distrs.GetStringSelection())]
        else:
            clientes_distr_tienda = self.clientes_distr[np.where(self.clientes_distr[:,1] == i)]
        self.tabla_distrdores.update_tabla_dist(clientes_distr_tienda)

    def update_info(self, cliente_):
        self.all_clientes = db.fetch_data_clientes(self.cb_fechas.GetStringSelection())
        self.distribuidores = np.unique(self.all_clientes[:,2])
        self.cb_distrs.Clear()
        for distr in self.distribuidores:
            self.cb_distrs.Append(distr)
        self.cb_distrs.SetValue(cliente_[1])

        self.clientes_distr = self.all_clientes[np.where(self.all_clientes[:,2] == cliente_[1])]

        self.tiendas_distr = np.unique(self.clientes_distr[:,1])
        self.cb_tiendas.Clear()
        self.cb_tiendas.Append('TODAS')
        for tienda in self.tiendas_distr:
            self.cb_tiendas.Append(tienda)
        self.cb_tiendas.SetValue('TODAS')

        #clientes_distr_tienda = self.clientes_distr[np.where(self.clientes_distr[:,1] == cliente_[0])]
        self.tabla_distrdores.update_tabla_dist(self.clientes_distr)

    def OnEditClient(self, e):
        dlg = wx.TextEntryDialog(self.main_window, 'Ingresa el numero de cliente a editar:', 'Editar Cliente')
        dlg.CentreOnParent()
        continue_ = 0
        ed_cliente = 0
        while continue_ == 0:
            if dlg.ShowModal() == wx.ID_OK:
                no_cliente=dlg.GetValue()
                cliente_ = db.fetch_one_cliente(self.cb_fechas.GetStringSelection(), no_cliente)
                if cliente_ == []:
                    wx.MessageBox('Numero de Cliente Incorrecto!!', 'Error!!', wx.OK | wx.ICON_ERROR)
                else:
                    _cliente = []
                    for client in cliente_[0]:
                        _cliente.append(str(client))
                    continue_ = 1
                    ed_cliente = 1
            else:
                continue_ = 1
        dlg.Destroy()
        if ed_cliente == 1: 
            title_ = "Editar cliente:"
            self.cliente_management(_cliente, title_, 1, no_cliente)

    def cliente_management(self, cliente_, title, option, agg_ed):
        win = mcd.new_client_dialog(self.main_window, title, self.cb_fechas.GetStringSelection(), cliente_)
        new_client_ = 0
        while new_client_ == 0:
            if win.ncd_dialog.ShowModal() == wx.ID_OK:
                new_client_ = win.Onagregar_Editar(option, agg_ed)
                if new_client_ == 1:
                    self.update_info(win.new_cliente)
            else:
                new_client_ = 1
        win.ncd_dialog.Destroy()
