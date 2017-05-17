import pyodbc
import wx
import Read_And_Write_Files
import GUI
import time
import datetime

class SQLCon():
    def __new__(self, server_in, database_in, username_in, password_in, driver_in, port_in):

        server = server_in
        database = database_in
        username = username_in
        password = password_in
        driver = driver_in
        port = port_in

        cnxn = pyodbc.connect('DRIVER=' + driver + ' ; SERVER='+server+'; PORT=' + port + ';DATABASE='+database+' ;UID='+username+' ;PWD='+password)

        cursor = cnxn.cursor()
        return(cursor)

class SQLConAutoCommit():
    def __new__(self, server_in, database_in, username_in, password_in, driver_in, port_in):

        server = server_in
        database = database_in
        username = username_in
        password = password_in
        driver = driver_in
        port = port_in

        ConString = ('DRIVER={ODBC Driver 13 for SQL Server}; SERVER='+server+'; PORT=' + port + ';DATABASE='+database+'; Trusted_Connection=yes;')

        cnxn = pyodbc.connect(ConString, autocommit=True)

        cursor = cnxn.cursor()
        return(cursor)

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

class SQLGetColumnNames():
    def __new__(self, open_con, table_name):
        open_con.execute('SELECT * FROM ' + table_name)
        columns = [column[0] for column in open_con.description]
        return(columns)

class SQLCreateTable():
    def __new__(self, open_con, table_name, column_list):
        combine_string = ''
        for x in range(len(column_list)):
            if x == len(column_list)-1:
                combine_string = combine_string + '' + column_list[x]
            else:
                combine_string = combine_string + '' + column_list[x] + ','




        create_string = "CREATE TABLE " + table_name + "(" + combine_string + ")"
        open_con.execute(create_string)
        open_con.commit()

class SQLSearchColumnMutipleEntry():
    def __new__(self, open_con, username, table_name, condition, column_list):
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

            """ # Run ID check for the user log
                        new_id_generated = SQLGenerateNewID(user_con, 'User_Logs')
                        # Get date at time
                        now = datetime.datetime.now()
                        date_now = now.date()
                        time_now = now.time()
                        # Create list for user log insert
                        user_list = (new_id_generated, username, 'Search all columns of the table for the condition', table_name, condition, str(date_now), str(time_now))
                        # Execute insert string
                        SQLInsertInto(user_con, "", "", 'User_Logs', user_list)"""

        return (rows)

class SQLSearchColumnSingleEntry():
    def __new__(self, open_con, table_name, column_to_return, column_of_condition, condition):
        single_row_string = "SELECT " + column_to_return + " FROM " + table_name + " WHERE " + column_of_condition \
                            + " LIKE '" + condition + "'"
        open_con.execute(single_row_string)
        row = open_con.fetchone()
        #open_con.close()
        return (row)

class SQLSearchAll():
    def __new__(self, open_con, username, table_name, column_of_condition, condition):
        serch_all = "SELECT * FROM " + table_name
        open_con.execute(serch_all)
        row = open_con.fetchall()
        ''''#---------------------------------------------------------------------------------------------------------
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
        SQLInsertInto(user_con, "", "", 'User_Logs', user_list)'''
        return (row)

class SQLSearchAllSingleColumn():
    def __new__(self, open_con, username, table_name, column_of_condition):
        single_row_string = "SELECT " + column_of_condition + " FROM " + table_name
        open_con.execute(single_row_string)
        rows = open_con.fetchall()
        #open_con.close()
        return (rows)

class SQLInsertInto():
    def __new__(self, open_con, username, table_name, insert_list):

        insert_string = """INSERT INTO %s VALUES %s""" %( table_name, insert_list)
        open_con.execute(insert_string)
        open_con.commit()

class SQLRemove():
    def __new__(self, open_con, table_name, column_of_condition, condition):
        if condition == 0:
            condition = -1
        delete_string = "DELETE FROM %s WHERE %s = %s" %(table_name, column_of_condition, condition)
        open_con.execute(delete_string)
        open_con.commit()
        #open_con.close()

