import wx
import wx.grid
import Tablas
import query_database as db
import numpy as np
import manage_cliente_dialogs as ncd
import select_tiendas_new_quincena as stnq
import datetime

class relaciones_tiendas(wx.Panel):
    def __init__(self, main_window):
        wx.Panel.__init__(self, parent=main_window)
        self.main_window = main_window
        self.SetBackgroundColour('blue')
        self.fechas = db.fetch_all_tables() 
        self.clientes = db.fetch_data_clientes(self.fechas[0])
        self.tiendas = np.unique(self.clientes[:,1])#db.fetch_all_tiendas_from_table(self.fechas[0])
        self.mis_comisiones = db.fetch_all_comisiones()
        a = list(set(self.tiendas).difference(set(self.mis_comisiones[:,1])))
        if a:
            db.insert_new_tienda(a[0], self)
            self.mis_comisiones = db.fetch_all_comisiones()
        self.tiendas = np.insert(self.tiendas, 0, 'TODAS', axis=0)
        #############################   HEADER PANEL   #######################################
        font = wx.Font(12, wx.FONTFAMILY_MODERN, wx.NORMAL, wx.FONTWEIGHT_BOLD)

        st_fechas = wx.StaticText(self, label='Seleccionar Fecha:')
        st_fechas.Wrap(20) 
        st_fechas.SetFont(font)
        st_fechas.SetForegroundColour(wx.BLACK)
        st_tiendas = wx.StaticText(self, label='Mostrar Tiendas:')
        st_tiendas.Wrap(20)
        st_tiendas.SetFont(font)
        st_tiendas.SetForegroundColour(wx.BLACK)
        st_new_quinc = wx.StaticText(self, label='Avanzar Quincena:')
        st_new_quinc.Wrap(20)
        st_new_quinc.SetFont(font)
        st_new_quinc.SetForegroundColour(wx.BLACK)
        st_new_client = wx.StaticText(self, label='Agregar Cliente:')
        st_new_client.Wrap(20)
        st_new_client.SetFont(font)
        st_new_client.SetForegroundColour(wx.BLACK)
        st_edit_client = wx.StaticText(self, label='Editar Cliente:')
        st_edit_client.Wrap(20)
        st_edit_client.SetFont(font)
        st_edit_client.SetForegroundColour(wx.BLACK)
        st_delete_client = wx.StaticText(self, label='Eliminar Cliente:')
        st_delete_client.Wrap(20)
        st_delete_client.SetFont(font)
        st_delete_client.SetForegroundColour(wx.BLACK)

        self.cb_fechas = wx.ComboBox(self, choices=self.fechas, style=wx.CB_READONLY)
        self.cb_fechas.SetSelection(0)
        self.cb_tiendas = wx.ComboBox(self, choices=self.tiendas, style=wx.CB_READONLY)
        self.cb_tiendas.SetSelection(0)
        btn_av_quinc = wx.Button(self, label='Avanzar...')
        btn_new_client = wx.Button(self, label='Agregar')
        btn_edit_client = wx.Button(self, id=wx.ID_ANY, label='Editar')
        btn_delete_client = wx.Button(self, id=wx.ID_ANY, label='Eliminar')

        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox1.Add(st_fechas, 0, wx.ALIGN_CENTER|wx.TOP, 10)
        vbox1.Add(self.cb_fechas, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox2.Add(st_tiendas, 0, wx.ALIGN_CENTER|wx.TOP, 10)
        vbox2.Add(self.cb_tiendas, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        vbox3 = wx.BoxSizer(wx.VERTICAL)
        vbox3.Add(st_new_quinc, 1, wx.ALIGN_CENTER|wx.TOP, 10)
        vbox3.Add(btn_av_quinc, 0, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 10)

        vbox4 = wx.BoxSizer(wx.VERTICAL)
        vbox4.Add(st_new_client, 1, wx.ALIGN_CENTER|wx.TOP, 10)
        vbox4.Add(btn_new_client, 0, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 10)
        
        vbox5 = wx.BoxSizer(wx.VERTICAL)
        vbox5.Add(st_edit_client, 1, wx.ALIGN_CENTER|wx.TOP, 10)
        vbox5.Add(btn_edit_client, 0, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 10)

        vbox6 = wx.BoxSizer(wx.VERTICAL)
        vbox6.Add(st_delete_client, 1, wx.ALIGN_CENTER|wx.TOP, 10)
        vbox6.Add(btn_delete_client, 0, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 10)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(vbox1, 0)
        hbox.Add(vbox2, 0)
        hbox.Add(vbox3, 1)
        hbox.Add(vbox4, 1)
        hbox.Add(vbox5, 1)
        hbox.Add(vbox6, 1)   

        #############################   GRID  ########################################
        
        self.tabla_tiendas = Tablas.Tabla(self)
        self.tabla_tiendas.myGrid.Bind(wx.grid.EVT_GRID_CELL_CHANGED, self.OnCellChange)
        self.tabla_tiendas.update_tabla_tiendas(self.clientes, self.mis_comisiones, self.cb_fechas.GetStringSelection())

        #############################   FOOT  #########################################

        st_total_minimos = wx.StaticText(self, label='Total Minimos:')
        st_total_minimos.SetFont(font)
        st_total_minimos.SetForegroundColour(wx.BLACK)
        self.total_minimos = wx.StaticText(self, label='')
        self.total_minimos.SetFont(font)
        self.total_minimos.SetForegroundColour(wx.YELLOW)

        st_total_comision = wx.StaticText(self, label='Total Comisiones:')
        st_total_comision.SetFont(font) 
        st_total_comision.SetForegroundColour(wx.BLACK)
        self.total_comision = wx.StaticText(self, label='')
        self.total_comision.SetFont(font)
        self.total_comision.SetForegroundColour(wx.YELLOW)

        st_total_pagar = wx.StaticText(self, label='Total a Pagar:')
        st_total_pagar.SetFont(font) 
        st_total_pagar.SetForegroundColour(wx.BLACK)
        self.total_pagar = wx.StaticText(self, label='')
        self.total_pagar.SetFont(font)
        self.total_pagar.SetForegroundColour(wx.YELLOW)

        st_total_distr_comision = wx.StaticText(self, label='Comision Distribuidores:')
        st_total_distr_comision.SetFont(font) 
        st_total_distr_comision.SetForegroundColour(wx.BLACK)
        self.total_distr_com = wx.StaticText(self, label='')
        self.total_distr_com.SetFont(font)
        self.total_distr_com.SetForegroundColour(wx.RED)

        st_total_ingreso = wx.StaticText(self, label='Comision Final:')
        st_total_ingreso.SetFont(font) 
        st_total_ingreso.SetForegroundColour(wx.BLACK)
        self.total_ingreso = wx.StaticText(self, label='')
        self.total_ingreso.SetFont(font)
        self.total_ingreso.SetForegroundColour(wx.GREEN)

        st_nota = wx.StaticText(self, label='*Los clientes con fecha de inicio mayor a la relacion actual, no son considerados en los totales!!')
        st_nota.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
        st_nota.SetForegroundColour(wx.YELLOW)

        vbox6 = wx.BoxSizer(wx.VERTICAL)
        vbox6.Add(st_total_minimos, 0, wx.ALIGN_CENTER|wx.TOP, 10)
        vbox6.Add(self.total_minimos, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        vbox7 = wx.BoxSizer(wx.VERTICAL)
        vbox7.Add(st_total_comision, 0, wx.ALIGN_CENTER|wx.TOP, 10)
        vbox7.Add(self.total_comision, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        vbox8 = wx.BoxSizer(wx.VERTICAL)
        vbox8.Add(st_total_pagar, 1, wx.ALIGN_CENTER|wx.TOP, 10)
        vbox8.Add(self.total_pagar, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        vbox9 = wx.BoxSizer(wx.VERTICAL)
        vbox9.Add(st_total_distr_comision, 1, wx.ALIGN_CENTER|wx.TOP, 10)
        vbox9.Add(self.total_distr_com, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        
        vbox10 = wx.BoxSizer(wx.VERTICAL)
        vbox10.Add(st_total_ingreso, 1, wx.ALIGN_CENTER|wx.TOP, 10)
        vbox10.Add(self.total_ingreso, 0,  wx.ALIGN_CENTER | wx.ALL, 10)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.Add(vbox6,  )
        hbox2.Add(vbox7,  1)
        hbox2.Add(vbox8,  1)
        hbox2.Add(vbox9,  1)
        hbox2.Add(vbox10, 1)   

        #############################   OVERALL VERTICAL ADJUSMENT  ########################################
        vbox11 = wx.BoxSizer(wx.VERTICAL)
        vbox11.Add(hbox, 0, wx.EXPAND | wx.ALL, 10)
        vbox11.Add(self.tabla_tiendas.myGrid, 1)
        vbox11.Add(hbox2, 0, wx.EXPAND | wx.ALL, 10)
        vbox11.Add(st_nota, 0)
        self.SetSizer(vbox11) 
       
        self.cb_fechas.Bind(wx.EVT_COMBOBOX, self.CB_fechas_OnSelect)
        self.cb_tiendas.Bind(wx.EVT_COMBOBOX, self.CB_tiendas_OnSelect)
        btn_av_quinc.Bind(wx.EVT_BUTTON, self.OnNewQuincena)
        btn_new_client.Bind(wx.EVT_BUTTON, self.OnNewClient)
        btn_edit_client.Bind(wx.EVT_BUTTON, self.OnEditClient)
        btn_delete_client.Bind(wx.EVT_BUTTON, self.OnDeleteClient)
        
        self.update_totales(self.clientes)  

    ############################### CALLBACK FUNCTIONS #######################################
    def OnCellChange(self, evt):
        #print ("OnCellChange: (%d,%d) %s\n" % (evt.GetRow(), evt.GetCol(), evt.GetPosition()))

        if evt.GetCol() == 4 or evt.GetCol() == 7:
            value = self.tabla_tiendas.myGrid.GetCellValue(evt.GetRow(), evt.GetCol())
            value = value.replace('$',' ')
            self.tabla_tiendas.myGrid.SetCellValue(evt.GetRow(), evt.GetCol(), '$ '+ str(float(value))) 
        if  evt.GetCol() == 10 or evt.GetCol() == 11:
            value = self.tabla_tiendas.myGrid.GetCellValue(evt.GetRow(), evt.GetCol())
            value = value.replace('%',' ')
            self.tabla_tiendas.myGrid.SetCellValue(evt.GetRow(), evt.GetCol(), str(value) + ' %')

        cliente = []
        cliente.append(self.tabla_tiendas.myGrid.GetRowLabelValue(evt.GetRow()))
        for col in range(12):
            cliente.append(self.tabla_tiendas.myGrid.GetCellValue(evt.GetRow(),col))

        if self.On_Editar(cliente):
            i = self.cb_fechas.GetStringSelection()
            self.clientes = db.fetch_data_clientes(i)
            self.tiendas = np.unique(self.clientes[:,1])#db.fetch_all_tiendas_from_table(self.fechas[0])
            self.tiendas = np.insert(self.tiendas, 0, 'TODAS', axis=0)
            self.mis_comisiones = db.fetch_all_comisiones()
            tienda_ = cliente[1].upper()
            self.cb_tiendas.Clear()
            for tienda in self.tiendas:
                self.cb_tiendas.Append(tienda)
            self.cb_tiendas.SetValue(tienda_)

            clientes_select = self.clientes[np.where(self.clientes[:,1] == cliente[1])]

            #self.tabla_tiendas.update_tabla_tiendas(clientes_select, self.mis_comisiones, self.cb_fechas.GetStringSelection())            
            self.update_totales(clientes_select)
        

    def update_all(self):
        self.fechas = db.fetch_all_tables() 
        self.cb_fechas.Clear()
        for fecha in self.fechas:
            self.cb_fechas.Append(fecha)
        self.cb_fechas.SetSelection(0)

        self.clientes = db.fetch_data_clientes(self.fechas[0])

        self.tiendas = np.unique(self.clientes[:,1])#db.fetch_all_tiendas_from_table(self.fechas[0])
        self.tiendas = np.insert(self.tiendas, 0, 'TODAS', axis=0)
        self.cb_tiendas.Clear()
        for tienda in self.tiendas:
            self.cb_tiendas.Append(tienda)
        self.cb_tiendas.SetSelection(0)
        
        self.tabla_tiendas.update_tabla_tiendas(self.clientes, self.mis_comisiones, self.fechas[0])
        self.update_totales(self.clientes)

    def CB_fechas_OnSelect(self, e):
        i = e.GetString()
        self.clientes = db.fetch_data_clientes(i)
        self.tiendas = np.unique(self.clientes[:,1])#db.fetch_all_tiendas_from_table(self.fechas[0])
        self.tiendas = np.insert(self.tiendas, 0, 'TODAS', axis=0)
        self.cb_tiendas.Clear()
        for tienda in self.tiendas:
            self.cb_tiendas.Append(tienda)
        self.cb_tiendas.SetSelection(0)
        
        self.tabla_tiendas.update_tabla_tiendas(self.clientes, self.mis_comisiones, self.cb_fechas.GetStringSelection())
        self.update_totales(self.clientes)
    
    def CB_tiendas_OnSelect(self, e):
        i = e.GetString()
        if i == 'TODAS':
            clientes_select = self.clientes
        else:
            clientes_select = self.clientes[np.where(self.clientes[:,1] == i)]
        self.tabla_tiendas.update_tabla_tiendas(clientes_select, self.mis_comisiones, self.cb_fechas.GetStringSelection())
        self.update_totales(clientes_select)

    def get_next_fecha(self, date_type):
        new_date = datetime.datetime.now()
        day_ = new_date.day
        month_ = new_date.month
        year_ = new_date.year
        if new_date.day > 20:
            day_ = 6
            month_ = month_ + 1
            if new_date.month == 12:
                month_ = 1
                year_ = new_date.year + 1
        else:
            if new_date.day < 6:
                day_ = 6
            else:
                day_ = 20
        if date_type == 0:
            new_date = datetime.datetime(year_, month_, day_).strftime("%d_%B_%Y")
        else:
            new_date = datetime.datetime(year_, month_, day_).strftime("%Y-%m-%d")

        return new_date


    def OnNewQuincena(self, e):
        new_date = self.get_next_fecha(0)
        if datetime.datetime.strptime(new_date, '%d_%B_%Y').strftime('%d_%b_%Y').upper() in self.fechas:
            message_text = "La proxima fecha de pago es " + new_date + ", y ya se encuentra en el sistema."
            wx.MessageBox(message_text, 'Error', wx.OK | wx.ICON_ERROR)
        else:
            message_ = "Estas seguro que deseas avanzar a la quincena del " + new_date + "?"
            dlg = wx.MessageDialog(None, message_,'Avanzar quincena',wx.OK| wx.CANCEL | wx.ICON_QUESTION)
            result = dlg.ShowModal()
            fechas_obj = []
            if result == wx.ID_OK:
                win = stnq.select_which_tiendas(self.main_window, "Seleccionar tiendas a avanzar:", self.tiendas)
                btn_pressed = win.stnq_dialog.ShowModal()
                if btn_pressed == wx.ID_OK:
                    for fecha in self.fechas:
                        fechas_obj.append(datetime.datetime.strptime(fecha, "%d_%b_%Y"))
                    last_date = max(fechas_obj)
                    last_date = last_date.strftime("%d_%b_%Y")
                    new_date = datetime.datetime.strptime(new_date, '%d_%B_%Y').strftime('%d_%b_%Y')
                    self.clientes = db.new_table_quinc(last_date, new_date, win.new_tiendas_select)
                    
                    self.fechas = db.fetch_all_tables() 
                    self.cb_fechas.Clear()
                    for fecha in self.fechas:
                        self.cb_fechas.Append(fecha)
                    self.cb_fechas.SetValue(new_date)
                    
                    self.tiendas = np.unique(self.clientes[:,1])#db.fetch_all_tiendas_from_table(self.fechas[0])
                    self.cb_tiendas.Clear()
                    self.tiendas = np.insert(self.tiendas, 0, 'TODAS', axis=0)
                    for tienda in self.tiendas:
                        self.cb_tiendas.Append(tienda)
                    self.cb_tiendas.SetSelection(0)

                    self.tabla_tiendas.update_tabla_tiendas(self.clientes, self.mis_comisiones, self.cb_fechas.GetStringSelection())
                    self.update_totales(self.clientes)
                
            dlg.Destroy()
  

    def OnNewClient(self, e):
        cliente_ = ['']*12
        tienda_selected = self.cb_tiendas.GetStringSelection()
        if tienda_selected != "TODAS":
            cliente_[1] = tienda_selected
        cliente_[6] = '1'
        cliente_[7] = '8'
        cliente_[9] = '2019-01-31'
        cliente_[10] = self.get_next_fecha(1)
        cliente_[11] = '0'
        title_ = "Ingresar cliente nuevo:"
        self.cliente_management(cliente_, title_, 0, 0)
    
    def cliente_management(self, cliente_, title, option, agg_ed):
        win = ncd.new_client_dialog(self.main_window, title, self.cb_fechas.GetStringSelection(), cliente_)
        new_client_ = 0
        while new_client_ == 0:
            btn_pressed = win.ncd_dialog.ShowModal()
            if btn_pressed == wx.ID_OK:
                new_client_ = win.Onagregar_Editar(option, agg_ed)
                if new_client_ == 1:
                    i = self.cb_fechas.GetStringSelection()
                    self.clientes = db.fetch_data_clientes(i)
                    self.tiendas = np.unique(self.clientes[:,1])#db.fetch_all_tiendas_from_table(self.fechas[0])
                    self.tiendas = np.insert(self.tiendas, 0, 'TODAS', axis=0)
                    self.mis_comisiones = db.fetch_all_comisiones()
                    self.cb_tiendas.Clear()

                    for tienda in self.tiendas:
                        self.cb_tiendas.Append(tienda)
                    self.cb_tiendas.SetValue(win.new_cliente[0])

                    clientes_select = self.clientes[np.where(self.clientes[:,1] == win.new_cliente[0])]

                    self.tabla_tiendas.update_tabla_tiendas(clientes_select, self.mis_comisiones, self.cb_fechas.GetStringSelection())
                    self.update_totales(clientes_select)
            else:
                new_client_ = 1
                
        win.ncd_dialog.Destroy()


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

    def OnDeleteClient(self, e):
        dlg = wx.TextEntryDialog(self.main_window, 'Ingresa el numero de cliente a eliminar:', 'Eliminar Cliente')
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
            title_ = "Eliminar cliente:"
            self.cliente_management(_cliente, title_, 2, no_cliente)

    def update_totales(self, clientes):
        fecha_obj = datetime.datetime.strptime(self.cb_fechas.GetStringSelection(), "%d_%b_%Y")
        unique_tiendas = np.unique(clientes[:,1])
        totales = []
        for tienda in unique_tiendas:
            clientes_por_tienda = clientes[np.where(clientes[:,1] == tienda)]
            clientes_por_tienda = clientes_por_tienda[np.where(clientes_por_tienda[:,10] <= fecha_obj.date())]
            total = np.sum(clientes_por_tienda[:,8])
            mi_comision = np.where(self.mis_comisiones == tienda)[0][0]
            mi_comision = (int(self.mis_comisiones[mi_comision,2])/100.0) * total
            a_pagar = total - mi_comision
            totales.append([total, mi_comision, a_pagar])
        totales = np.asarray(totales)

        comisiones_distr = np.sum(clientes[:,8] * (clientes[:,11]/100.0))

        self.total_minimos.SetLabel(str('$ ' + "{0:,.2f}".format(np.sum(totales[:,0]))))
        self.total_comision.SetLabel(str('$ ' + "{0:,.2f}".format(np.sum(totales[:,1]))))
        self.total_distr_com.SetLabel(str('$ ' + "{0:,.2f}".format(comisiones_distr)))
        self.total_ingreso.SetLabel(str('$ ' + "{0:,.2f}".format(np.sum(totales[:,1]) - comisiones_distr)))
        self.total_pagar.SetLabel(str('$ ' + "{0:,.2f}".format(np.sum(totales[:,2]))))

    def On_Editar(self, cliente_):
        err = 0
        try:
            tienda = cliente_[1]
            if not tienda:
                raise ValueError('empty string')
            err = 1
            distribuidor = cliente_[2]
            if not distribuidor:
                raise ValueError('empty string')
            err = 2
            cliente = cliente_[3]
            if not cliente:
                raise ValueError('empty string')
            err = 3
            folio = cliente_[4]
            if not folio:
                raise ValueError('empty string')
            err = 4
            compra_total = float(cliente_[5].strip('$'))
            err = 5
            qinicial = int(cliente_[6])
            err = 6
            qfinal = int(cliente_[7])
            err = 7
            if qinicial > qfinal:
                raise ValueError('quincena inicial debe ser menor que final')
            err = 8
            minimo = float(cliente_[8].strip('$'))
            err = 9
            date_ = datetime.datetime.strptime(cliente_[9], "%d_%b_%Y")
            fechac = datetime.datetime.strftime(date_, "%Y-%m-%d")
            err = 10
            date_ = datetime.datetime.strptime(cliente_[10], "%d_%b_%Y")
            fechap = datetime.datetime.strftime(date_, "%Y-%m-%d")
            err = 11
            if fechap < fechac:
                raise ValueError('fechap es menor que fechac')
            err = 12
            comision = int(cliente_[12].strip('%'))

            new_cliente = [str(tienda).upper(), distribuidor.upper(), cliente.upper(), str(folio).upper(), str(compra_total).upper(), str(qinicial).upper(), str(qfinal).upper(), str(minimo).upper(), str(fechac).upper(), str(fechap).upper(), str(comision).upper()]
            db.editar_cliente(self.cb_fechas.GetStringSelection(), new_cliente, cliente_[0])

            return 1

        except ValueError:
            _error = {
                0 : u'El campo "TIENDA" est\u00E1 vac\u00EDo, ingresa uno.',
                1 : u'El campo "DISTRIBUIDOR" est\u00E1 vac\u00EDo, ingresa uno.',
                2 : u'El campo "CLIENTE" est\u00E1 vac\u00EDo, ingresa uno..',
                3 : u'El campo "FOLIO" est\u00E1 vac\u00EDo, ingresa uno..',
                4 : u'"COMPRA TOTAL" debe contener solo digitos \u00F3 el campo est\u00E1 vac\u00EDo.',
                5 : u'"QUINCENA INICIAL" debe contener solo digitos \u00F3 el campo est\u00E1 vac\u00EDo.',
                6 : u'"QUINCENA FINAL" debe contener solo digitos \u00F3 el campo est\u00E1 vac\u00EDo.',
                7 : u'"QUINCENA FINAL" no puede ser menor que la quincena inicial.',
                8 : u'"PAGO M\u00CDNIMO" debe contener solo digitos \u00F3 el campo est\u00E1 vac\u00EDo.',
                9 : u'La "FECHA DE COMPRA" debe ser en el formato "2019-12-31" \u00F3 el campo est\u00E1 vac\u00EDo.',
                10 : u'La "FECHA DE INICIO" debe ser en el formato "2019-12-31" \u00F3 el campo est\u00E1 vac\u00EDo.',
                11 : u'La "FEHCA DE PRIMER PAGO" no puede ser anterior a la fecha de compra.',
                12 : u'La "COMISI\u00D3N" debe contener solo digitos \u00F3 el campo est\u00E1 vac\u00EDo.',
            }[err]
            wx.MessageBox(_error, 'Error', wx.OK | wx.ICON_ERROR)
            return 0
