import pyodbc
import wx
import Read_And_Write_Files
import GUI
import time
import datetime

def __new__showMessageDlg(self, msg, title):
    """""",
    dlg = wx.MessageDialog(parent=None, message=msg,
                               caption=title, style=wx.OK | wx.CANCEL | wx.ICON_QUESTION)
    dlg.ShowModal()
    dlg.Destroy()

class SQLCon():
    def __new__(self, server_in, database_in, username_in, password_in, driver_in, port_in):

        server = server_in
        database = database_in
        username = username_in
        password = password_in
        driver = driver_in
        port = port_in

        ConString = ('DRIVER='+driver+';PORT=' + port + ';SERVER='+server+';PORT=' + port + ';DATABASE='+database+';UID='+username+';PWD='+password)

        cnxn = pyodbc.connect('DRIVER='+driver+';PORT=' + port + ';SERVER='+server+';PORT=' + port + ';DATABASE='+database+';UID='+username+';PWD='+password)

        cursor = cnxn.cursor()
        return(cursor)

class SQLCreateTable():
    def __new__(self, open_con, table_name, column_list):
        pal = ''
        for x in range(len(column_list)):

            if x == (len(column_list))-1:
                column_name_and_data = ' ' + (column_list[0][x]) + ' ' + (column_list[1][x])
                combine_string = str(combine_string) + str(column_name_and_data)
            else:
                column_name_and_data = ' ' + (column_list[0][x]) + ' ' + (column_list[1][x]) + ','
                combine_string = str(combine_string) + str(column_name_and_data)

        create_string = "CREATE TABLE " + table_name + "(" + pal + ")"
        open_con.execute(create_string)
        open_con.commit()


class SQLSearchAll():
    def __new__(self, open_con, user_con, username, table_name, column_of_condition, condition):
        search_all = "SELECT * FROM " + table_name
        open_con.execute(search_all)
        row = open_con.fetchall()
        #---------------------------------------------------------------------------------------------------------
        # Update the user_log with the querry
        # ---------------------------------------------------------------------------------------------------------
        new_id_generated = SQLGenerateNewID(user_con, 'User_Logs')
        # Get date at time
        now = datetime.datetime.now()
        date_now = now.date()
        time_now = now.time()
        # Create list for user log insert
        user_list = (
        new_id_generated, username, 'Display all data in the table', table_name, condition,
        str(date_now), str(time_now))
        # Execute insert string
        SQLInsertInto(user_con, "", "", 'User_Logs', user_list)
        return (row)

class SQLSearchColumnSingleEntry():
    def __new__(self, open_con, username, table_name, column_of_condition, condition):
        single_row_string = "SELECT " + column_of_condition + " FROM " + table_name + " WHERE " + column_of_condition \
                            + " LIKE '" + condition + "%%'"
        open_con.execute(single_row_string)
        row = open_con.fetchone()
        #open_con.close()
        return (row)

class SQLSearchColumnMutipleEntry():
    def __new__(self, open_con, user_con, username, table_name, condition, column_list):
        build_string = ""
        for x in range(len(column_list)):

            if x == len(column_list)-1:
                build_string = build_string + str(column_list[x] + " LIKE '%" + condition + "%'")
            else:
                build_string = build_string + str(column_list[x] + " LIKE '%" + condition + "%' OR ")

        single_row_string = "SELECT * FROM " + table_name + " WHERE " + build_string
        open_con.execute(single_row_string)

        # a = open_con.fetchall()
        rows = []
        for row in open_con.fetchall():
            rows.append(row)


        # Run ID check for the user log
        new_id_generated = SQLGenerateNewID(user_con, 'User_Logs')
        # Get date at time
        now = datetime.datetime.now()
        date_now = now.date()
        time_now = now.time()
        # Create list for user log insert
        user_list = (new_id_generated, username, 'Search all columns of the table for the condition', table_name, condition, str(date_now), str(time_now))
        # Execute insert string
        SQLInsertInto(user_con, "", "", 'User_Logs', user_list)
        return (rows)

class SQLSearchMultipleRow():
    def __new__(self, open_con, user_con, username, table_name, column_of_condition, condition):
        single_row_string = "SELECT * FROM " + table_name + " WHERE " + column_of_condition + " LIKE '%" + condition + "%'"
        open_con.execute(single_row_string)

        #a = open_con.fetchall()
        rows = []
        for row in open_con.fetchall():

            rows.append(row)

        #open_con.close()
        return (rows)

class SQLSearchRows():
    def __new__(self, open_con,  user_con, username, table_name, column_of_condition, condition):
        single_row_string = "SELECT * FROM %s WHERE %s LIKE '%s %%'" %(table_name, column_of_condition, condition)
        open_con.execute(single_row_string)
        row = open_con.fetchone()
        return(row)

class SQLInsertInto():
    def __new__(self, open_con, user_con, username, table_name, insert_list):

        insert_string = """INSERT INTO %s VALUES %s""" %(table_name, insert_list)
        open_con.execute(insert_string)
        open_con.commit()
        #open_con.close()

class SQLRemove():
    def __new__(self, open_con, table_name, column_of_condition, condition):
        if condition == 0:
            condition = -1
        delete_string = "DELETE FROM %s WHERE %s = %s" %(table_name, column_of_condition, condition)
        open_con.execute(delete_string)
        open_con.commit()
        #open_con.close()

class SQLUpdateRow():
    def __new__(self, open_con, table_name, remove_list):
        pass

class SQLUpdateEntry():
    def __new__(self, open_con, table, id_to_remove, column_list, entry_list):
        string_mid = ''
        string_start = 'UPDATE ' + table + ' SET '
        for x in range(len(column_list)):
            string_mid = string_mid + column_list[x] + ' = ' + entry_list[x]

        string_end = 'WHERE ID = ' + str(id_to_remove)

        update_sting  = str(string_start + string_mid + string_end)
        open_con.execute(update_sting)
        open_con.commit()

class SQLGetColumnNames():
    def __new__(self, open_con, table_name):
        open_con.execute('SELECT * FROM ' + table_name)
        columns = [column[0] for column in open_con.description]
        return(columns)

class SQLGenerateNewID():
    def __new__(self, open_con, table_name):
        single_row_string = "SELECT MAX(ID) FROM %s "%(table_name)

        open_con.execute(single_row_string)
        rows = open_con.fetchone()

        rows_as_list = [x for x in rows]
        if  rows_as_list[0] == None:
            new_id = 1
        else:
            new_id = rows_as_list[-1] + 1


        return(new_id)












