import wx
import Read_And_Write_Files
from SQL import SQLCon
from SQL import SQLGenerateNewID
from SQL import SQLInsertInto
import datetime

server = ''
#server = '192.168.2.114'
database = ''
username = ''
password = ''
driver = ''
port = ''



class CheckDialog(wx.Dialog):
    def __init__(self, parent, title, message, value):
        super(CheckDialog, self).__init__(parent, title=title, size=(500, 100))
        # Create a new panel
        panel = wx.Panel(self)
        self.check_value = 0
        check_dialog_sizer_main = wx.BoxSizer(wx.VERTICAL)
        check_dialog_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.check_dialog_message = wx.StaticText(self, label=message + value)

        self.yes_btn = wx.Button(self, 0, "Yes")
        self.yes_btn.Bind(wx.EVT_BUTTON, lambda event: self.Yes(event, self.check_value))
        self.no_btn = wx.Button(self, 0, "No")
        self.no_btn.Bind(wx.EVT_BUTTON, lambda event: self.No(event, self.check_value))

        check_dialog_sizer.Add(self.yes_btn, 0, wx.ALIGN_CENTER , 10)
        check_dialog_sizer.Add(self.no_btn, 0, wx.ALIGN_CENTER , 10)

        check_dialog_sizer_main.Add(self.check_dialog_message, 0, wx.ALIGN_CENTER | wx.EXPAND, 10)
        check_dialog_sizer_main.Add(check_dialog_sizer, 1, wx.ALIGN_CENTER | wx.EXPAND, 10)
        self.SetSizer(check_dialog_sizer_main)

    def Yes(self, event, check_value):
        self.check_value = 1
        self.EndModal(self.check_value)

    def No(self,event, check_value):
        self.check_value = 0
        self.EndModal(self.check_value)

