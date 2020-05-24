from mysql.connector import MySQLConnection, Error
from DataBase_config import read_db_config
import wx
import datetime
import numpy as np
 
def new_table_quinc(last, new, check_list ):
    try:
        error_ = 0
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM " + last)#06_Abril_2019
        clientes = cursor.fetchall()
        clientes = [list(elem) for elem in clientes]  
        resto_clientes = []
        new_date = datetime.datetime.strptime(new, "%d_%b_%Y")
        new_date = datetime.date(new_date.year, new_date.month, new_date.day)
        for cliente in clientes:
            if cliente[10] <= new_date:
                if cliente[1] in check_list:
                    cliente[6] =  cliente[6] + 1
                if cliente[6] <= cliente[7]:
                    resto_clientes.append(cliente)
                else:
                    print ("cliente fuera por quincena: ")
                    print (cliente)
            else:
                print ("cliente sin avance por fecha: ")
                resto_clientes.append(cliente)
                print (cliente)
        
        cursor.execute("CREATE TABLE " + new + " LIKE " + last )
        for data in resto_clientes:
            query = "INSERT INTO " + str(new) + " (tienda, distribuidor, nombre_cliente, folio, compra_total, quincena_actual, quincenas_totales, pago_minimo, fecha_compra, fecha_primer_pago, porcentaje_comision) VALUES ('" + str(data[1]).upper() + "','" + str(data[2]).upper() + "','" + str(data[3]).upper() + "','" + str(data[4]).upper() + "','" + str(data[5]).upper() + "','"+ str(data[6]).upper() + "','" + str(data[7]).upper() + "','" + str(data[8]).upper() + "','" + str(data[9]).upper() + "','" + str(data[10]).upper() + "','" + str(data[11]).upper() + "')" 
            cursor.execute(query)
            conn.commit()     
 
    except Error as e:
        wx.MessageBox(e, 'Error', wx.OK | wx.ICON_ERROR)
        print(e)
        error_ = 1
 
    finally:
        cursor.close()
        conn.close()
        if error_ == 1:
            data_ = []
            return data
        else:
            return np.asarray(resto_clientes)

def import_data_to_database(new, clientes):
    try:
        error_ = 0
        fechas = fetch_all_tables()

        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor() 

        cursor.execute("CREATE TABLE " + new + " LIKE " + fechas[0])
        for data in clientes:
            fecha_compra = datetime.datetime.strptime(data[8], "%d_%b_%Y")
            fecha_compra = datetime.datetime.strftime(fecha_compra, "%Y-%m-%d")
            fecha_inicio = datetime.datetime.strptime(data[9], "%d_%b_%Y")
            fecha_inicio = datetime.datetime.strftime(fecha_inicio, "%Y-%m-%d")
            query = "INSERT INTO " + str(new) + " (tienda, distribuidor, nombre_cliente, folio, compra_total, quincena_actual, quincenas_totales, pago_minimo, fecha_compra, fecha_primer_pago, porcentaje_comision) VALUES ('" + str(data[0]).upper() + "','" + str(data[1]).upper() + "','" + str(data[2]).upper() + "','" + str(data[3]).upper() + "','" + str(data[4]).upper() + "','"+ str(data[5]).upper() + "','" + str(data[6]).upper() + "','" + str(data[7]).upper() + "','" + str(fecha_compra) + "','" + str(fecha_inicio) + "','" + str(data[10]).upper() + "')" 
            cursor.execute(query)
            conn.commit()     
 
    except Error as e:
        wx.MessageBox(e, 'Error', wx.OK | wx.ICON_ERROR)
        print(e)
        error_ = 1
 
    finally:
        cursor.close()
        conn.close()
        return error_

def fetch_data_clientes(fecha):
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM " + fecha.lower() + " ORDER BY tienda ASC, nombre_cliente ASC, fecha_compra DESC")#06_Abril_2019
 
        clientes = cursor.fetchall()
 
    except Error as e:
        wx.MessageBox(e, 'Error', wx.OK | wx.ICON_ERROR)
        print(e)
 
    finally:
        cursor.close()
        conn.close()
        return np.asarray(clientes)

def fetch_comision_tiendas():
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM comision_por_tiendas")
 
        tiendas = cursor.fetchall()
 
    except Error as e:
        wx.MessageBox(e, 'Error', wx.OK | wx.ICON_ERROR)
        print(e)
 
    finally:
        cursor.close()
        conn.close()
        return tiendas

