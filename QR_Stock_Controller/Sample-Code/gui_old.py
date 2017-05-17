########################################################################################################################
# Import library's bellow
# ---------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------
# Database connection class imports
from SQL import SQLSearchRows
from SQL import SQLSearchMultipleRow
from SQL import SQLSearchColumnMutipleEntry
from SQL import SQLGetColumnNames
from SQL import SQLCon
from SQL import SQLInsertInto
from SQL import SQLGenerateNewID
from SQL import SQLRemove
from SQL import SQLSearchAll
# ----------------------------------------------
# My file reader and writer import
import Read_And_Write_Files
# ----------------------------------------------
# My Modal file GUI's
from Modals import CheckDialog
from Modals import LoginDialog
import Modals
# ----------------------------------------------
# WXPython GUI library
import wx
# ----------------------------------------------
# Python Operating System library
import os
import os.path
import stat
import time
# ----------------------------------------------
# Object list view, the list's used for holding data
from ObjectListView import ObjectListView, ColumnDefn
# ----------------------------------------------
'''
server = 'MARK-PC\SQLEXPRESS'
#server = '192.168.2.114'
database = 'TUCKER31'
username = 'Jeff'
password = 'password1'
driver = '{ODBC Driver 13 for SQL Server}'
port = '49170'
'''
# ----------------------------------------------
# Global table names
# ----------------------------------------------
fitting_table = 'Fittings'
lamp_table = 'Lamps'
driver_table = 'Drivers'
accessories_table = 'Accessories'
log_table = 'User_Logs'



