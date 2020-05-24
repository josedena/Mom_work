import wx
import relaciones_tiendas as rt
import relaciones_distribuidores as rd
import edit_tiendas_com as ed_tiendas
import importar_relaciones as imp_rel
import imprimir_relaciones as print_rel
import math
import locale

class Menu_principal:
    def __init__(self, main_window):
        self.main_win = main_window
        self.main_win.CreateStatusBar()
        #locale.setlocale(locale.LC_ALL, 'spanish')
        self.locale = wx.Locale(wx.LANGUAGE_SPANISH)

        menuFile = wx.Menu()
        item = menuFile.Append(-1, "&Relaciones Tiendas", "Administrador de las Relaciones.")
        self.main_win.Bind(wx.EVT_MENU, self.OnRelaciones_tiendas, item)
        item = menuFile.Append(-1, "Relaciones Distribuidores", "Administrador de las tiendas.")
        self.main_win.Bind(wx.EVT_MENU, self.OnRelaciones_distribuidores, item)
        item = menuFile.Append(-1, u"Editar Mi comision Tiendas", u"Editor de la comision que recibo de las tiendas.")
        self.main_win.Bind(wx.EVT_MENU, self.OnEditar_tiendas, item)
        item = menuFile.Append(-1, "Importar Registros(.xls)", "Importar registros de quincenas previas.")
        self.main_win.Bind(wx.EVT_MENU, self.OnImportar_datos, item)
        menuFile.AppendSeparator()
        item = menuFile.Append(wx.ID_ABOUT, "&Sobre Aplicacion", u"Informacion sobre la aplicacion.")
        self.main_win.Bind(wx.EVT_MENU, self.OnAbout, item)
        item = menuFile.Append(wx.ID_EXIT, "&Salir", u"Cerrar esta aplicacion.")
        self.main_win.Bind(wx.EVT_MENU, self.OnQuit, item)

        menu_imprimir = wx.Menu()
        item = menu_imprimir.Append(-1, u"Configuracion de pagina...\tF5", "Configurar margenes, tipo de hoja, etc.")
        self.main_win.Bind(wx.EVT_MENU, self.OnPageSetup, item)
        item = menu_imprimir.Append(-1, "Vista previa...\tF6", "Ver el documento final antes de imprimir.")
        self.main_win.Bind(wx.EVT_MENU, self.OnPrintPreview, item)
        item = menu_imprimir.Append(-1, "Imprimir...\tF7", "Imprimir el documento.")
        self.main_win.Bind(wx.EVT_MENU, self.OnPrint, item)
        item = menu_imprimir.Append(-1, "Exportar...\tF8", "Exportar el documento a (.xls).")
        self.main_win.Bind(wx.EVT_MENU, self.OnExport, item)
        menu_imprimir.AppendSeparator()

        self.menuBar = wx.MenuBar()
        self.menuBar.Append(menuFile, "&Inicio")
        self.menuBar.Append(menu_imprimir, "&Imprimir")
        self.main_win.SetMenuBar(self.menuBar)

        self.main_win.SetStatusText(u"Bienvenido a la aplicacion DISTRIBUIDORES!!")

        self.rel_tiendas = rt.relaciones_tiendas(self.main_win)
        self.rel_distr  = rd.relaciones_distribuidores(self.main_win)
        self.rel_distr.Hide()
        #self.rel_tiendas.Hide()
        self.menuBar.EnableTop(1, False)

        self.main_win.sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_win.sizer.Add(self.rel_tiendas, 1, wx.EXPAND)
        self.main_win.sizer.Add(self.rel_distr, 1, wx.EXPAND)
        self.main_win.SetSizer(self.main_win.sizer)

        # initialize the print data and set some default values
        self.pdata = wx.PrintData()
        self.pdata.SetPaperId(wx.PAPER_A4)
        self.pdata.SetOrientation(wx.PORTRAIT)
        self.pdata.SetPrinterName('')
        self.pdata.SetColour(False)
        self.pdata.SetNoCopies(1)
        self.margins = (wx.Point(3,3), wx.Point(3,3))


    def OnQuit(self, event):
        self.main_win.Close()

    def OnAbout(self, event):
        wx.MessageBox("Aplicacion desarrollada para uso personal.\n"
            " Soporte: josea.denar@live.com\n"
            " Version 1.0 \n", "Acerca de Distribuidores",
            wx.OK | wx.ICON_INFORMATION, self.main_win)

    def OnImportar_datos(self, event):
        openFileDialog = wx.FileDialog(self.main_win, "Abrir", "", "", "Excel files (*.xls)|*.xls", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if openFileDialog.ShowModal() != wx.ID_CANCEL:
            imp_rel.importar_datos_from_excel(openFileDialog.GetPath(), openFileDialog.GetFilename())
            openFileDialog.Destroy()
            self.rel_distr.update_all()
            self.rel_tiendas.update_all()

    def OnRelaciones_tiendas(self, event):
        self.rel_distr.Hide()
        self.menuBar.EnableTop(1, False)
        self.main_win.SetTitle("Relaciones Tiendas")
        self.rel_tiendas.update_all()
        self.rel_tiendas.Show()
        self.main_win.Layout()

    def OnRelaciones_distribuidores(self, event):
        self.rel_tiendas.Hide()
        self.menuBar.EnableTop(1, True)
        self.main_win.SetTitle("Relaciones Distribuidores")
        self.rel_distr.update_all()
        self.rel_distr.Show()
        self.main_win.Layout()

    def OnEditar_tiendas(self, event):
        edit_tiendas = ed_tiendas.edit_tiendas_dialog(self.main_win, "Editar Comision en Tiendas")
        if edit_tiendas.ed_tiendas_dialog.ShowModal() == wx.ID_OK:
            edit_tiendas.On_aceptar_btn()   

    def OnPageSetup(self, evt):
        data = wx.PageSetupDialogData()
        data.SetPrintData(self.pdata)
        data.SetDefaultMinMargins(True)
        data.SetMarginTopLeft(self.margins[0])
        data.SetMarginBottomRight(self.margins[1])

        dlg = wx.PageSetupDialog(self.main_win, data)
        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetPageSetupData()
            self.pdata = wx.PrintData(data.GetPrintData()) # force a copy
            self.pdata.SetPaperId(data.GetPaperId())
            #print_("paperID %r, paperSize %r" % (self.pdata.GetPaperId(), self.pdata.GetPaperSize()))
            self.margins = (data.GetMarginTopLeft(),
                            data.GetMarginBottomRight())
        dlg.Destroy()


    def OnPrintPreview(self, evt):
        data = wx.PrintDialogData(self.pdata)
        text = self.rel_distr.get_data_from_cells()
        printout1 = print_rel.TextDocPrintout(text, "title", self.margins)
        printout2 = print_rel.TextDocPrintout(text, "title", self.margins)
        data.SetMinPage(1)
        data.SetMaxPage(math.ceil(len(text)/96))
        preview = wx.PrintPreview(printout1, printout2, data)
        
        if "__WXMAC__" in wx.PlatformInfo:
            preview.SetZoom(170)
        else:
            preview.SetZoom(100)

        if not preview:
            wx.MessageBox("No se puede crear la vista previa!", "Error")
        else:
            # create the preview frame such that it overlays the app frame
            frame = wx.PreviewFrame(preview, self.main_win, "Vista previa de impresion.",
                                    pos=self.main_win.GetPosition(),
                                    size=self.main_win.GetSize())
            frame.Initialize()
            frame.Show()


    def OnPrint(self, evt):
        text = self.rel_distr.get_data_from_cells()
        printout = print_rel.TextDocPrintout(text, "title", self.margins)
        data = wx.PrintDialogData(self.pdata)
        data.SetMinPage(1)
        data.SetMaxPage(math.ceil(len(text)/96))
        printer = wx.Printer(data)  
        useSetupDialog = True
        if not printer.Print(self.main_win, printout, useSetupDialog) \
           and printer.GetLastError() == wx.PRINTER_ERROR:
            wx.MessageBox(
                "Hubo un problema al imprimir.\n"
                "Quiza la imporesora no esta instalada correctamente?",
                "Error al imprimir", wx.OK)
        else:
            data = printer.GetPrintDialogData()
            self.pdata = wx.PrintData(data.GetPrintData()) # force a copy
        printout.Destroy()   

    def OnExport(self, evt):
        with wx.FileDialog(self.main_win, "Guardar archivo Excel", wildcard="Archivos Excel (*.xls)|*.xls",style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind
            # save the current contents in the file
            pathname = fileDialog.GetPath()
            try:
                self.rel_distr.export_data_from_cells(pathname)
            except IOError:
                wx.LogError("No se puede guardar el archivo '%s'." % pathname)