class LoginDialog(wx.Dialog):
    def __init__(self, parent, title):
        super(LoginDialog, self).__init__(parent, title=title, size=(500, 100))
        panel = wx.Panel(self)
        first_read = Read_And_Write_Files.Read_File('ini.tuk')
        self.manager_server = first_read[0]
        self.manager_database = first_read[1]
        self.manager_driver = first_read[2]
        self.manager_port = first_read[3]
        my_test_list = []
        login_dialog_sizer_main = wx.BoxSizer(wx.VERTICAL)
        login_dialog_sizer_text_static = wx.BoxSizer(wx.HORIZONTAL)
        login_dialog_sizer_text_inputs = wx.BoxSizer(wx.HORIZONTAL)
        login_dialog_sizer_buttons = wx.BoxSizer(wx.HORIZONTAL)

        main_txt_static = wx.StaticText(self, label='Please enter your server login and password')
        login_txt_static = wx.StaticText(self, label='Login:')
        self.login_text_ctrl = wx.TextCtrl(self, -1, "", size=(175, -1))
        password_txt_static = wx.StaticText(self, label='Password:')
        self.password_text_ctrl = wx.TextCtrl(self, -1, "", size=(175, -1))

        self.btn_login = wx.Button(self, -1, "Login")
        self.btn_login.Bind(wx.EVT_BUTTON, lambda event: self.Login(event, self.manager_server,
                                                                    self.manager_database,
                                                                    self.login_text_ctrl.GetValue(),
                                                                    self.password_text_ctrl.GetValue(),
                                                                    self.manager_driver,
                                                                    self.manager_port))
        self.btn_options = wx.Button(self, -1, "Options")
        self.btn_options.Bind(wx.EVT_BUTTON, lambda event: self.Options(event,panel))

        login_dialog_sizer_text_static.Add(main_txt_static, 0, wx.ALIGN_CENTER, 10)

        login_dialog_sizer_text_inputs.Add(login_txt_static, 0, wx.ALIGN_CENTER, 10)
        login_dialog_sizer_text_inputs.Add(self.login_text_ctrl, 0, wx.ALIGN_CENTER, 10)
        login_dialog_sizer_text_inputs.Add(password_txt_static, 0, wx.ALIGN_CENTER, 10)
        login_dialog_sizer_text_inputs.Add(self.password_text_ctrl, 0, wx.ALIGN_CENTER, 10)


        login_dialog_sizer_buttons.Add(self.btn_login, 0, wx.ALIGN_CENTER, 10)
        login_dialog_sizer_buttons.Add(self.btn_options, 0, wx.ALIGN_CENTER, 10)

        login_dialog_sizer_main.Add(login_dialog_sizer_text_static, 1, wx.ALIGN_CENTER | wx.EXPAND, 10)
        login_dialog_sizer_main.Add(login_dialog_sizer_text_inputs, 1, wx.ALIGN_CENTER | wx.EXPAND, 10)
        login_dialog_sizer_main.Add(login_dialog_sizer_buttons, 1, wx.ALIGN_CENTER | wx.EXPAND, 10)
        self.Centre(True)

        self.SetSizer(login_dialog_sizer_main)

    def Login(self,event, server, database, login, password, driver, port):

        login_state = 0

        self.login_in = self.login_text_ctrl.GetValue()
        self.password_in = self.password_text_ctrl.GetValue()

        login_read = Read_And_Write_Files.Read_File('ini.tuk')
        server_in = login_read[0]
        database_in = login_read[1]
        driver_in = login_read[2]
        port_in = login_read[3]

        try:
            open = SQLCon(server_in, database_in, self.login_in, self.password_in, driver_in, port_in)
            login_state = 1
            pass_back_list = {login_state, server_in, database_in, self.login_in}
        except:
            self.showMessageDlg("Your login failed please check your password and username and try again!",
                                "Incorrect Details", wx.OK | wx.CANCEL | wx.ICON_QUESTION)

        if login_state == 1:
            self.EndModal(True)

    def Options(self, event, login_panel):
        database_manager_instance = DataBaseManagerDialog(login_panel, 'Database Manager').ShowModal()

    def showMessageDlg(self, msg, title, style):
        """"""
        dlg = wx.MessageDialog(parent=None, message=msg,
                               caption=title, style=style)
        dlg.ShowModal()
        dlg.Destroy()

    def onInfo(self, event, message):

        self.showMessageDlg(message, wx.OK | wx.ICON_INFORMATION)