########################################################################################################################
# Main panel that holds all the widgets
# ---------------------------------------------------------------------------------------------------------------------
class MainPanel(wx.Panel):
    # ----------------------------------------------------------------------

    # ----------------------------------------------------------------------
    def __init__(self, parent, username, password):
        """Constructor"""
        working_table = 'ClientTable'
        wx.Panel.__init__(self, parent=parent)

        panel_main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        load_read = Read_And_Write_Files.Read_File('ini.tuk')
        open_con = SQLCon( load_read[0], load_read[1], username, password, load_read[2], load_read[3])

        tab_bar = MainTabBar(self, username, password)

        panel_main_sizer.Add(tab_bar, 1, wx.EXPAND)

        self.result = ''
        self.current_selection = 0

        # ----------------------------------------------
        # Old GUI code using for reference
        # ----------------------------------------------
        '''
        column_txt_static = wx.StaticText(self, label='Column to search')
        self.serach_column = wx.TextCtrl(self, -1, "ClientAge", size=(175, -1))
        condition_txt_static = wx.StaticText(self, label='Condition to search')
        self.serach_condition = wx.TextCtrl(self, -1, "24", size=(175, -1))

        self.insert_ID = wx.TextCtrl(self, -1, "6458", size=(175, -1))
        self.insert_ID.Bind(wx.EVT_CHAR_HOOK , lambda event: self.NextSelection(event, self.insert_client_name))

        self.insert_client_name = wx.TextCtrl(self, -1, "Paula", size=(175, -1))
        self.insert_client_name.Bind(wx.EVT_CHAR_HOOK, lambda event: self.NextSelection(event, self.insert_client_age))

        self.insert_client_age = wx.TextCtrl(self, -1, "24", size=(175, -1))
        self.insert_client_age.Bind(wx.EVT_CHAR_HOOK, lambda event: self.NextSelection(event, self.insert_client_user_name))

        self.insert_client_user_name = wx.TextCtrl(self, -1, "Paulateo", size=(175, -1))
        self.insert_client_user_name.Bind(wx.EVT_CHAR_HOOK, lambda event: self.NextSelection(event, self.insert_client_password))

        self.insert_client_password = wx.TextCtrl(self, -1, "191919", size=(175, -1))
        self.insert_client_password.Bind(wx.EVT_CHAR_HOOK, lambda event: self.NextSelection(event, self.btn_insert))

        self.btn_insert = wx.Button(self, -1, "Add to database")
        self.btn_insert.Bind(wx.EVT_CHAR_HOOK, lambda event: self.NextSelection(event, self.insert_ID))
        self.btn_insert.Bind(wx.EVT_BUTTON, lambda event: self.OnRunSearch(event, open, username, password,
                                                                           self.serach_column.GetValue(),
                                                                           self.serach_condition.GetValue()))


        self.btn_insert.Bind(wx.EVT_BUTTON, lambda event: self.OnInsert(event, open_con, username, password,
                                                                        self.insert_client_name.GetValue(),
                                                                        self.insert_client_age.GetValue(),
                                                                        self.insert_client_user_name.GetValue(),
                                                                        self.insert_client_password.GetValue()))

        self.btn_run = wx.Button(self, -1, "Run Search")
        self.btn_run.Bind(wx.EVT_BUTTON, lambda event: self.OnRunSearch(event, open, username, password,
                                                                        self.serach_column.GetValue(),
                                                                        self.serach_condition.GetValue()))

        self.btn_remove = wx.Button(self, -1, "Remove")
        self.btn_remove.Bind(wx.EVT_BUTTON, lambda event: self.OnRunSearch(event, open, username, password,
                                                                           self.serach_column.GetValue(),
                                                                           self.serach_condition.GetValue()))

        self.btn_remove.Bind(wx.EVT_BUTTON, lambda event: self.OnRemoveFromDataBase(event, open, username, password,
                                                                                    working_table,'ID',
                                                                                    self.current_selection))

        self.olv = ObjectListView(self, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.olv.Bind(wx.EVT_LIST_ITEM_SELECTED, lambda event: self.OnClick( event, self.olv))

        panel_wrapper_sizer = wx.BoxSizer(wx.VERTICAL)
        panel_wrapper_two_sizer = wx.BoxSizer(wx.VERTICAL)
        '''

        '''
        panel_wrapper_sizer.Add(column_txt_static, 0, wx.ALL, 2)
        panel_wrapper_sizer.Add(self.serach_column, 0, wx.ALL, 2)
        panel_wrapper_sizer.Add(condition_txt_static, 0, wx.ALL, 2)
        panel_wrapper_sizer.Add(self.serach_condition, 0, wx.ALL, 2)
        panel_wrapper_sizer.Add(self.btn_run, 0, wx.ALL, 2)
        panel_wrapper_sizer.Add(self.btn_remove, 0, wx.ALL, 2)

        panel_wrapper_sizer.Add(self.olv, 1, wx.EXPAND)

        panel_wrapper_two_sizer.Add(self.insert_ID, 0, wx.ALL, 2)
        panel_wrapper_two_sizer.Add(self.insert_client_name, 0, wx.ALL, 2)
        panel_wrapper_two_sizer.Add(self.insert_client_age, 0, wx.ALL, 2)
        panel_wrapper_two_sizer.Add(self.insert_client_user_name, 0, wx.ALL, 2)
        panel_wrapper_two_sizer.Add(self.insert_client_password, 0, wx.ALL, 2)
        panel_wrapper_two_sizer.Add(self.btn_insert, 0, wx.ALL, 2)


        panel_main_sizer.Add(panel_wrapper_sizer, 1, wx.EXPAND)
        panel_main_sizer.Add(panel_wrapper_two_sizer, 1, wx.EXPAND)
        '''
        # ----------------------------------------------
        self.SetSizer(panel_main_sizer)
        # ----------------------------------------------
        #column_list = SQLGetColumnNames(open, 'ClientTable')
        #self.setEntries(column_list)
    def OnInsert(self, event, open_con ,username, password, table, insert_list):

        load_read = Read_And_Write_Files.Read_File('ini.tuk')
        open_con = SQLCon(load_read[0], load_read[1], username, password, load_read[2], load_read[3])

        new_id_generated = SQLGenerateNewID(open_con, table)
        run_insert = SQLInsertInto(open_con, 'ClientTable', insert_list)
        open_con.close()
        event.Skip()

    def OnInsertOld(self, event, open_con ,username, password, insert_client_name, insert_client_age, insert_client_user_name, insert_client_password):

        load_read = Read_And_Write_Files.Read_File('ini.tuk')
        open_con = SQLCon(load_read[0], load_read[1], username, password, load_read[2], load_read[3])
        new_id_generated = SQLGenerateNewID(open_con, 'ClientTable')
        insert_list = (new_id_generated, insert_client_name,insert_client_age,insert_client_user_name,insert_client_password)
        run_insert = SQLInsertInto(open_con, 'ClientTable', insert_list)
        open_con.close()
        event.Skip()

    def OnRemoveFromDataBase(self, event, open_con, username, password, table_name, column_of_condition, condition):

        load_read = Read_And_Write_Files.Read_File('ini.tuk')
        open_con = SQLCon(load_read[0], load_read[1], username, password, load_read[2], load_read[3])
        condition_hold = condition
        check_user = CheckDialog(self,"Remove entry from database! ", "Do you wish to remove " + condition +
                                 " from the database? This will not be reversible!", condition_hold).ShowModal()
        if check_user == 1:
            removed_entry = SQLRemove(open_con, table_name, column_of_condition, condition_hold)
            #inform_user = MessageDialogBox('This is not a PDF file', 'Unknown File Type')

        open_con.close()
        event.Skip()

    def NextSelection(self, event, next_selected):
        a = event.GetKeyCode()
        if a == 370:
            next_selected.SetFocus()

    def OnClick(self, event, slected_list):
        get_id = slected_list.GetSelectedObject()
        current_selection = get_id.ID
        self.current_selection = str(current_selection)

    def setEntries(self, column_list):
        """"""
        column_build_list = []
        for x in range(len(column_list)):
            column_build_list.append(ColumnDefn(column_list[x], "right", 100, column_list[x]))

        self.olv.SetColumns(column_build_list)
        self.olv.SetObjects(self.entry_list)

    def updateDisplay(self,  entry_list):
        """
        #entry_list = str(entry_list).split(',')
        self.construction_list = []
        for row in entry_list:

            build_list = str(row).split(',')
            ID = build_list[0].replace('(',"").replace("[","").replace("'","").replace(" ","")

            ClientName = build_list[1].replace("(","").replace("[","").replace("'","").replace(" ","")
            ClientAge = build_list[2].replace("(","").replace("[","").replace("'","").replace(" ","")
            ClientUserName = build_list[3].replace("(","").replace("[","").replace("'","").replace(" ","")
            ClientPassWord = build_list[4].replace(')',"").replace("[","").replace("'","").replace(" ","")



            self.construction_list.append(DBItem(ID,
                                            ClientName,
                                            ClientAge,
                                            ClientUserName,
                                            ClientPassWord))


        self.olv.SetObjects(self.construction_list)
        """

    def OnRunSearch(self, event, open_con, username, password, table, column, condition):
        load_read = Read_And_Write_Files.Read_File('ini.tuk')
        open_con = SQLCon(load_read[0], load_read[1], username, password, load_read[2], load_read[3])
        column_list = SQLGetColumnNames(open_con, table)
        display_result = []
        if condition == "":
            run_result = SQLSearchAll(open_con, 'ClientTable', column, condition)
        else:
            '''for x in range(len(column_list)):
                run_result = SQLSearchMultipleRow(open_con, 'ClientTable', column_list[x], condition)
                '''
            run_result = SQLSearchColumnMutipleEntry(open_con, 'ClientTable', column, condition, column_list)
            display_result.append(run_result)
        self.updateDisplay(run_result)
        open_con.close()
        event.Skip()
#######################################################################################################################

# ---------------------------------------------------------------------------------------------------------------------
# Class for the menu bar
# ---------------------------------------------------------------------------------------------------------------------

#######################################################################################################################
# Class that create the tab bar
# ---------------------------------------------------------------------------------------------------------------------
class MainTabBar(wx.Notebook):

    # ----------------------------------------------------------------------
    def __init__(self, parent, username, password):
        wx.Notebook.__init__(self, parent, id=wx.ID_ANY, style=
        wx.BK_DEFAULT
                             # wx.BK_TOP
                             # wx.BK_BOTTOM
                             # wx.BK_LEFT
                             # wx.BK_RIGHT
                             )

        tab_one = FittingPanel(self, parent, username, password)
        tab_two = LampPanel(self, parent, username, password)
        tab_three = DriverPanel(self, parent,  username, password)
        tab_four = AccessoriesPanel(self, parent, username, password)

        self.AddPage(tab_one, "Fittings")
        self.AddPage(tab_two, "Lamps")
        self.AddPage(tab_three, "Drivers")
        self.AddPage(tab_four, "Accessories")
