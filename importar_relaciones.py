import numpy as np
#import xlwt
import xlrd
import datetime
import query_database as db
import wx

def importar_datos_from_excel(file_path, file_name):
    file_, sep, tail = file_name.partition('.')
    file_.lower()
    file_ = file_.replace("-","_")

    fechas = db.fetch_all_tables()
    if file_.upper() in fechas:
        wx.MessageBox('El archivo del '+ file_.upper() + ' ya se encuentra en la base datos.', 'Error', wx.OK | wx.ICON_ERROR)
    else:
        data = xlrd.open_workbook("distribuidores.xls")   
        table = data.sheets()[0]
        tabla = []
        dstrdr = []
        for row in range(0, table.nrows):
                for col in range(0, table.ncols):
                    dstrdr.append(table.cell(row,col).value)
                tabla.append(dstrdr)
                dstrdr = []

        comision_distr = np.array(tabla)

        data = xlrd.open_workbook(file_path)
        clientes= []
        for tienda in range(0, len(data.sheets())):
            table = data.sheets()[tienda]
            rows = table.nrows
            cols = table.ncols
            print (data.sheet_names()[tienda])
            for row in range(0, rows):
                print (table.cell(row,1).value)
                fecha_compra = xlrd.xldate.xldate_as_datetime(table.cell(row,8).value, data.datemode)
                #fecha_compra = datetime.datetime.strptime(table.cell(row,7).value, "%d.%m.%Y")
                fecha_compra = datetime.datetime.strftime(fecha_compra, "%d_%b_%Y")
                if isinstance(table.cell(row,2).value, str):
                    folio = str(table.cell(row,2).value)
                else:
                    folio = int(table.cell(row,2).value)
                try:
                    comision = int(float(comision_distr[np.where(comision_distr == table.cell(row,0).value)[0][0], np.where(comision_distr == data.sheet_names()[tienda])[1][0]]))
                except:
                    comision = 0
                clientes.append([data.sheet_names()[tienda], table.cell(row,0).value, table.cell(row,1).value, folio, table.cell(row,3).value, int(table.cell(row,4).value), int(table.cell(row,5).value), table.cell(row,6).value, fecha_compra.upper(), file_.upper(), comision])
        
        error = db.import_data_to_database(file_, clientes)
