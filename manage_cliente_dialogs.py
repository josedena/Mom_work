import wx
from dateutil.parser import parse
import datetime
import query_database as db

class new_client_dialog:
    def __init__(self, main_window, title_ ,fecha_, cliente_):
        self.fecha_ = fecha_
        self.new_cliente = []
        self.ncd_dialog = wx.Dialog(main_window ,title = title_, size = (350,500)) 
        self.ncd_dialog.Centre()
        panel = wx.Panel(self.ncd_dialog)
        vbox = wx.BoxSizer(wx.VERTICAL)

        vbox_2 = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(wx.StaticText(panel, label='Tienda:'))
        self.txt_tienda = wx.TextCtrl(panel, value=cliente_[1])
        hbox1.Add(self.txt_tienda, flag=wx.LEFT, border=5)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.Add(wx.StaticText(panel, label='Distribuidor:'))
        self.txt_distr = wx.TextCtrl(panel, value=cliente_[2])
        hbox2.Add(self.txt_distr, flag=wx.LEFT, border=5)

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3.Add(wx.StaticText(panel, label='Cliente: '))
        self.txt_cliente = wx.TextCtrl(panel, size=(270, 25), value=cliente_[3])
        hbox3.Add(self.txt_cliente, flag=wx.LEFT, border=5)

        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        hbox4.Add(wx.StaticText(panel, label='Folio:'))
        self.txt_folio = wx.TextCtrl(panel, value=cliente_[4])
        hbox4.Add(self.txt_folio, flag=wx.LEFT, border=5)

        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        hbox5.Add(wx.StaticText(panel, label='Compra total:'))
        self.txt_total = wx.TextCtrl(panel, value=cliente_[5])
        hbox5.Add(self.txt_total, flag=wx.LEFT, border=5)

        hbox6 = wx.BoxSizer(wx.HORIZONTAL)
        hbox6.Add(wx.StaticText(panel, label='Quincena Inicial:'))
        self.txt_qinicial = wx.TextCtrl(panel, value=cliente_[6])
        hbox6.Add(self.txt_qinicial, flag=wx.LEFT, border=5)

        hbox7 = wx.BoxSizer(wx.HORIZONTAL)
        hbox7.Add(wx.StaticText(panel, label='Quincenas totales:'))
        self.txt_qfinal = wx.TextCtrl(panel, value=cliente_[7])
        hbox7.Add(self.txt_qfinal, flag=wx.LEFT, border=5)

        hbox8 = wx.BoxSizer(wx.HORIZONTAL)
        hbox8.Add(wx.StaticText(panel, label=u'Pago m\u00EDnimo:'))
        self.txt_minimo = wx.TextCtrl(panel, value=cliente_[8])
        hbox8.Add(self.txt_minimo, flag=wx.LEFT, border=5)

        hbox9 = wx.BoxSizer(wx.HORIZONTAL)
        hbox9.Add(wx.StaticText(panel, label='Fecha de compra:'))
        self.txt_fechac = wx.TextCtrl(panel, value=cliente_[9])
        hbox9.Add(self.txt_fechac, flag=wx.LEFT, border=5)

        hbox10 = wx.BoxSizer(wx.HORIZONTAL)
        hbox10.Add(wx.StaticText(panel, label='Fecha primer pago:'))
        self.txt_fechap = wx.TextCtrl(panel, value=cliente_[10])
        hbox10.Add(self.txt_fechap, flag=wx.LEFT, border=5)

        hbox11 = wx.BoxSizer(wx.HORIZONTAL)
        hbox11.Add(wx.StaticText(panel, label=u'Comisi\u00F3n para distribuidor:'))
        self.txt_comision = wx.TextCtrl(panel, value=cliente_[11])
        hbox11.Add(self.txt_comision, flag=wx.LEFT, border=5)

        vbox_2.Add(hbox1, 1)
        vbox_2.Add(hbox2, 1)
        vbox_2.Add(hbox3, 1)
        vbox_2.Add(hbox4, 1)
        vbox_2.Add(hbox5, 1)
        vbox_2.Add(hbox6, 1)
        vbox_2.Add(hbox7, 1)
        vbox_2.Add(hbox8, 1)
        vbox_2.Add(hbox9, 1)
        vbox_2.Add(hbox10, 1)
        vbox_2.Add(hbox11, 1)
        panel.SetSizer(vbox_2)

        hbox_b = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self.ncd_dialog, id=wx.ID_OK ,label='Aceptar')
        okButton.SetDefault()
        okButton.SetFocus()
        closeButton = wx.Button(self.ncd_dialog, id=wx.ID_CANCEL ,label='Cancelar')

        hbox_b.Add(okButton, flag=wx.LEFT, border=5)
        hbox_b.Add(closeButton, flag=wx.LEFT, border=5)

        vbox.Add(panel, proportion=1, flag=wx.ALL|wx.EXPAND, border=5)
        vbox.Add(hbox_b, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)

        self.ncd_dialog.SetSizer(vbox)

    def Onagregar_Editar(self, option, cliente_no):
        err = 0
        try:
            tienda = self.txt_tienda.GetValue()
            if not tienda:
                raise ValueError('empty string')
            err = 1
            distribuidor = self.txt_distr.GetValue()
            if not distribuidor:
                raise ValueError('empty string')
            err = 2
            cliente = self.txt_cliente.GetValue()
            if not cliente:
                raise ValueError('empty string')
            err = 3
            folio = self.txt_folio.GetValue()
            if not folio:
                raise ValueError('empty string')
            err = 4
            compra_total = float(self.txt_total.GetValue())
            err = 5
            qinicial = int(self.txt_qinicial.GetValue())
            err = 6
            qfinal = int(self.txt_qfinal.GetValue())
            err = 7
            if qinicial > qfinal:
                raise ValueError('quincena inicial debe ser menor que final')
            err = 8
            minimo = float(self.txt_minimo.GetValue())
            err = 9
            if self.is_date(self.txt_fechac.GetValue()):
                fechac = self.txt_fechac.GetValue()
            err = 10
            if self.is_date(self.txt_fechap.GetValue()):
                fechap = self.txt_fechap.GetValue()
            err = 11
            if fechap < fechac:
                raise ValueError('fechap es menor que fechac')
            err = 12
            comision = int(self.txt_comision.GetValue())

            self.new_cliente = [str(tienda).upper(), distribuidor.upper(), cliente.upper(), str(folio).upper(), str(compra_total).upper(), str(qinicial).upper(), str(qfinal).upper(), str(minimo).upper(), str(fechac).upper(), str(fechap).upper(), str(comision).upper()]
            if option == 0:
                db.insertar_cliente(self.fecha_, self.new_cliente)
            if option == 1:
                db.editar_cliente(self.fecha_, self.new_cliente, cliente_no)
            if option == 2:            
                message_ = "Estas seguro que deseas eliminar al cliente " + cliente_no + "?"
                dlg = wx.MessageDialog(None, message_,'Eliminar cliente',wx.OK| wx.CANCEL | wx.ICON_QUESTION)
                result = dlg.ShowModal()
                if result == wx.ID_OK:
                    db.delete_cliente(self.fecha_, cliente_no)
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

    def is_date(self, string):
        try: 
            parse(string)
            return True
        except ValueError:
            return False