class DataBaseManagerDialog(wx.Dialog):

    def __init__(self, parent, title):
        super(DataBaseManagerDialog, self).__init__(parent, title=title, size=(500, 200))
        panel = wx.Panel(self)
        database_manager_sizer_main = wx.BoxSizer(wx.VERTICAL)
        database_manager_sizer_text_inputs_one = wx.BoxSizer(wx.HORIZONTAL)
        database_manager_sizer_text_inputs_two = wx.BoxSizer(wx.HORIZONTAL)
        database_manager_dialog_sizer_buttons = wx.BoxSizer(wx.HORIZONTAL)

        first_read = Read_And_Write_Files.Read_File('ini.tuk')
        server_manager = first_read[0]
        database_manager = first_read[1]
        driver_manager = first_read[2]
        port_manager = first_read[3]

        server_txt_static = wx.StaticText(self, label='Server:')
        self.server_text_ctrl = wx.TextCtrl(self, -1, server_manager, size=(200, -1))

        database_txt_static = wx.StaticText(self, label='Database:')
        self.database_text_ctrl = wx.TextCtrl(self, -1, database_manager, size=(200, -1))

        driver_txt_static = wx.StaticText(self, label='Driver:')
        self.driver_text_ctrl = wx.TextCtrl(self, -1, driver_manager, size=(200, -1))

        port_txt_static = wx.StaticText(self, label='Port:')
        self.port_text_ctrl = wx.TextCtrl(self, -1, port_manager, size=(200, -1))

        self.btn_commit = wx.Button(self, -1, "Commit")
        self.btn_commit.Bind(wx.EVT_BUTTON, lambda event: self.Commit(event, parent))

        self.btn_cancel = wx.Button(self, -1, "Cancel")
        self.btn_cancel.Bind(wx.EVT_BUTTON, lambda event: self.Cancel(event))

        database_manager_sizer_text_inputs_one.Add(server_txt_static, 0, wx.ALIGN_CENTER, 10)
        database_manager_sizer_text_inputs_one.Add(self.server_text_ctrl, 0, wx.ALIGN_CENTER, 10)

        database_manager_sizer_text_inputs_one.Add(database_txt_static, 0, wx.ALIGN_CENTER, 10)
        database_manager_sizer_text_inputs_one.Add(self.database_text_ctrl, 0, wx.ALIGN_CENTER, 10)

        database_manager_sizer_text_inputs_two.Add(driver_txt_static, 0, wx.ALIGN_CENTER, 10)
        database_manager_sizer_text_inputs_two.Add(self.driver_text_ctrl, 0, wx.ALIGN_CENTER, 10)

        database_manager_sizer_text_inputs_two.Add(port_txt_static, 0, wx.ALIGN_CENTER, 10)
        database_manager_sizer_text_inputs_two.Add(self.port_text_ctrl, 0, wx.ALIGN_CENTER, 10)

        database_manager_dialog_sizer_buttons.Add(self.btn_commit, 0, wx.ALIGN_CENTER, 10)
        database_manager_dialog_sizer_buttons.Add(self.btn_cancel, 0, wx.ALIGN_CENTER, 10)

        database_manager_sizer_main.Add(database_manager_sizer_text_inputs_one, 0, wx.ALIGN_CENTER, 10)
        database_manager_sizer_main.Add(database_manager_sizer_text_inputs_two, 0, wx.ALIGN_CENTER, 10)
        database_manager_sizer_main.Add(database_manager_dialog_sizer_buttons, 0, wx.ALIGN_CENTER, 10)

        self.Centre(True)
        self.SetSizer(database_manager_sizer_main)
        self.Fit()

    def Commit(self, event, login_panel):

        manager_server = self.server_text_ctrl.GetValue()
        manager_database = self.database_text_ctrl.GetValue()
        manager_driver = self.driver_text_ctrl.GetValue()
        manager_port = self.port_text_ctrl.GetValue()

        manager_list = [ manager_server, manager_database, manager_driver, manager_port]
        first_read = Read_And_Write_Files.Read_File('ini.tuk')
        commit_to_file = Read_And_Write_Files.Build_File.header_structure(self, manager_list, 'ini.tuk')
        self.EndModal(True)
        return(manager_list)




    def Cancel(self, event):
        self.EndModal(True)