class SQLUpdateEntry():
    def __new__(self, open_con, table, id_to_edit, column_list, entry_list):
        string_mid = ''
        string_start = 'UPDATE ' + table + ' SET '

        for x in range(len(entry_list)):
            entry_list[x] = "'" + str(entry_list[x]) + "'"

        for x in range(len(column_list)):
            if x == max(range(len(column_list))):
                string_mid = string_mid + column_list[x] + ' = ' + entry_list[x]
            else:
                string_mid = string_mid + column_list[x] + ' = ' + entry_list[x] + ' , '

        string_end = 'WHERE ID = ' + str(id_to_edit)

        update_sting = str(string_start + string_mid + string_end)
        open_con.execute(update_sting)
        open_con.commit()

class SQLSearchMultipleRow():
    def __new__(self, open_con, table_name, column_of_condition, condition):
        single_row_string = "SELECT * FROM " + table_name + " WHERE " + column_of_condition + " = " + condition
        open_con.execute(single_row_string)

        #a = open_con.fetchall()
        rows = []
        for row in open_con.fetchall():

            rows.append(row)

        #open_con.close()
        return (rows)

class SQLCreateProjectDatabase():
    def __new__(self, open_con, project, username, password):

        # -------------------------------------------------------------------------
        # Create the sub data base for the project
        # -------------------------------------------------------------------------
        project = ('Sub_DB_' + project)
        sql_string = 'CREATE DATABASE [' + project + ']'
        open_con.execute(sql_string)
        open_con.commit()
        # -------------------------------------------------------------------------

        # -------------------------------------------------------------------------
        # Assign the reader role to the current user for this database
        # -------------------------------------------------------------------------
        sql_string = "USE " + project + " EXECUTE  sp_addrolemember db_datareader, [" + username + "];"
        open_con.execute(sql_string)
        open_con.commit()
        # -------------------------------------------------------------------------
        # Assign the writer role to the current user for this database
        # -------------------------------------------------------------------------
        sql_string = "USE " + project + " EXECUTE  sp_addrolemember db_datawriter, [" + username + "];"
        open_con.execute(sql_string)
        open_con.commit()
        # -------------------------------------------------------------------------
        # Assign the owner role to the current user for this database
        # -------------------------------------------------------------------------
        sql_string = "USE " + project + " EXECUTE  sp_addrolemember db_owner, [" + username + "];"
        open_con.execute(sql_string)
        open_con.commit()
        # -------------------------------------------------------------------------
        # Create the main table for the database
        # -------------------------------------------------------------------------
        # Generate the column list for the table
        column_list = ['ID INT', 'model varchar(MAX)', 'total_qty varchar(MAX)',
                       'internal_held_qty varchar(MAX)', 'site_held_qty varchar(MAX)',
                       'cost varchar(MAX)']

        # Refresh the connection to point at the new database
        conn_read = Read_And_Write_Files.Read_File('data_conn.tuk')
        server_in = conn_read[0]
        port_in = conn_read[2]
        driver_in = conn_read[3]

        # Read current user info
        user_read = Read_And_Write_Files.Read_File('user.tuk')
        username = user_read[0]
        password = user_read[1]

        open_con = SQLCon(server_in, project, username, password, driver_in, port_in)
        # Run table creation class
        SQLCreateTable(open_con, 'project_stock', column_list)
        open_con.close()
        # -------------------------------------------------------------------------

class SQLRemoveProjectDatabase():
    def __new__(self, open_con, project):
        project = ('Sub_DB_' + project)
        sql_string = 'USE master; ALTER DATABASE ' + project + ' SET SINGLE_USER WITH ROLLBACK IMMEDIATE; DROP DATABASE ' + project
        open_con.execute(sql_string)
        open_con.commit()