#!/usr/bin/env python3

import wx 
from Menu_frame import Menu_principal

class main_Form(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, title="DISTRIBUIDORES", size = (1290,750))
        menu = Menu_principal(self)
        
if __name__ == '__main__':
    
    app = wx.App(0)
    main_window = main_Form()
    main_window.Center()
    main_window.Show()
    app.MainLoop()