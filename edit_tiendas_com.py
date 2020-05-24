import wx
import query_database as db
import numpy as np

class edit_tiendas_dialog:
    def __init__(self, main_window, title_):
        self.ed_tiendas_dialog = wx.Dialog(main_window ,title = title_, size = (200,200)) 
        self.ed_tiendas_dialog.Centre()
        tiendas = db.fetch_comision_tiendas()
        self.tiendas = np.asarray(tiendas)
        self.selection = 0

        panel = wx.Panel(self.ed_tiendas_dialog)

        self.cb_tiendas = wx.ComboBox(panel, choices=self.tiendas[:,1], style=wx.CB_READONLY)
        self.cb_tiendas.SetSelection(0)
        self.txt_tienda = wx.TextCtrl(panel, value=self.tiendas[0,2])

        okButton = wx.Button(panel, id=wx.ID_OK ,label='Aceptar')
        closeButton = wx.Button(panel, id=wx.ID_CANCEL ,label='Cancelar')

        hbox_b = wx.BoxSizer(wx.HORIZONTAL)
        hbox_b.Add(okButton, 0, wx.EXPAND|wx.ALL, 10)
        hbox_b.Add(closeButton, 0, wx.EXPAND|wx.ALL, 10)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.cb_tiendas, 0, wx.EXPAND|wx.ALL, 10)
        vbox.Add(self.txt_tienda, 0, wx.EXPAND|wx.ALL, 10)
        vbox.Add(hbox_b, 0, wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, 10)
        panel.SetSizer(vbox)

        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox1.Add(panel, 0, wx.EXPAND, 0)
        self.ed_tiendas_dialog.SetSizer(vbox1)

        self.cb_tiendas.Bind(wx.EVT_COMBOBOX, self.CB_tiendas_OnSelect)

    def CB_tiendas_OnSelect(self, e):
        self.tiendas[self.selection,2] = self.txt_tienda.GetValue()
        self.selection = e.GetSelection()
        self.txt_tienda.SetValue(self.tiendas[self.selection,2])

    def On_aceptar_btn(self):
        for row in range(0, self.tiendas.shape[0]):
            tienda = self.tiendas[row,1]
            comision = self.tiendas[row,2]
            db.editar_tienda_comision(tienda, comision)