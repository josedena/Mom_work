import wx
from dateutil.parser import parse
import datetime
import numpy as np

class select_which_tiendas:
    def __init__(self, main_window, title_ , tiendas):
        self.new_tiendas_select = tiendas
        self.new_tiendas_select  = np.delete(self.new_tiendas_select , np.argwhere(self.new_tiendas_select  == "TODAS"))
        self.stnq_dialog = wx.Dialog(main_window ,title = title_, size = (350,500)) 
        self.stnq_dialog.Centre()
        panel = wx.Panel(self.stnq_dialog)
        vbox = wx.BoxSizer(wx.VERTICAL)

        pos_y = 0
        self.cb = [None] * len(self.new_tiendas_select)
        for i in range(0, len(self.new_tiendas_select)):
            pos_y += 30
            self.cb[i] = wx.CheckBox(panel, label=self.new_tiendas_select[i], pos=(20, pos_y))
            self.cb[i].SetValue(True)        

        hbox_b = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self.stnq_dialog, id=wx.ID_OK ,label='Aceptar')
        okButton.SetDefault()
        okButton.SetFocus()
        closeButton = wx.Button(self.stnq_dialog, id=wx.ID_CANCEL ,label='Cancelar')

        hbox_b.Add(okButton, flag=wx.LEFT, border=5)
        hbox_b.Add(closeButton, flag=wx.LEFT, border=5)

        vbox.Add(panel, proportion=1, flag=wx.ALL|wx.EXPAND, border=5)
        vbox.Add(hbox_b, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)

        self.stnq_dialog.SetSizer(vbox)

        self.stnq_dialog.Bind(wx.EVT_CHECKBOX,self.onChecked) 
        self.stnq_dialog.Centre() 
        self.stnq_dialog.Show(True) 

    def onChecked(self, e): 
        cb = e.GetEventObject()
        if cb.GetValue() == True:
            self.new_tiendas_select = np.append(self.new_tiendas_select, cb.GetLabel())
        else:
            self.new_tiendas_select  = np.delete(self.new_tiendas_select , np.argwhere(self.new_tiendas_select  == cb.GetLabel()))
        print(self.new_tiendas_select)