# ---------------------------------------------------------------------------------------------------------------------
# Separate classes for the GUI of the different pages of the tab bar
# ---------------------------------------------------------------------------------------------------------------------
class FittingPanel(wx.Panel):
    def __init__(self, parent, panel, username, password):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        # -------------------------------------------------------------------------------------------------------------
        # Create variable for the panel
        # -------------------------------------------------------------------------------------------------------------
        self.list = []
        # -------------------------------------------------------------------------------------------------------------


        # -------------------------------------------------------------------------------------------------------------
        # Create all the size's
        # -------------------------------------------------------------------------------------------------------------
        control_sizer = wx.BoxSizer(wx.HORIZONTAL)
        list_view_sizer = wx.BoxSizer(wx.HORIZONTAL)
        info_bar_sizer = wx.BoxSizer(wx.HORIZONTAL)
        wrapper_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # -------------------------------------------------------------------------------------------------------------
        # Create widgets
        # -------------------------------------------------------------------------------------------------------------
        self.search_text_ctr = wx.TextCtrl(self, -1, "", size=(175, -1))
        #self.search_text_ctr.Bind(wx.EVT_CHAR_HOOK, lambda event: self.OnSearch(event, self.insert_client_name))

        self.btn_run_search = wx.Button(self, -1, "Run Search")
        self.btn_run_search.Bind(wx.EVT_BUTTON, lambda event: self.OnRunSearch(event, username, password, fitting_table, '', self.search_text_ctr.GetValue(), 1))

        self.btn_add_entry = wx.Button(self, -1, "Create new fitting")
        self.btn_add_entry.Bind(wx.EVT_BUTTON,
                                 lambda event: self.OnAddEntry(event, username, password, fitting_table, 1))
        self.btn_remove_entry = wx.Button(self, -1, "Remove Fitting")

        self.fitting_list = ObjectListView(self, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.fitting_list.AutoSizeColumns()

        self.info_bar_static_text_user = wx.StaticText(self, label='You are logged in as : %s' % username)

        # -------------------------------------------------------------------------------------------------------------
        # Add widgets to sizer's
        # -------------------------------------------------------------------------------------------------------------
        control_sizer.Add(self.btn_run_search, 0, wx.ALIGN_CENTER)
        control_sizer.Add(self.search_text_ctr, 0, wx.ALIGN_CENTER)
        control_sizer.Add(self.btn_add_entry, 0, wx.ALIGN_CENTER)
        control_sizer.Add(self.btn_remove_entry, 0, wx.ALIGN_CENTER)

        list_view_sizer.Add(self.fitting_list, 1, wx.EXPAND | wx.ALL)

        info_bar_sizer.Add(self.info_bar_static_text_user, 0, wx.ALIGN_CENTER)

        # -------------------------------------------------------------------------------------------------------------
        # Wrap sizer that contain widgets vertically with spacers
        # -------------------------------------------------------------------------------------------------------------
        wrapper_sizer.AddSpacer(5)
        wrapper_sizer.Add(control_sizer, 0, wx.ALL)
        wrapper_sizer.AddSpacer(5)
        wrapper_sizer.Add(list_view_sizer, 1, wx.EXPAND)
        wrapper_sizer.AddSpacer(5)
        wrapper_sizer.Add(info_bar_sizer, 0, wx.ALL)
        wrapper_sizer.AddSpacer(5)
        # -------------------------------------------------------------------------------------------------------------
        # Wrap sizer that contain sizer's with widgets horizontally with spacers
        # -------------------------------------------------------------------------------------------------------------
        main_sizer.AddSpacer(10)
        main_sizer.Add(wrapper_sizer, 1, wx.EXPAND | wx.ALL)
        main_sizer.AddSpacer(10)

        self.SetSizer(main_sizer)

        load_read = Read_And_Write_Files.Read_File('ini.tuk')
        open_con = SQLCon(load_read[0], load_read[1], username, password, load_read[2], load_read[3])
        column_list = SQLGetColumnNames(open_con, fitting_table)

        self.setEntries(column_list)

    def updateDisplay(self, entry_list):
        self.construction_list = []
        for row in entry_list:
            build_list = str(row).split(',')
            ID = build_list[0].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Product_Code = build_list[1].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Manufacturer = build_list[2].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Fitting_Type = build_list[3].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Fitting_Description = build_list[4].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            IP_Rating = build_list[5].replace('(', "").replace("[", "").replace("'", "").replace(" ", "")
            Dimmable = build_list[6].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Voltage_Min = build_list[7].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Voltage_Max = build_list[8].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Voltage_Type = build_list[9].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Wattage = build_list[10].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Colour = build_list[11].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Beam_Angle = build_list[12].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Colour_Temperature = build_list[13].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            CRI = build_list[14].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Lumens = build_list[15].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Image_Name = build_list[16].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Sage_Category = build_list[17].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Finite_Code = build_list[18].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Unit_of_measure = build_list[19].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Warrenty = build_list[20].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Notes = build_list[21].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Finite_Solutions_Buy_Price = build_list[22].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Discount_off_published_Trade_Price = build_list[23].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Published_manufacturer_Trade_Price_ex_VAT = build_list[24].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Published_manufacturer_Retail_ex_VAT = build_list[25].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Finite_Solutions_Sell_price = build_list[26].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Finite_Solutions_Margin_Price = build_list[27].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Finite_Solutions_Margin_Percentage = build_list[28].replace('(', "").replace("[", "").replace("'", "").replace(")", "")


            self.construction_list.append(FittingListRowBuilder(ID,
                                                                Product_Code,
                                                                Manufacturer,
                                                                Fitting_Type,
                                                                Fitting_Description,
                                                                IP_Rating,
                                                                Dimmable,
                                                                Voltage_Min,
                                                                Voltage_Max,
                                                                Voltage_Type,
                                                                Wattage,
                                                                Colour,
                                                                Beam_Angle,
                                                                Colour_Temperature,
                                                                CRI,
                                                                Lumens,
                                                                Image_Name,
                                                                Sage_Category,
                                                                Finite_Code,
                                                                Unit_of_measure,
                                                                Warrenty,
                                                                Notes,
                                                                Finite_Solutions_Buy_Price,
                                                                Discount_off_published_Trade_Price,
                                                                Published_manufacturer_Trade_Price_ex_VAT,
                                                                Published_manufacturer_Retail_ex_VAT,
                                                                Finite_Solutions_Sell_price,
                                                                Finite_Solutions_Margin_Price,
                                                                Finite_Solutions_Margin_Percentage))

        self.fitting_list.SetObjects(self.construction_list)

    def setEntries(self, column_list):
        """"""
        column_build_list = []
        for x in range(len(column_list)):
            width = len(column_list[x])
            width = width * 10
            if width <= 80:
                width = 90
            column_build_list.append(ColumnDefn(column_list[x], "center", width, column_list[x]))

        self.fitting_list.SetColumns(column_build_list)
        self.fitting_list.SetObjects(self.list)

    def OnRunSearch(self, event, username, password, table, column, condition, login_state):
        if login_state == 0:
            # message that you need to be loged in!
            event.Skip()
        load_read = Read_And_Write_Files.Read_File('ini.tuk')
        open_con = SQLCon(load_read[0], load_read[1], username, password, load_read[2], load_read[3])
        user_con = SQLCon(load_read[0], load_read[1], username, password, load_read[2], load_read[3])
        column_list = SQLGetColumnNames(open_con, table)
        display_result = []
        if condition == "":
            run_result = SQLSearchAll(open_con, user_con, username, table, column, condition)
        else:
            run_result = SQLSearchColumnMutipleEntry(open_con, user_con, username, table, condition, column_list)
            display_result.append(run_result)
        self.updateDisplay(run_result)
        open_con.close()
        user_con.close()
        event.Skip()

    def OnAddEntry(self, event, username, password, table , login_state):



        add_fitting_modal = Modals.AddFittingModal(self, "Add new fitting to the database", username, password, table, login_state).ShowModal()

        event.Skip()

class LampPanel(wx.Panel):
    def __init__(self, parent, panel, username, password):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        # -------------------------------------------------------------------------------------------------------------
        # Create variable for the panel
        # -------------------------------------------------------------------------------------------------------------
        self.list = []
        # -------------------------------------------------------------------------------------------------------------
        # -------------------------------------------------------------------------------------------------------------
        # Create all the size's
        # -------------------------------------------------------------------------------------------------------------
        control_sizer = wx.BoxSizer(wx.HORIZONTAL)
        list_view_sizer = wx.BoxSizer(wx.HORIZONTAL)
        info_bar_sizer = wx.BoxSizer(wx.HORIZONTAL)
        wrapper_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # -------------------------------------------------------------------------------------------------------------
        # Create widgets
        # -------------------------------------------------------------------------------------------------------------
        self.search_text_ctr = wx.TextCtrl(self, -1, "", size=(175, -1))
        #self.search_text_ctr.Bind(wx.EVT_CHAR_HOOK, lambda event: self.OnSearch(event, self.insert_client_name))

        self.btn_run_search = wx.Button(self, -1, "Run Search")
        self.btn_run_search.Bind(wx.EVT_BUTTON,
                                 lambda event: self.OnRunSearch(event, username, password, lamp_table, '',
                                                                self.search_text_ctr.GetValue(), 1))
        #self.btn_run.Bind(wx.EVT_BUTTON, lambda event: self.OnRunSearch(event, open, username, password, self.search_text_ctr.GetValue()))

        self.btn_add_entry = wx.Button(self, -1, "Create new Lamp")

        self.btn_remove_entry = wx.Button(self, -1, "Remove Lamp")

        self.lamp_list = ObjectListView(self, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.lamp_list.AutoSizeColumns()

        self.info_bar_static_text_user = wx.StaticText(self, label='You are logged in as : %s' % username)

        # -------------------------------------------------------------------------------------------------------------
        # Add widgets to sizer's
        # -------------------------------------------------------------------------------------------------------------
        control_sizer.Add(self.btn_run_search, 0, wx.ALIGN_CENTER)
        control_sizer.Add(self.search_text_ctr, 0, wx.ALIGN_CENTER)
        control_sizer.Add(self.btn_add_entry, 0, wx.ALIGN_CENTER)
        control_sizer.Add(self.btn_remove_entry, 0, wx.ALIGN_CENTER)

        list_view_sizer.Add(self.lamp_list, 1, wx.EXPAND | wx.ALL)

        info_bar_sizer.Add(self.info_bar_static_text_user, 0, wx.ALIGN_CENTER)


        # -------------------------------------------------------------------------------------------------------------
        # Wrap sizer that contain widgets vertically with spacers
        # -------------------------------------------------------------------------------------------------------------
        wrapper_sizer.AddSpacer(5)
        wrapper_sizer.Add(control_sizer, 0, wx.ALL)
        wrapper_sizer.AddSpacer(5)
        wrapper_sizer.Add(list_view_sizer, 1, wx.EXPAND)
        wrapper_sizer.AddSpacer(5)
        wrapper_sizer.Add(info_bar_sizer, 0, wx.ALL)
        wrapper_sizer.AddSpacer(5)
        # -------------------------------------------------------------------------------------------------------------
        # Wrap sizer that contain sizer's with widgets horizontally with spacers
        # -------------------------------------------------------------------------------------------------------------
        main_sizer.AddSpacer(10)
        main_sizer.Add(wrapper_sizer, 1, wx.EXPAND | wx.ALL)
        main_sizer.AddSpacer(10)

        self.SetSizer(main_sizer)

        load_read = Read_And_Write_Files.Read_File('ini.tuk')
        open_con = SQLCon(load_read[0], load_read[1], username, password, load_read[2], load_read[3])
        column_list = SQLGetColumnNames(open_con, lamp_table)

        self.setEntries(column_list)

    def updateDisplay(self,  entry_list):

        self.construction_list = []
        for row in entry_list:

            build_list = str(row).split(',')
            ID = build_list[0].replace('(',"").replace("[","").replace("'","").replace(" ","")
            Product_Code = build_list[1].replace('(',"").replace("[","").replace("'","").replace(" ","")
            Manufacturer = build_list[2].replace('(',"").replace("[","").replace("'","").replace(" ","")
            Fitting_Type = build_list[3].replace('(',"").replace("[","").replace("'","").replace(" ","")
            Fixing_Type = build_list[4].replace('(',"").replace("[","").replace("'","").replace(" ","")
            Dimming_Type = build_list[5].replace('(',"").replace("[","").replace("'","").replace(" ","")
            Wattage = build_list[6].replace('(',"").replace("[","").replace("'","").replace(" ","")
            Halogen_Equivalent_Wattage = build_list[7].replace('(',"").replace("[","").replace("'","").replace(" ","")
            Beam_Angle = build_list[8].replace('(',"").replace("[","").replace("'","").replace(" ","")
            Colour_Temperature = build_list[9].replace('(',"").replace("[","").replace("'","").replace(" ","")
            CRI = build_list[10].replace('(',"").replace("[","").replace("'","").replace(" ","")
            Lumens = build_list[11].replace('(',"").replace("[","").replace("'","").replace(" ","")
            Voltage_Type = build_list[12].replace('(',"").replace("[","").replace("'","").replace(" ","")
            Finite_Code = build_list[13].replace('(',"").replace("[","").replace("'","").replace(" ","")
            Finite_Solutions_Buy_Price = build_list[14].replace('(',"").replace("[","").replace("'","").replace(" ","")
            Discount_off_published_Trade_Price = build_list[15].replace('(',"").replace("[","").replace("'","").replace(" ","")
            Published_Manufacturer_Trade_Price_ex_VAT = build_list[16].replace('(',"").replace("[","").replace("'","").replace(" ","")
            Published_Manufacturer_Retail_ex_VAT = build_list[17].replace('(',"").replace("[","").replace("'","").replace(" ","")
            Finite_Solutions_Sell_price = build_list[18].replace('(',"").replace("[","").replace("'","").replace(" ","")
            Finite_Solutions_Margin_Price = build_list[19].replace('(',"").replace("[","").replace("'","").replace(" ","")
            Finite_Solutions_Margin_Percentage = build_list[20].replace('(', "").replace("[", "").replace("'", "").replace(
                " ", "")

            self.construction_list.append(LampListRowBuilder(ID, Product_Code, Manufacturer, Fitting_Type, Fixing_Type,
                                                             Dimming_Type, Wattage, Halogen_Equivalent_Wattage, Beam_Angle, Colour_Temperature, CRI, Lumens, Voltage_Type,
                                                             Finite_Code, Finite_Solutions_Buy_Price, Discount_off_published_Trade_Price, Published_Manufacturer_Trade_Price_ex_VAT, Published_Manufacturer_Retail_ex_VAT,
                                                             Finite_Solutions_Sell_price, Finite_Solutions_Margin_Price, Finite_Solutions_Margin_Percentage))

        self.lamp_list.SetObjects(self.construction_list)

    def setEntries(self, column_list):
        """"""
        column_build_list = []
        for x in range(len(column_list)):
            width = len(column_list[x])
            width = width * 10
            if width <= 80:
                width = 90
            column_build_list.append(ColumnDefn(column_list[x], "left", width, column_list[x]))

        self.lamp_list.SetColumns(column_build_list)
        self.lamp_list.SetObjects(self.list)

    def OnRunSearch(self, event, username, password, table, column, condition, login_state):
        if login_state == 0:
            # message that you need to be loged in!
            event.Skip()
        load_read = Read_And_Write_Files.Read_File('ini.tuk')
        open_con = SQLCon(load_read[0], load_read[1], username, password, load_read[2], load_read[3])
        user_con = SQLCon(load_read[0], load_read[1], username, password, load_read[2], load_read[3])
        column_list = SQLGetColumnNames(open_con, table)
        display_result = []
        if condition == "":
            run_result = SQLSearchAll(open_con, user_con, username, table, column, condition)
        else:
            run_result = SQLSearchColumnMutipleEntry(open_con, user_con, username, table, condition, column_list)
            display_result.append(run_result)
        self.updateDisplay(run_result)
        open_con.close()
        user_con.close()
        event.Skip()

class DriverPanel(wx.Panel):
    def __init__(self, parent, panel, username, password):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        # -------------------------------------------------------------------------------------------------------------
        # Create variable for the panel
        # -------------------------------------------------------------------------------------------------------------
        self.list = []
        # -------------------------------------------------------------------------------------------------------------
        # Create all the size's
        # -------------------------------------------------------------------------------------------------------------
        control_sizer = wx.BoxSizer(wx.HORIZONTAL)
        list_view_sizer = wx.BoxSizer(wx.HORIZONTAL)
        info_bar_sizer = wx.BoxSizer(wx.HORIZONTAL)
        wrapper_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # -------------------------------------------------------------------------------------------------------------
        # Create widgets
        # -------------------------------------------------------------------------------------------------------------
        self.search_text_ctr = wx.TextCtrl(self, -1, "", size=(175, -1))
        #self.search_text_ctr.Bind(wx.EVT_CHAR_HOOK, lambda event: self.OnSearch(event, self.insert_client_name))

        self.btn_run_search = wx.Button(self, -1, "Run Search")
        self.btn_run_search.Bind(wx.EVT_BUTTON,
                                 lambda event: self.OnRunSearch(event, username, password, driver_table, '',
                                                                self.search_text_ctr.GetValue(), 1))

        self.btn_add_entry = wx.Button(self, -1, "Create new Driver")

        self.btn_remove_entry = wx.Button(self, -1, "Remove Driver")

        self.driver_list = ObjectListView(self, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.driver_list.AutoSizeColumns()

        self.info_bar_static_text_user = wx.StaticText(self, label='You are logged in as : %s' % username)

        # -------------------------------------------------------------------------------------------------------------
        # Add widgets to sizer's
        # -------------------------------------------------------------------------------------------------------------
        control_sizer.Add(self.btn_run_search, 0, wx.ALIGN_CENTER)
        control_sizer.Add(self.search_text_ctr, 0, wx.ALIGN_CENTER)
        control_sizer.Add(self.btn_add_entry, 0, wx.ALIGN_CENTER)
        control_sizer.Add(self.btn_remove_entry, 0, wx.ALIGN_CENTER)

        list_view_sizer.Add(self.driver_list, 1, wx.EXPAND | wx.ALL)

        info_bar_sizer.Add(self.info_bar_static_text_user, 0, wx.ALIGN_CENTER)


        # -------------------------------------------------------------------------------------------------------------
        # Wrap sizer that contain widgets vertically with spacers
        # -------------------------------------------------------------------------------------------------------------
        wrapper_sizer.AddSpacer(5)
        wrapper_sizer.Add(control_sizer, 0, wx.ALL)
        wrapper_sizer.AddSpacer(5)
        wrapper_sizer.Add(list_view_sizer, 1, wx.EXPAND)
        wrapper_sizer.AddSpacer(5)
        wrapper_sizer.Add(info_bar_sizer, 0, wx.ALL)
        wrapper_sizer.AddSpacer(5)
        # -------------------------------------------------------------------------------------------------------------
        # Wrap sizer that contain sizer's with widgets horizontally with spacers
        # -------------------------------------------------------------------------------------------------------------
        main_sizer.AddSpacer(10)
        main_sizer.Add(wrapper_sizer, 1, wx.EXPAND | wx.ALL)
        main_sizer.AddSpacer(10)

        self.SetSizer(main_sizer)

        load_read = Read_And_Write_Files.Read_File('ini.tuk')
        open_con = SQLCon(load_read[0], load_read[1], username, password, load_read[2], load_read[3])
        column_list = SQLGetColumnNames(open_con, driver_table)

        self.setEntries(column_list)

    def updateDisplay(self, entry_list):
        self.construction_list = []
        for row in entry_list:
            build_list = str(row).split(',')
            ID = build_list[0].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Product_Code = build_list[1].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Manufacturer = build_list[2].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Description = build_list[3].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Voltage = build_list[4].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Dimming_Type = build_list[5].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Notes = build_list[6].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Max_Wattage = build_list[7].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Finite_Code = build_list[8].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Finite_Solutions_Buy_Price = build_list[9].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Discount_off_published_Trade_Price = build_list[10].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Published_manufacturer_Trade_Price_ex_VAT = build_list[11].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Published_manufacturer_Retail_ex_VAT = build_list[12].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Finite_Solutions_Sell_price = build_list[13].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Finite_Solutions_Margin_Price = build_list[14].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Finite_Solutions_Margin_Percentage = build_list[15].replace('(', "").replace("[", "").replace("'", "").replace(")", "")

            self.construction_list.append(DriversListRowBuilder(ID, Product_Code, Manufacturer, Description, Voltage,
                                                             Dimming_Type, Notes, Max_Wattage, Finite_Code, Finite_Solutions_Buy_Price,
                                                             Discount_off_published_Trade_Price, Published_manufacturer_Trade_Price_ex_VAT, Published_manufacturer_Retail_ex_VAT,
                                                             Finite_Solutions_Sell_price, Finite_Solutions_Margin_Price, Finite_Solutions_Margin_Percentage))

        self.driver_list.SetObjects(self.construction_list)

    def setEntries(self, column_list):
        """"""
        column_build_list = []
        for x in range(len(column_list)):
            width = len(column_list[x])
            width = width * 10
            if width <= 80:
                width = 90
            column_build_list.append(ColumnDefn(column_list[x], "left", width, column_list[x]))

        self.driver_list.SetColumns(column_build_list)
        self.driver_list.SetObjects(self.list)

    def OnRunSearch(self, event, username, password, table, column, condition, login_state):
        if login_state == 0:
            # message that you need to be loged in!
            event.Skip()
        load_read = Read_And_Write_Files.Read_File('ini.tuk')
        open_con = SQLCon(load_read[0], load_read[1], username, password, load_read[2], load_read[3])
        user_con = SQLCon(load_read[0], load_read[1], username, password, load_read[2], load_read[3])
        column_list = SQLGetColumnNames(open_con, table)
        display_result = []
        if condition == "":
            run_result = SQLSearchAll(open_con, user_con, username, table, column, condition)
        else:
            run_result = SQLSearchColumnMutipleEntry(open_con, user_con, username, table, condition, column_list)
            display_result.append(run_result)
        self.updateDisplay(run_result)
        open_con.close()
        user_con.close()
        event.Skip()

class AccessoriesPanel(wx.Panel):
    def __init__(self, parent, panel, username, password):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        # -------------------------------------------------------------------------------------------------------------
        # Create variable for the panel
        # -------------------------------------------------------------------------------------------------------------
        self.list = []
        # -------------------------------------------------------------------------------------------------------------
        # Create all the size's
        # -------------------------------------------------------------------------------------------------------------
        control_sizer = wx.BoxSizer(wx.HORIZONTAL)
        list_view_sizer = wx.BoxSizer(wx.HORIZONTAL)
        info_bar_sizer = wx.BoxSizer(wx.HORIZONTAL)
        wrapper_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # -------------------------------------------------------------------------------------------------------------
        # Create widgets
        # -------------------------------------------------------------------------------------------------------------
        self.search_text_ctr = wx.TextCtrl(self, -1, "", size=(175, -1))
        #self.search_text_ctr.Bind(wx.EVT_CHAR_HOOK, lambda event: self.OnSearch(event, self.insert_client_name))

        self.btn_run_search = wx.Button(self, -1, "Run Search")
        self.btn_run_search.Bind(wx.EVT_BUTTON,
                                 lambda event: self.OnRunSearch(event, username, password, accessories_table, '',
                                                                self.search_text_ctr.GetValue(), 1))

        self.btn_add_entry = wx.Button(self, -1, "Create new Accessorie")

        self.btn_remove_entry = wx.Button(self, -1, "Remove Accessorie")

        self.accessorie_list = ObjectListView(self, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.accessorie_list.AutoSizeColumns()
        self.info_bar_static_text_user = wx.StaticText(self, label='You are logged in as : %s' % username)

        # -------------------------------------------------------------------------------------------------------------
        # Add widgets to sizer's
        # -------------------------------------------------------------------------------------------------------------
        control_sizer.Add(self.btn_run_search, 0, wx.ALIGN_CENTER)
        control_sizer.Add(self.search_text_ctr, 0, wx.ALIGN_CENTER)
        control_sizer.Add(self.btn_add_entry, 0, wx.ALIGN_CENTER)
        control_sizer.Add(self.btn_remove_entry, 0, wx.ALIGN_CENTER)

        list_view_sizer.Add(self.accessorie_list, 1, wx.EXPAND | wx.ALL)

        info_bar_sizer.Add(self.info_bar_static_text_user, 0, wx.ALIGN_CENTER)


        # -------------------------------------------------------------------------------------------------------------
        # Wrap sizer that contain widgets vertically with spacers
        # -------------------------------------------------------------------------------------------------------------
        wrapper_sizer.AddSpacer(5)
        wrapper_sizer.Add(control_sizer, 0, wx.ALL)
        wrapper_sizer.AddSpacer(5)
        wrapper_sizer.Add(list_view_sizer, 1, wx.EXPAND)
        wrapper_sizer.AddSpacer(5)
        wrapper_sizer.Add(info_bar_sizer, 0, wx.ALL)
        wrapper_sizer.AddSpacer(5)
        # -------------------------------------------------------------------------------------------------------------
        # Wrap sizer that contain sizer's with widgets horizontally with spacers
        # -------------------------------------------------------------------------------------------------------------
        main_sizer.AddSpacer(10)
        main_sizer.Add(wrapper_sizer, 1, wx.EXPAND | wx.ALL)
        main_sizer.AddSpacer(10)

        self.SetSizer(main_sizer)

        load_read = Read_And_Write_Files.Read_File('ini.tuk')
        open_con = SQLCon(load_read[0], load_read[1], username, password, load_read[2], load_read[3])
        column_list = SQLGetColumnNames(open_con, accessories_table)

        self.setEntries(column_list)

    def updateDisplay(self, entry_list):
        self.construction_list = []
        for row in entry_list:
            build_list = str(row).split(',')
            ID = build_list[0].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Product_Code = build_list[1].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Manufacturer = build_list[2].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Description = build_list[3].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Voltage = build_list[4].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Dimming_Type = build_list[5].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Notes = build_list[6].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Max_Wattage = build_list[7].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Finite_Code = build_list[8].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Finite_Solutions_Buy_Price = build_list[9].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Discount_off_published_Trade_Price = build_list[10].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Published_manufacturers_Trade_Price_Ex_VAT = build_list[11].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Published_manufacturer_Retail_Ex_VAT = build_list[12].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Finite_Solutions_Sell_price = build_list[13].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Finite_Solutions_Margin_Price = build_list[14].replace('(', "").replace("[", "").replace("'", "").replace("", "")
            Finite_Solutions_Margin_Percentage = build_list[15].replace('(', "").replace("[", "").replace("'", "").replace(")", "")


            self.construction_list.append(AccessoriesListRowBuilder(ID, Product_Code, Manufacturer, Description, Voltage,
                                                                    Dimming_Type, Notes, Max_Wattage, Finite_Code, Finite_Solutions_Buy_Price,
                                                                    Discount_off_published_Trade_Price, Published_manufacturers_Trade_Price_Ex_VAT, Published_manufacturer_Retail_Ex_VAT,
                                                                    Finite_Solutions_Sell_price, Finite_Solutions_Margin_Price, Finite_Solutions_Margin_Percentage))

        self.accessorie_list.SetObjects(self.construction_list)

    def setEntries(self, column_list):
        """"""
        column_build_list = []
        for x in range(len(column_list)):
            width = len(column_list[x])
            width = width * 10
            if width <= 80:
                width = 90
            column_build_list.append(ColumnDefn(column_list[x], "left", width, column_list[x]))

        self.accessorie_list.SetColumns(column_build_list)
        self.accessorie_list.SetObjects(self.list)

    def OnRunSearch(self, event, username, password, table, column, condition, login_state):
        if login_state == 0:
            # message that you need to be loged in!
            event.Skip()
        load_read = Read_And_Write_Files.Read_File('ini.tuk')
        open_con = SQLCon(load_read[0], load_read[1], username, password, load_read[2], load_read[3])
        user_con = SQLCon(load_read[0], load_read[1], username, password, load_read[2], load_read[3])
        column_list = SQLGetColumnNames(open_con, table)
        display_result = []
        if condition == "":
            run_result = SQLSearchAll(open_con, user_con, username, table, column, condition)
        else:
            run_result = SQLSearchColumnMutipleEntry(open_con, user_con, username, table, condition, column_list)
            display_result.append(run_result)
        self.updateDisplay(run_result)
        open_con.close()
        user_con.close()
        event.Skip()

#######################################################################################################################

# ---------------------------------------------------------------------------------------------------------------------
class AccessoriesListRowBuilder(object):

    def __init__(self, ID, Product_Code, Manufacturer, Description, Voltage,
                 Dimming_Type, Notes, Max_Wattage, Finite_Code, Finite_Solutions_Buy_Price,
                 Discount_off_published_Trade_Price, Published_manufacturers_Trade_Price_ex_VAT,  Published_manufacturer_Retail_ex_VAT,
                 Finite_Solutions_Sell_price, Finite_Solutions_Margin_Price, Finite_Solutions_Margin_Percentage):

        self.ID = ID
        self.Product_Code = Product_Code
        self.Manufacturer = Manufacturer
        self.Description = Description
        self.Voltage = Voltage
        self.Dimming_Type = Dimming_Type
        self.Notes = Notes
        self.Max_Wattage = Max_Wattage
        self.Finite_Code = Finite_Code
        self.Finite_Solutions_Buy_Price = Finite_Solutions_Buy_Price
        self.Discount_off_published_Trade_Price = Discount_off_published_Trade_Price
        self.Published_manufacturers_Trade_Price_ex_VAT = Published_manufacturers_Trade_Price_ex_VAT
        self.Published_manufacturer_Retail_ex_VAT = Published_manufacturer_Retail_ex_VAT
        self.Finite_Solutions_Sell_price = Finite_Solutions_Sell_price
        self.Finite_Solutions_Margin_Price = Finite_Solutions_Margin_Price
        self.Finite_Solutions_Margin_Percentage = Finite_Solutions_Margin_Percentage

class DriversListRowBuilder(object):
    def __init__(self, ID, Product_Code, Manufacturer, Description, Voltage,
                 Dimming_Type, Notes, Max_Wattage, Finite_Code, Finite_Solutions_Buy_Price,
                 Discount_off_published_Trade_Price, Published_manufacturer_Trade_Price_ex_VAT, Published_manufacturer_Retail_ex_VAT,
                 Finite_Solutions_Sell_price, Finite_Solutions_Margin_Price, Finite_Solutions_Margin_Percentage):
        self.ID = ID
        self.Product_Code = Product_Code
        self.Manufacturer = Manufacturer
        self.Description = Description
        self.Voltage = Voltage
        self.Dimming_Type = Dimming_Type
        self.Notes = Notes
        self.Max_Wattage = Max_Wattage
        self.Finite_Code = Finite_Code
        self.Finite_Solutions_Buy_Price = Finite_Solutions_Buy_Price
        self.Discount_off_published_Trade_Price = Discount_off_published_Trade_Price
        self.Published_manufacturer_Trade_Price_ex_VAT = Published_manufacturer_Trade_Price_ex_VAT
        self.Published_manufacturer_Retail_ex_VAT = Published_manufacturer_Retail_ex_VAT
        self.Finite_Solutions_Sell_price = Finite_Solutions_Sell_price
        self.Finite_Solutions_Margin_Price = Finite_Solutions_Margin_Price
        self.Finite_Solutions_Margin_Percentage = Finite_Solutions_Margin_Percentage

class FittingListRowBuilder(object):
    def __init__(self, ID, Product_Code, Manufacturer, Fitting_Type, Fitting_Description,
                 IP_Rating, Dimmable, Voltage_Min, Voltage_Max, Voltage_Type, Wattage, Colour, Beam_Angle, Colour_Temperature, CRI, Lumens, Image_Name, Sage_Category,
                 Finite_Code, Unit_of_measure, Warrenty, Notes, Finite_Solutions_Buy_Price, Discount_off_published_Trade_Price, Published_manufacturer_Trade_Price_ex_VAT, Published_manufacturer_Retail_ex_VAT,
                 Finite_Solutions_Sell_price, Finite_Solutions_Margin_Price, Finite_Solutions_Margin_Percentage):
        self.ID = ID
        self.Product_Code = Product_Code
        self.Manufacturer = Manufacturer
        self.Fitting_Type = Fitting_Type
        self.Fitting_Description = Fitting_Description
        self.IP_Rating = IP_Rating
        self.Dimmable = Dimmable
        self.Voltage_Min = Voltage_Min
        self.Voltage_Max = Voltage_Max
        self.Voltage_Type = Voltage_Type
        self.Wattage = Wattage
        self.Colour = Colour
        self.Beam_Angle = Beam_Angle
        self.Colour_Temperature = Colour_Temperature
        self.CRI = CRI
        self.Lumens = Lumens
        self.Image_Name = Image_Name
        self.Sage_Category = Sage_Category
        self.Finite_Code = Finite_Code
        self.Unit_of_measure = Unit_of_measure
        self.Warrenty = Warrenty
        self.Notes = Notes
        self.Finite_Solutions_Buy_Price = Finite_Solutions_Buy_Price
        self.Discount_off_published_Trade_Price = Discount_off_published_Trade_Price
        self.Published_manufacturer_Trade_Price_ex_VAT = Published_manufacturer_Trade_Price_ex_VAT
        self.Published_manufacturer_Retail_ex_VAT = Published_manufacturer_Retail_ex_VAT
        self.Finite_Solutions_Sell_price = Finite_Solutions_Sell_price
        self.Finite_Solutions_Margin_Price = Finite_Solutions_Margin_Price
        self.Finite_Solutions_Margin_Percentage = Finite_Solutions_Margin_Percentage

class LampListRowBuilder(object):
    def __init__(self, ID, Product_Code, Manufacturer, Fitting_Type, Fixing_Type,
                 Dimming_Type, Wattage, Halogen_Equivalent_Wattage, Beam_Angle, Colour_Temperature, CRI, Lumens, Voltage_Type,
                 Finite_Code, Finite_Solutions_Buy_Price, Discount_off_published_Trade_Price, Published_Manufacturer_Trade_Price_ex_VAT, Published_Manufacturer_Retail_ex_VAT,
                 Finite_Solutions_Sell_price, Finite_Solutions_Margin_Price, Finite_Solutions_Margin_Percentage):
        self.ID = ID
        self.Product_Code = Product_Code
        self.Manufacturer = Manufacturer
        self.Fitting_Type = Fitting_Type
        self.Fixing_Type = Fixing_Type
        self.Dimming_Type = Dimming_Type
        self.Wattage = Wattage
        self.Halogen_Equivalent_Wattage = Halogen_Equivalent_Wattage
        self.Beam_Angle = Beam_Angle
        self.Colour_Temperature = Colour_Temperature
        self.CRI = CRI
        self.Lumens = Lumens
        self.Voltage_Type = Voltage_Type
        self.Finite_Code = Finite_Code
        self.Finite_Solutions_Buy_Price = Finite_Solutions_Buy_Price
        self.Discount_off_published_Trade_Price = Discount_off_published_Trade_Price
        self.Published_Manufacturer_Trade_Price_ex_VAT = Published_Manufacturer_Trade_Price_ex_VAT
        self.Published_Manufacturer_Retail_ex_VAT = Published_Manufacturer_Retail_ex_VAT
        self.Finite_Solutions_Sell_price = Finite_Solutions_Sell_price
        self.Finite_Solutions_Margin_Price = Finite_Solutions_Margin_Price
        self.Finite_Solutions_Margin_Percentage = Finite_Solutions_Margin_Percentage

#######################################################################################################################
# Main frame which call the GUI loop and hold the MainPanel and MainMenu bar
# ---------------------------------------------------------------------------------------------------------------------
class MainFrame(wx.Frame):

    ########################################################################
    # creates a instance of the panel "that's what the __init__ means".
    # because of this, it means that the code in this function is only
    # called when the program is started and the GUI loads for the first time
    # means it cannot be used for any calculations i believe!
    # ----------------------------------------------------------------------
    def __init__(self):


        wx.Frame.__init__(self, None, title="Tuck Database Manager! Time To Tuck In!", size=(800, 600))


        login_modal = LoginDialog(self, 'Login')
        res = login_modal.ShowModal()

        username = login_modal.login_in
        password = login_modal.password_in
        panel = MainPanel(self, username, password)


        if login_modal == 0:
           self.OnExitNonEvent()

        if login_modal == 5101:
           self.OnExitNonEvent()

        self.Centre(True)

        self.Show()

    def OnExitNonEvent(self):
        # Closes the program !
        self.Close(True)