class AddFittingModal(wx.Dialog):
    def __init__(self,  parent, title, username, password, table, login_state):
        super(AddFittingModal, self).__init__(parent, title=title, size=(500, 200))
        panel = wx.Panel(self)
        grid_sizer_one = wx.FlexGridSizer( 2, 29, 0)
        grid_sizer_two = wx.FlexGridSizer( 2, 29, 0)
        sizer_wrapper = wx.BoxSizer(wx.HORIZONTAL)
        sizer_main = wx.BoxSizer(wx.VERTICAL)


        sizer_wrapper.AddSpacer(10)
        sizer_wrapper.Add(grid_sizer_one, 0,  wx.ALIGN_TOP)
        sizer_wrapper.AddSpacer(5)
        sizer_wrapper.Add(grid_sizer_two, 0,  wx.ALIGN_TOP)
        sizer_wrapper.AddSpacer(10)

        sizer_main.AddSpacer(10)
        sizer_main.Add(sizer_wrapper, 0, wx.ALIGN_CENTER)
        sizer_main.AddSpacer(10)

        self.product_code_text_ctrl = wx.TextCtrl(self, -1, "", size=(175, -1))
        self.product_code_static_text = wx.StaticText(self, label='Product Code:')
        grid_sizer_one.Add(self.product_code_static_text, 0, wx.ALIGN_RIGHT, 2)
        grid_sizer_one.Add(self.product_code_text_ctrl, 0, wx.ALIGN_CENTER, 2)


        self.manufacturer_text_ctrl = wx.TextCtrl(self, -1, "", size=(175, -1))
        self.manufacturer_static_text = wx.StaticText(self, label='Manufacturer:')
        grid_sizer_one.Add(self.manufacturer_static_text, 0, wx.ALIGN_RIGHT, 2)
        grid_sizer_one.Add(self.manufacturer_text_ctrl, 0, wx.ALIGN_CENTER, 2)


        self.fitting_type_text_ctrl = wx.TextCtrl(self, -1, "", size=(175, -1))
        self.fitting_type_static_text = wx.StaticText(self, label='Fitting Type:')
        grid_sizer_one.Add(self.fitting_type_static_text, 0, wx.ALIGN_RIGHT, 2)
        grid_sizer_one.Add(self.fitting_type_text_ctrl, 0, wx.ALIGN_CENTER, 2)


        self.fitting_description_text_ctrl = wx.TextCtrl(self, -1, "", size=(175, -1))
        self.fitting_description_static_text = wx.StaticText(self, label='Fitting Description:')
        grid_sizer_one.Add(self.fitting_description_static_text, 0, wx.ALIGN_RIGHT, 2)
        grid_sizer_one.Add(self.fitting_description_text_ctrl, 0, wx.ALIGN_CENTER, 2)


        self.IP_rating_text_ctrl = wx.TextCtrl(self, -1, "", size=(175, -1))
        self.IP_rating_static_text = wx.StaticText(self, label='IP Rating:')
        grid_sizer_one.Add(self.IP_rating_static_text, 0, wx.ALIGN_RIGHT, 2)
        grid_sizer_one.Add(self.IP_rating_text_ctrl, 0, wx.ALIGN_CENTER, 2)


        self.dimmable_text_ctrl = wx.TextCtrl(self, -1, "", size=(175, -1))
        self.dimmable_static_text = wx.StaticText(self, label='Dimmable:')
        grid_sizer_one.Add(self.dimmable_static_text, 0, wx.ALIGN_RIGHT, 2)
        grid_sizer_one.Add(self.dimmable_text_ctrl, 0, wx.ALIGN_CENTER, 2)


        self.voltage_min_text_ctrl = wx.TextCtrl(self, -1, "", size=(175, -1))
        self.voltage_min_static_text = wx.StaticText(self, label='Voltage Min:')
        grid_sizer_one.Add(self.voltage_min_static_text, 0, wx.ALIGN_RIGHT, 2)
        grid_sizer_one.Add(self.voltage_min_text_ctrl, 0, wx.ALIGN_CENTER, 2)


        self.voltage_max_text_ctrl = wx.TextCtrl(self, -1, "", size=(175, -1))
        self.voltage_max_static_text = wx.StaticText(self, label='Voltage Max:')
        grid_sizer_one.Add(self.voltage_max_static_text, 0, wx.ALIGN_RIGHT, 2)
        grid_sizer_one.Add(self.voltage_max_text_ctrl, 0, wx.ALIGN_CENTER, 2)


        self.voltage_type_text_ctrl = wx.TextCtrl(self, -1, "", size=(175, -1))
        self.voltage_type_static_text = wx.StaticText(self, label='Voltage Type:')
        grid_sizer_one.Add(self.voltage_type_static_text, 0, wx.ALIGN_RIGHT, 2)
        grid_sizer_one.Add(self.voltage_type_text_ctrl, 0, wx.ALIGN_CENTER, 2)


        self.wattage_text_ctrl = wx.TextCtrl(self, -1, "", size=(175, -1))
        self.wattage_static_text = wx.StaticText(self, label='Wattage:')
        grid_sizer_one.Add(self.wattage_static_text, 0, wx.ALIGN_RIGHT, 2)
        grid_sizer_one.Add(self.wattage_text_ctrl, 0, wx.ALIGN_CENTER, 2)


        self.color_text_ctrl = wx.TextCtrl(self, -1, "", size=(175, -1))
        self.color_static_text = wx.StaticText(self, label='Color:')
        grid_sizer_one.Add(self.color_static_text, 0, wx.ALIGN_RIGHT, 2)
        grid_sizer_one.Add(self.color_text_ctrl, 0, wx.ALIGN_CENTER, 2)


        self.beam_angle_text_ctrl = wx.TextCtrl(self, -1, "", size=(175, -1))
        self.beam_angle_static_text = wx.StaticText(self, label='Beam Angle:')
        grid_sizer_one.Add(self.beam_angle_static_text, 0, wx.ALIGN_RIGHT, 2)
        grid_sizer_one.Add(self.beam_angle_text_ctrl, 0, wx.ALIGN_CENTER, 2)


        self.colour_temperature_text_ctrl = wx.TextCtrl(self, -1, "", size=(175, -1))
        self.colour_temperature_static_text = wx.StaticText(self, label='Color Temperature:')
        grid_sizer_one.Add(self.colour_temperature_static_text, 0, wx.ALIGN_RIGHT, 2)
        grid_sizer_one.Add(self.colour_temperature_text_ctrl, 0, wx.ALIGN_CENTER, 2)


        self.CRI_text_ctrl = wx.TextCtrl(self, -1, "", size=(175, -1))
        self.CRI_static_text = wx.StaticText(self, label='CRI:')
        grid_sizer_one.Add(self.CRI_static_text, 0, wx.ALIGN_RIGHT, 2)
        grid_sizer_one.Add(self.CRI_text_ctrl, 0, wx.ALIGN_CENTER, 2)


        self.lumens_text_ctrl = wx.TextCtrl(self, -1, "", size=(175, -1))
        self.lumens_static_text = wx.StaticText(self, label='Lumens:')
        grid_sizer_two.Add(self.lumens_static_text, 0, wx.ALIGN_RIGHT, 2)
        grid_sizer_two.Add(self.lumens_text_ctrl, 0, wx.ALIGN_CENTER, 2)


        self.image_name_text_ctrl = wx.TextCtrl(self, -1, "", size=(175, -1))
        self.image_name_static_text = wx.StaticText(self, label='Image Name:')
        grid_sizer_two.Add(self.image_name_static_text, 0, wx.ALIGN_RIGHT, 2)
        grid_sizer_two.Add(self.image_name_text_ctrl, 0, wx.ALIGN_CENTER, 2)


        self.sage_category_text_ctrl = wx.TextCtrl(self, -1, "", size=(175, -1))
        self.sage_category_static_text = wx.StaticText(self, label='Sage Category:')
        grid_sizer_two.Add(self.sage_category_static_text, 0, wx.ALIGN_RIGHT, 2)
        grid_sizer_two.Add(self.sage_category_text_ctrl, 0, wx.ALIGN_CENTER, 2)


        self.finite_code_text_ctrl = wx.TextCtrl(self, -1, "", size=(175, -1))
        self.finite_code_static_text = wx.StaticText(self, label='Finite Code:')
        grid_sizer_two.Add(self.finite_code_static_text, 0, wx.ALIGN_RIGHT, 2)
        grid_sizer_two.Add(self.finite_code_text_ctrl, 0, wx.ALIGN_CENTER, 2)


        self.unit_of_measure_text_ctrl = wx.TextCtrl(self, -1, "", size=(175, -1))
        self.unit_of_measure_static_text = wx.StaticText(self, label='Unit Of Measure:')
        grid_sizer_two.Add(self.unit_of_measure_static_text, 0, wx.ALIGN_RIGHT, 2)
        grid_sizer_two.Add(self.unit_of_measure_text_ctrl, 0, wx.ALIGN_CENTER, 2)


        self.warrenty_text_ctrl = wx.TextCtrl(self, -1, "", size=(175, -1))
        self.warrenty_static_text = wx.StaticText(self, label='Warrenty:')
        grid_sizer_two.Add(self.warrenty_static_text, 0, wx.ALIGN_RIGHT, 2)
        grid_sizer_two.Add(self.warrenty_text_ctrl, 0, wx.ALIGN_CENTER, 2)


        self.note_text_ctrl = wx.TextCtrl(self, -1, "", size=(175, -1))
        self.note_static_text = wx.StaticText(self, label='Note:')
        grid_sizer_two.Add(self.note_static_text, 0, wx.ALIGN_RIGHT, 2)
        grid_sizer_two.Add(self.note_text_ctrl, 0, wx.ALIGN_CENTER, 2)


        self.buy_price_text_ctrl = wx.TextCtrl(self, -1, "", size=(175, -1))
        self.buy_price_static_text = wx.StaticText(self, label='Finite Solutions buy price:')
        grid_sizer_two.Add(self.buy_price_static_text, 0, wx.ALIGN_RIGHT, 2)
        grid_sizer_two.Add(self.buy_price_text_ctrl, 0, wx.ALIGN_CENTER, 2)


        self.trade_price_text_ctrl = wx.TextCtrl(self, -1, "", size=(175, -1))
        self.trade_price_static_text = wx.StaticText(self, label='Discount off published Trade Price:')
        grid_sizer_two.Add(self.trade_price_static_text, 0, wx.ALIGN_RIGHT, 2)
        grid_sizer_two.Add(self.trade_price_text_ctrl, 0, wx.ALIGN_CENTER, 2)


        self.trade_price_ex_vat_text_ctrl = wx.TextCtrl(self, -1, "", size=(175, -1))
        self.trade_price_static_text = wx.StaticText(self, label='Published manufacturer Trade Price ex VAT:')
        grid_sizer_two.Add(self.trade_price_static_text, 0, wx.ALIGN_RIGHT, 2)
        grid_sizer_two.Add(self.trade_price_ex_vat_text_ctrl, 0, wx.ALIGN_CENTER, 2)


        self.trade_retail_price_ex_vat_text_ctrl = wx.TextCtrl(self, -1, "", size=(175, -1))
        self.trade_retail_price_static_text = wx.StaticText(self, label='Published manufacturer Retail ex VAT:')
        grid_sizer_two.Add(self.trade_retail_price_static_text, 0, wx.ALIGN_RIGHT, 0)
        grid_sizer_two.Add(self.trade_retail_price_ex_vat_text_ctrl, 0, wx.ALIGN_CENTER, 0)


        self.sell_price_text_ctrl = wx.TextCtrl(self, -1, "", size=(175, -1))
        self.sell_price_static_text = wx.StaticText(self, label='Finite Solutions sell price:')
        grid_sizer_two.Add(self.sell_price_static_text, 0, wx.ALIGN_RIGHT, 0)
        grid_sizer_two.Add(self.sell_price_text_ctrl, 0, wx.ALIGN_CENTER, 0)


        self.sell_margin_price_text_ctrl = wx.TextCtrl(self, -1, "", size=(175, -1))
        self.sell_margin_price_static_text = wx.StaticText(self, label='Finite Solutions Margin Price:')
        grid_sizer_two.Add(self.sell_margin_price_static_text, 0, wx.ALIGN_RIGHT, 0)
        grid_sizer_two.Add(self.sell_margin_price_text_ctrl, 0, wx.ALIGN_CENTER, 0)


        self.sell_margin_percentage_text_ctrl = wx.TextCtrl(self, -1, "", size=(175, -1))
        self.sell_margin_percentage_static_text = wx.StaticText(self, label='Finite Solutions Margin Percentage:')
        grid_sizer_two.Add(self.sell_margin_percentage_static_text, 0, wx.ALIGN_RIGHT, 0)
        grid_sizer_two.Add(self.sell_margin_percentage_text_ctrl, 0, wx.ALIGN_CENTER, 0)


        self.commit_btn = wx.Button(self, 0, "Commit")
        self.commit_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnCommit(username, password, table))
        self.cancel_btn = wx.Button(self, 0, "Cancel")
        self.cancel_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnCancel(event))

        grid_sizer_two.Add(self.commit_btn, 0, wx.ALIGN_RIGHT, 0)
        grid_sizer_two.Add(self.cancel_btn, 0, wx.ALIGN_LEFT, 0)

       # self.Centre()
        self.SetSizer(sizer_main)
        self.Fit()

    def NextSelection(self, event, next_selected):
        a = event.GetKeyCode()
        if a == 370:
            next_selected.SetFocus()


    def OnCommit(self, username, password, table):
        build_list = ()
        load_read = Read_And_Write_Files.Read_File('ini.tuk')
        open_con = SQLCon(load_read[0], load_read[1], username, password, load_read[2], load_read[3])
        new_id_generated = SQLGenerateNewID(open_con, table)

        insert_list = [new_id_generated,
                       self.product_code_text_ctrl.GetValue(),
                       self.manufacturer_text_ctrl.GetValue(),
                       self.fitting_type_text_ctrl.GetValue(),
                       self.fitting_description_text_ctrl.GetValue(),
                       self.IP_rating_text_ctrl.GetValue(),
                       self.dimmable_text_ctrl.GetValue(),
                       self.voltage_min_text_ctrl.GetValue(),
                       self.voltage_max_text_ctrl.GetValue(),
                       self.voltage_type_text_ctrl.GetValue(),
                       self.wattage_text_ctrl.GetValue(),
                       self.color_text_ctrl.GetValue(),
                       self.beam_angle_text_ctrl.GetValue(),
                       self.colour_temperature_text_ctrl.GetValue(),
                       self.CRI_text_ctrl.GetValue(),
                       self.lumens_text_ctrl.GetValue(),
                       self.image_name_text_ctrl.GetValue(),
                       self.sage_category_text_ctrl.GetValue(),
                       self.finite_code_text_ctrl.GetValue(),
                       self.unit_of_measure_text_ctrl.GetValue(),
                       self.warrenty_text_ctrl.GetValue(),
                       self.note_text_ctrl.GetValue(),
                       self.buy_price_text_ctrl.GetValue(),
                       self.trade_price_text_ctrl.GetValue(),
                       self.trade_price_ex_vat_text_ctrl.GetValue(),
                       self.trade_retail_price_ex_vat_text_ctrl.GetValue(),
                       self.sell_price_text_ctrl.GetValue(),
                       self.sell_margin_price_text_ctrl.GetValue(),
                       self.sell_margin_percentage_text_ctrl.GetValue()]

        for x in range(len(insert_list)):
            if insert_list[x] == "":
                insert_list[x] = "Not Applicable"


        for x in range(len(insert_list)):
            build_list = build_list + (insert_list[x],)

        run_insert = SQLInsertInto(open_con, '', username, table, build_list)

        # ---------------------------------------------------------------------------------------------------------
        # Update the user_log with the querry
        # ---------------------------------------------------------------------------------------------------------
        load_read = Read_And_Write_Files.Read_File('ini.tuk')
        user_con = SQLCon(load_read[0], load_read[1], username, password, load_read[2], load_read[3])
        new_id_generated = SQLGenerateNewID(user_con, 'User_Logs')
            # Get date at time
        now = datetime.datetime.now()
        date_now = now.date()
        time_now = now.time()
            # Create list for user log insert
        user_list = (new_id_generated, username, 'Insert data into table', table, "Database ID =" + str(new_id_generated), str(date_now), str(time_now))
        # Close connections
        SQLInsertInto(user_con, "", "", 'User_Logs', user_list)
        open_con.close()
        user_con.close()


    def OnCancel(self, event):
        self.EndModal(True)