def fetch_clientes_por_distribuidor(fecha, distrdor, tienda):
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        if tienda == "TODAS":
            cursor.execute("SELECT * FROM " + fecha.lower() + " WHERE distribuidor = '" + distrdor + "'" + " ORDER BY tienda ASC, nombre_cliente ASC, fecha_compra DESC")#06_Abril_2019
        else:
            cursor.execute("SELECT * FROM " + fecha.lower() + " WHERE distribuidor = '" + distrdor + "' AND tienda = '" + tienda + "'"+ " ORDER BY tienda ASC, nombre_cliente ASC, fecha_compra DESC")
        clientes = cursor.fetchall()
        clientes = np.asarray(clientes)
        _date = datetime.datetime.strptime(fecha.lower(), "%d_%b_%Y")
        _date = datetime.date(_date.year, _date.month, _date.day)
        clientes = clientes[np.where(clientes[:,2] <= _date)]
 
    except Error as e:
        wx.MessageBox(e, 'Error', wx.OK | wx.ICON_ERROR)
        print(e)
 
    finally:
        cursor.close()
        conn.close()
        return clientes.tolist()

def fetch_all_tables():
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tablas = []
        tables_ = cursor.fetchall()
        for tabla in range(0,len(tables_)):
            tablas.append(str(tables_[tabla][0]).upper())
        tablas.remove('COMISION_POR_TIENDAS')
 
    except Error as e:
        wx.MessageBox(e, 'Error', wx.OK | wx.ICON_ERROR)
        print(e)
 
    finally:
        cursor.close()
        conn.close()
        return tablas

def fetch_all_distr_from_table(table):
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT distribuidor FROM " + table)
        distrs = []
        #tiendas.append('TODAS')
        distrs_ = cursor.fetchall()
        for distr_ in range(0,len(distrs_)):
            distrs.append(distrs_[distr_][0])
 
    except Error as e:
        wx.MessageBox(e, 'Error', wx.OK | wx.ICON_ERROR)
        print(e)
 
    finally:
        cursor.close()
        conn.close()
        return np.asarray(distrs)

def fetch_all_tiendas_from_distr(fecha, distrdor):
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT tienda FROM " + fecha.lower() + " WHERE distribuidor = '" + distrdor+ "'")
        tiendas = []
        tiendas.append('TODAS')
        tiendas_ = cursor.fetchall()
        for tienda in range(0,len(tiendas_)):
            tiendas.append(tiendas_[tienda][0])
 
    except Error as e:
        wx.MessageBox(e, 'Error', wx.OK | wx.ICON_ERROR)
        print(e)
 
    finally:
        cursor.close()
        conn.close()
        return tiendas

def fetch_all_tiendas_from_table(table):
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT tienda FROM " + table)
        tiendas = []
        tiendas.append('TODAS')
        tiendas_ = cursor.fetchall()
        for tienda in range(0,len(tiendas_)):
            tiendas.append(tiendas_[tienda][0])
 
    except Error as e:
        wx.MessageBox(e, 'Error', wx.OK | wx.ICON_ERROR)
        print(e)
 
    finally:
        cursor.close()
        conn.close()
        return tiendas

def fetch_clientes_tienda(fecha, tienda):
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        query = "SELECT * FROM " + fecha.lower() + " WHERE tienda = '" + tienda + "'"
        cursor.execute(query)
 
        clientes = cursor.fetchall()
 
    except Error as e:
        wx.MessageBox(e, 'Error', wx.OK | wx.ICON_ERROR)
        print(e)
 
    finally:
        cursor.close()
        conn.close()
        return clientes

def fetch_one_cliente(fecha, no_cliente):
    try:
        error = 0
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        query = "SELECT * FROM " + fecha.lower() + " WHERE id = '" + no_cliente + "'"
        cursor.execute(query)
 
        cliente = cursor.fetchall()
 
    except Error as e:
        wx.MessageBox(e, 'Error', wx.OK | wx.ICON_ERROR)
        print(e)
        error = 1
 
    finally:
        cursor.close()
        conn.close()
        return cliente

def fetch_all_comisiones():
    try:
        dbconfig = read_db_config()
        error = 0
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        query = "SELECT * FROM comision_por_tiendas"
        cursor.execute(query)
        comisiones_ = cursor.fetchall()

    except Error as e:
        wx.MessageBox(e, 'Error', wx.OK | wx.ICON_ERROR)
        print(e)
        error = 1
 
    finally:
        cursor.close()
        conn.close()
        if error == 0:
            return np.asarray(comisiones_)

def insert_new_tienda(tienda, parent):
    continue_ = 0
    while (continue_ == 0):
        dlg = wx.TextEntryDialog(parent, 'La tienda '+tienda+' no tiene asignada tu comision, ingresa una:','Falta comision')
        if dlg.ShowModal() == wx.ID_OK:
            comision_dlg = dlg.GetValue()
            try:
                comisiones_ = [[int(comision_dlg)]]
                insertar_tienda_comision(tienda, comisiones_[0][0])
                continue_ = 1
            except ValueError:
                wx.MessageBox('Comision incorrecta. Ejemplo: para 10%, ingresa: 10', 'Error', wx.OK | wx.ICON_ERROR)
    dlg.Destroy() 

def fetch_comisiones(tienda, parent):
    try:
        dbconfig = read_db_config()
        error = 0
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        query = "SELECT comision FROM comision_por_tiendas WHERE tienda = '" + tienda + "'"
        cursor.execute(query)
        comisiones_ = cursor.fetchall()
        if comisiones_ == []:
            continue_ = 0
            while (continue_ == 0):
                dlg = wx.TextEntryDialog(parent, 'La tienda '+tienda+' no tiene asignada tu comision, ingresa una:','Falta comision')
                if dlg.ShowModal() == wx.ID_OK:
                    comision_dlg = dlg.GetValue()
                    try:
                        comisiones_ = [[int(comision_dlg)]]
                        insertar_tienda_comision(tienda, comisiones_[0][0])
                        continue_ = 1
                    except ValueError:
                        wx.MessageBox('Comision incorrecta. Ejemplo: para 10%, ingresa: 10', 'Error', wx.OK | wx.ICON_ERROR)
                dlg.Destroy() 
        #for comision in range(0,len(comisiones_)):

    except Error as e:
        wx.MessageBox(e, 'Error', wx.OK | wx.ICON_ERROR)
        print(e)
        error = 1
 
    finally:
        cursor.close()
        conn.close()
        if error == 0:
            return comisiones_[0][0]  

def delete_cliente(fecha, no_cliente):
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()

        query = "DELETE FROM " + fecha.lower() + " WHERE id = '" + no_cliente + "'"
        cursor.execute(query)
        conn.commit()
        #print ("Record inserted successfully into python_users table")
    except Error as e:
        conn.rollback() #rollback if any exception occured
        wx.MessageBox(e, 'Error', wx.OK | wx.ICON_ERROR)
        print("Failed inserting record into python_users table {}".format(e))
        return 0
    finally:
        #closing database connection.
        if(conn.is_connected()):
            cursor.close()
            conn.close()
        return 1

def insertar_cliente(fecha, data):
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()

        query = "INSERT INTO " + fecha.lower() + " (tienda, distribuidor, nombre_cliente, folio, compra_total, quincena_actual, quincenas_totales, pago_minimo, fecha_compra, fecha_primer_pago, porcentaje_comision) VALUES ('" + data[0] + "','" + data[1] + "','" + data[2] + "','" + data[3] + "','" + data[4] + "','"+ data[5] + "','" + data[6] + "','" + data[7] + "','" + data[8] + "','" + data[9] + "','" + data[10] + "')" 
        cursor.execute(query)
        conn.commit()
        #print ("Record inserted successfully into python_users table")
    except Error as e:
        conn.rollback() #rollback if any exception occured
        wx.MessageBox(e, 'Error', wx.OK | wx.ICON_ERROR)
        print("Failed inserting record into python_users table {}".format(e))
    finally:
        #closing database connection.
        if(conn.is_connected()):
            cursor.close()
            conn.close()

def editar_cliente(fecha, data, no_cliente):
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        query = "UPDATE " + fecha.lower() + " SET tienda = '" + data[0] + "', distribuidor = '" + data[1]+ "', nombre_cliente = '" + data[2] + "', folio = '" + data[3] + "', compra_total = '" + data[4] + "', quincena_actual = '" + data[5] + "', quincenas_totales = '" + data[6] + "', pago_minimo = '" + data[7] + "', fecha_compra = '" + data[8] + "', fecha_primer_pago = '" + data[9] + "', porcentaje_comision = '" + data[10] + "' WHERE id = '" + no_cliente + "';" 
        
        cursor.execute(query)
        conn.commit()
        #print ("Record inserted successfully into python_users table")
    except Error as e:
        conn.rollback() #rollback if any exception occured
        wx.MessageBox(e, 'Error', wx.OK | wx.ICON_ERROR)
        print("Failed inserting record into python_users table {}".format(e))
    finally:
        #closing database connection.
        if(conn.is_connected()):
            cursor.close()
            conn.close()

def insertar_tienda_comision(tienda, comision):
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        query = "INSERT INTO comision_por_tiendas (tienda, comision) VALUES ('" + tienda + "','" + str(comision) + "')" 
        cursor.execute(query)
        conn.commit()
        #print ("Record inserted successfully into python_users table")
    except Error as e:
        conn.rollback() #rollback if any exception occured
        wx.MessageBox(e, 'Error', wx.OK | wx.ICON_ERROR)
        print("Failed inserting record into python_users table {}".format(e))
    finally:
        #closing database connection.
        if(conn.is_connected()):
            cursor.close()
            conn.close()
    
def editar_tienda_comision(tienda, comision):
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        query = "UPDATE comision_por_tiendas SET comision = '" + str(comision) + "' WHERE tienda = '" + tienda +"'" 
        cursor.execute(query)
        conn.commit()
        #print ("Record inserted successfully into python_users table")
    except Error as e:
        conn.rollback() #rollback if any exception occured
        wx.MessageBox(e, 'Error', wx.OK | wx.ICON_ERROR)
        print("Failed inserting record into python_users table {}".format(e))
    finally:
        #closing database connection.
        if(conn.is_connected()):
            cursor.close()
            conn.close()
