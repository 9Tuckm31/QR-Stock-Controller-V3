# --------------------------------------------------------------------------
'''-------------------------------------------------------------------------
This python file is for the creation of the GUI elements for each modal.
I may also put in some other functions for the modals, just so they are
all in one place.
-------------------------------------------------------------------------'''
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# Import Library's
# --------------------------------------------------------------------------
#----------------------------------------
import wx
import SQL
import Data_Transforms
from SQL import SQLCon
import GUI
import Object_List_View_Builder
from ObjectListView import ObjectListView, ColumnDefn
import Read_And_Write_Files

################################################################################################################
# Popup messages !
################################################################################################################

def ShowMessageDlg(self, msg, title, style):

    dlg = wx.MessageDialog(parent=None, message=msg,
                            caption=title, style=style)

    result = dlg.ShowModal() == wx.ID_OK
    dlg.Destroy()
    return result

################################################################################################################
################################################################################################################
# Modals menu bar!
################################################################################################################
################################################################################################################

# --------------------------------------------------------------------------------------------
# File drop down menu button
# --------------------------------------------------------------------------------------------

class OpenDialog(wx.Dialog):
    def __init__(self, parent, title):
        super(OpenDialog, self).__init__(parent, title=title, size=(600, 300))

class LoginDialog(wx.Dialog):
    def __init__(self, parent, title):

        super(LoginDialog, self).__init__(parent, title=title, size=(600, 300))
        login_grid_sizer = wx.FlexGridSizer(2,2,2)
        login_wrapper_sizer = wx.BoxSizer(wx.VERTICAL)
        login_main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        login_btn_wrapper_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.info_static_text = wx.StaticText(self, label="Please enter in your username and password")
        self.login_static_text = wx.StaticText(self, label="Login: ")
        self.password_static_text = wx.StaticText(self, label="Password: ")

        self.login_text_control = wx.TextCtrl(self, -1, "Jeff", size=(175, -1))
        self.password_text_ctrl = wx.TextCtrl(self, -1, "password1", size=(175, -1))

        self.login_btn = wx.Button(self, 0, label="Login")
        self.login_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnLogin(event,
                                                                      self.login_text_control.GetValue(),
                                                                      self.password_text_ctrl.GetValue()))
        self.option_btn = wx.Button(self, 0, label="Options")
        self.option_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnOption(event))
        self.cancel_btn = wx.Button(self, 0, label="Cancel")
        self.cancel_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnCancel(event))

        login_grid_sizer.Add(self.login_static_text, 0, wx.ALIGN_LEFT, 10)
        login_grid_sizer.Add(self.login_text_control, 0, wx.ALIGN_LEFT, 10)
        login_grid_sizer.Add(self.password_static_text, 0, wx.ALIGN_LEFT, 10)
        login_grid_sizer.Add(self.password_text_ctrl, 0, wx.ALIGN_LEFT, 10)

        login_btn_wrapper_sizer.Add(self.login_btn, 0, wx.ALIGN_RIGHT, 10)
        login_btn_wrapper_sizer.Add(self.option_btn, 0, wx.ALIGN_CENTER, 10)
        login_btn_wrapper_sizer.Add(self.cancel_btn, 0, wx.ALIGN_LEFT, 10)

        login_wrapper_sizer.AddSpacer(10)
        login_wrapper_sizer.Add(self.info_static_text, 0, wx.ALIGN_LEFT, 10)
        login_wrapper_sizer.AddSpacer(5)
        login_wrapper_sizer.Add(login_grid_sizer, 0, wx.ALIGN_LEFT | wx.ALL, 10)
        login_wrapper_sizer.AddSpacer(5)
        login_wrapper_sizer.Add(login_btn_wrapper_sizer, 0, wx.ALIGN_LEFT | wx.ALL, 10)
        login_wrapper_sizer.AddSpacer(10)

        login_main_sizer.AddSpacer(50)
        login_main_sizer.Add(login_wrapper_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        login_main_sizer.AddSpacer(50)

        self.SetSizer(login_main_sizer)
        login_main_sizer.Fit(self)

    def OnLogin(self, event, username, password):
        login_state = 0
        login_read = Read_And_Write_Files.Read_File('data_conn.tuk')
        server_in = login_read[0]
        database_in = login_read[1]
        port_in = login_read[2]
        driver_in = login_read[3]


        try:
            open_con = SQLCon(server_in, database_in, username, password, driver_in, port_in)
            login_state = 1
            pass_back_list = {login_state, server_in, database_in, username}
            #self.showMessageDlg("You are logged in!"
             #                   , wx.OK | wx.CANCEL | wx.ICON_QUESTION)
        except:
            self.showMessageDlg("Your login failed please check your password and username and try again!",
                                "Incorrect Details"
                                , wx.OK | wx.CANCEL | wx.ICON_QUESTION)

        if login_state == 1:
            self.showMessageDlg("You are logged in","Welcome Back", wx.OK | wx.CANCEL | wx.ICON_QUESTION)

            user_build_list = [username, password]
            commit_to_file = Read_And_Write_Files.Build_File('N/A', user_build_list, 'user.tuk')

            self.EndModal(True)
        #self.EndModal(True)

    def OnOption(self, event):
        data_base_manager_dialog = DatabaseManagerDialog(self, 'Database Manager').ShowModal()

    def OnCancel(self, event):
        self.EndModal(True)

    def showMessageDlg(self, msg, title, style):
        """"""
        dlg = wx.MessageDialog(parent=None, message=msg,
                               caption=title, style=style)
        dlg.ShowModal()
        dlg.Destroy()

class LogOutDialog(wx.Dialog):
    def __init__(self, parent, title):
        super(LogOutDialog, self).__init__(parent, title=title, size=(600, 300))

# --------------------------------------------------------------------------------------------
# Edit drop down menu button
# --------------------------------------------------------------------------------------------

class CompanyInfoDialog(wx.Dialog):
    # These values should all be pulled from the database !

    def __init__(self, parent, title, company_name,company_owner,company_vocation,
                                 company_year_established,company_address,company_contact_number,logo_file_path):
        super(CompanyInfoDialog, self).__init__(parent, title=title, size=(600, 300))
        # ----------------------------------------------------------------
        # Create dynamic vars
        # ----------------------------------------------------------------

        # ----------------------------------------------------------------
        # Create buttons
        # ----------------------------------------------------------------
        self.company_info_ok_btn = wx.Button(self, 0, label="Ok")
        self.company_info_ok_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnOk(event))
        self.company_info_edit_btn = wx.Button(self, 0, label="Edit")
        self.company_info_edit_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnEdit(event, parent,
                                                                                 self.company_info_name_txt_display.GetLabel(),
                                                                                 self.company_info_owner_txt_display.GetLabel(),
                                                                                 self.company_info_vocation_txt_display.GetLabel(),
                                                                                 self.company_info_year_established_txt_display.GetLabel(),
                                                                                 self.company_info_address_txt_display.GetLabel(),
                                                                                 self.company_info_contact_number_txt_display.GetLabel(),
                                                                                 self.company_info_logo_file_path_text.GetLabel()))
        # ----------------------------------------------------------------
        # Create static text
        # ----------------------------------------------------------------
        self.company_info_name_txt_title = wx.StaticText(self, -1, "Company Name:  ", (20, 20))
        self.company_info_name_txt_display = wx.StaticText(self, -1, company_name, (20, 20))

        self.company_info_owner_txt_title = wx.StaticText(self, -1, "Registered Owner:  ", (20, 20))
        self.company_info_owner_txt_display = wx.StaticText(self, -1, company_owner, (20, 20))

        self.company_info_vocation_txt_title = wx.StaticText(self, -1, "Company Vocation/Services Description:  ", (20, 20))
        self.company_info_vocation_txt_display = wx.StaticText(self, -1, company_vocation, (20, 20))

        self.company_info_year_established_txt_title = wx.StaticText(self, -1, "Year company was established:  ", (20, 20))
        self.company_info_year_established_txt_display = wx.StaticText(self, -1, company_year_established, (20, 20))

        self.company_info_address_txt_title = wx.StaticText(self, -1, "Company address:  ", (20, 20))
        self.company_info_address_txt_display = wx.StaticText(self, -1, company_address, (20, 20))

        self.company_info_contact_number_txt_title = wx.StaticText(self, -1, "Company contact number:  ", (20, 20))
        self.company_info_contact_number_txt_display = wx.StaticText(self, -1, company_contact_number, (20, 20))

        if logo_file_path != "":
            self.company_info_logo_file_path_text = wx.StaticText(self, -1, logo_file_path, (200, 20))
        # ----------------------------------------------------------------
        # Create the logo image view here !
        # ----------------------------------------------------------------
        company_info_logo_control = wx.EmptyImage(300, 300)
        self.imageCtrl = wx.StaticBitmap(self, wx.ID_ANY,
                                        wx.BitmapFromImage(company_info_logo_control))
        self.PhotoMaxSize = 300

        # ----------------------------------------------------------------
        # Create sizer's
        # ----------------------------------------------------------------
        company_info_btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        company_info_name_txt_sizer = wx.BoxSizer(wx.HORIZONTAL)
        company_info_owner_txt_sizer = wx.BoxSizer(wx.HORIZONTAL)
        company_info_vocation_txt_sizer = wx.BoxSizer(wx.HORIZONTAL)
        company_info_year_established_txt_sizer = wx.BoxSizer(wx.HORIZONTAL)
        company_info_address_txt_sizer = wx.BoxSizer(wx.HORIZONTAL)
        company_info_contact_number_txt_sizer = wx.BoxSizer(wx.HORIZONTAL)
        company_info_logo_file_path_sizer = wx.BoxSizer(wx.HORIZONTAL)
        company_info_logo_sizer = wx.BoxSizer(wx.HORIZONTAL)
        company_info_inner_sizer = wx.BoxSizer(wx.VERTICAL)
        company_info_wrapper_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # ----------------------------------------------------------------
        # Add buttons to button sizer
        # ----------------------------------------------------------------
        company_info_btn_sizer.Add(self.company_info_ok_btn, 0, wx.ALIGN_CENTER, 10)
        company_info_btn_sizer.Add(self.company_info_edit_btn, 0, wx.ALIGN_CENTER, 10)
        # ----------------------------------------------------------------
        # Add static text to text sizer's
        # ----------------------------------------------------------------
        company_info_name_txt_sizer.Add(self.company_info_name_txt_title, 0, wx.ALL | wx.ALIGN_CENTER)
        company_info_name_txt_sizer.Add(self.company_info_name_txt_display, 0, wx.ALL | wx.ALIGN_CENTER)
        # ----------------------------------------------------------------
        company_info_owner_txt_sizer.Add(self.company_info_owner_txt_title, 0, wx.ALL | wx.ALIGN_CENTER)
        company_info_owner_txt_sizer.Add(self.company_info_owner_txt_display, 0, wx.ALL | wx.ALIGN_CENTER)
        # ----------------------------------------------------------------
        company_info_vocation_txt_sizer.Add(self.company_info_vocation_txt_title, 0, wx.ALL | wx.ALIGN_CENTER)
        company_info_vocation_txt_sizer.Add(self.company_info_vocation_txt_display, 0, wx.ALL | wx.ALIGN_CENTER)
        # ----------------------------------------------------------------
        company_info_year_established_txt_sizer.Add(self.company_info_year_established_txt_title, 0, wx.ALL | wx.ALIGN_CENTER)
        company_info_year_established_txt_sizer.Add(self.company_info_year_established_txt_display, 0, wx.ALL | wx.ALIGN_CENTER)
        # ----------------------------------------------------------------
        company_info_address_txt_sizer.Add(self.company_info_address_txt_title, 0, wx.ALL | wx.ALIGN_CENTER)
        company_info_address_txt_sizer.Add(self.company_info_address_txt_display, 0, wx.ALL | wx.ALIGN_CENTER)
        # ----------------------------------------------------------------
        company_info_contact_number_txt_sizer.Add(self.company_info_contact_number_txt_title, 0, wx.ALL | wx.ALIGN_CENTER)
        company_info_contact_number_txt_sizer.Add(self.company_info_contact_number_txt_display, 0, wx.ALL | wx.ALIGN_CENTER)
        # ----------------------------------------------------------------
        company_info_logo_file_path_sizer.Add(self.company_info_logo_file_path_text, 0, wx.ALL | wx.ALIGN_CENTER)
        # ----------------------------------------------------------------
        # Logo image view to sizer
        # ----------------------------------------------------------------
        company_info_logo_sizer.Add(self.imageCtrl, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        self.OnView()

        # ----------------------------------------------------------------
        # Add text and button sizer's to the inner sizer
        # ----------------------------------------------------------------
        company_info_inner_sizer.AddSpacer(5)
        company_info_inner_sizer.Add(company_info_name_txt_sizer, 0, wx.ALL | wx.ALIGN_CENTER)
        company_info_inner_sizer.AddSpacer(5)
        company_info_inner_sizer.Add(company_info_owner_txt_sizer, 0, wx.ALL | wx.ALIGN_CENTER)
        company_info_inner_sizer.AddSpacer(5)
        company_info_inner_sizer.Add(company_info_vocation_txt_sizer, 0, wx.ALL | wx.ALIGN_CENTER)
        company_info_inner_sizer.AddSpacer(5)
        company_info_inner_sizer.Add(company_info_year_established_txt_sizer, 0, wx.ALL | wx.ALIGN_CENTER)
        company_info_inner_sizer.AddSpacer(5)
        company_info_inner_sizer.Add(company_info_address_txt_sizer, 0, wx.ALL | wx.ALIGN_CENTER)
        company_info_inner_sizer.AddSpacer(5)
        company_info_inner_sizer.Add(company_info_contact_number_txt_sizer, 0, wx.ALL | wx.ALIGN_CENTER)
        company_info_inner_sizer.AddSpacer(5)
        company_info_inner_sizer.Add(company_info_logo_file_path_sizer, 0, wx.ALL | wx.ALIGN_CENTER)
        company_info_inner_sizer.AddSpacer(5)
        company_info_inner_sizer.Add(company_info_logo_sizer, 1, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER)
        company_info_inner_sizer.AddSpacer(5)
        company_info_inner_sizer.Add(company_info_btn_sizer, 0, wx.ALL)
        company_info_inner_sizer.AddSpacer(5)
        # ----------------------------------------------------------------
        company_info_wrapper_sizer.AddSpacer(10)
        company_info_wrapper_sizer.Add(company_info_inner_sizer, 0, wx.ALL)
        company_info_wrapper_sizer.AddSpacer(10)
        # ----------------------------------------------------------------

        # ----------------------------------------------------------------
        width = 300  # panel width
        self.company_info_logo_file_path_text.Wrap(width)
        # ----------------------------------------------------------------
        self.SetSizer(company_info_wrapper_sizer)
        company_info_wrapper_sizer.Fit(self)


    def OnOk(self,event):
        self.EndModal(True)

    def OnEdit(self,event, parent, company_name, company_owner, company_vocation, company_year_established,
               company_address, company_contact_number, logo_file_path):
        CompanyInfoEditDialog(self,  'Edit',
                              company_name,
                              company_owner,
                              company_vocation,
                              company_year_established,
                              company_address,
                              company_contact_number,
                              logo_file_path).ShowModal()

    def OnView(self):
        filepath = self.company_info_logo_file_path_text.GetLabel()
        company_info_logo_control = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
        # scale the image, preserving the aspect ratio
        W = company_info_logo_control.GetWidth()
        H = company_info_logo_control.GetHeight()
        if W > H:
            NewW = self.PhotoMaxSize
            NewH = self.PhotoMaxSize * H / W
        else:
            NewH = self.PhotoMaxSize
            NewW = self.PhotoMaxSize * W / H
        company_info_logo_control = company_info_logo_control.Scale(NewW, NewH)

        self.imageCtrl.SetBitmap(wx.BitmapFromImage(company_info_logo_control))

        self.Refresh()

class CompanyInfoEditDialog(wx.Dialog):
    def __init__(self, parent, title, company_name, company_owner, company_vocation, company_year_established, company_address, company_contact_number, logo_file_path):
        super(CompanyInfoEditDialog, self).__init__(parent, title=title, size=(600, 300))
        # ----------------------------------------------------------------
        # Text Controls
        # ----------------------------------------------------------------
        self.company_edit_name_text_static = wx.StaticText(self, -1, "Company Name:  ", (20, 20))
        self.company_edit_name_text_ctrl = wx.TextCtrl(self, -1, company_name, size=(175, -1))

        self.company_info_owner_text_static = wx.StaticText(self, -1, "Registered Owner:  ", (20, 20))
        self.company_edit_owner_text_ctrl = wx.TextCtrl(self, -1, company_owner, size=(175, -1))

        self.company_edit_vocation_text_static = wx.StaticText(self, -1, "Vocation:  ", (20, 20))
        self.company_edit_vocation_text_ctrl = wx.TextCtrl(self, -1, company_vocation, size=(175, -1))

        self.company_edit_year_text_static = wx.StaticText(self, -1, "Year:  ", (20, 20))
        self.company_edit_year_text_ctrl = wx.TextCtrl(self, -1, company_year_established, size=(175, -1))

        self.company_edit_address_text_static = wx.StaticText(self, -1, "Address:  ", (20, 20))
        self.company_edit_address_text_ctrl = wx.TextCtrl(self, -1, company_address, size=(175, -1))

        self.company_edit_number_text_static = wx.StaticText(self, -1, "Number:  ", (20, 20))
        self.company_edit_number_text_ctrl = wx.TextCtrl(self, -1, company_contact_number, size=(175, -1))

        self.company_edit_logo_text_static = wx.StaticText(self, -1, "Logo Path:  ", (20, 20))
        self.company_edit_logo_text_ctrl = wx.TextCtrl(self, -1, logo_file_path, size=(175, -1))
        # ----------------------------------------------------------------
        # Buttons
        # ----------------------------------------------------------------
        self.company_edit_commit_btn = wx.Button(self, 0, label="Commit")
        self.company_edit_commit_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnCommit(event,parent,
                                                                                     self.company_edit_name_text_ctrl.GetValue(),
                                                                                     self.company_edit_owner_text_ctrl.GetValue(),
                                                                                     self.company_edit_vocation_text_ctrl.GetValue(),
                                                                                     self.company_edit_year_text_ctrl.GetValue(),
                                                                                     self.company_edit_address_text_ctrl.GetValue(),
                                                                                     self.company_edit_number_text_ctrl.GetValue(),
                                                                                     self.company_edit_logo_text_ctrl.GetValue()))
        self.company_edit_cancel_btn = wx.Button(self, 0, label="Cancel")
        self.company_edit_cancel_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnCancel(event))
        self.company_edit_logo_path_btn = wx.Button(self, 0, label="Choose")
        self.company_edit_logo_path_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnChoose(event, parent))
        # ----------------------------------------------------------------
        # Sizer's
        # ----------------------------------------------------------------
        company_edit_btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # ----------------------------------------------------------------
        company_edit_logo_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # ----------------------------------------------------------------
        company_edit_grid_sizer = wx.FlexGridSizer(7, 2, 10, 10)
        # ----------------------------------------------------------------
        company_edit_wrapper_sizer = wx.BoxSizer(wx.HORIZONTAL)
        company_edit_inner_sizer = wx.BoxSizer(wx.VERTICAL)
        # ----------------------------------------------------------------
        # Add buttons to sizer
        # ----------------------------------------------------------------
        company_edit_btn_sizer.Add(self.company_edit_commit_btn, 0, wx.ALIGN_CENTER, 10)
        company_edit_btn_sizer.Add(self.company_edit_cancel_btn, 0, wx.ALIGN_CENTER, 10)
        # ----------------------------------------------------------------
        # Add text control to sizer
        # ----------------------------------------------------------------
        company_edit_logo_sizer.Add(self.company_edit_logo_text_ctrl, 0, wx.ALIGN_CENTER, 10)
        company_edit_logo_sizer.Add(self.company_edit_logo_path_btn, 0, wx.ALIGN_CENTER, 10)
        # ----------------------------------------------------------------
        # Add widgets to grid sizer
        # ----------------------------------------------------------------
        company_edit_grid_sizer.Add(self.company_edit_name_text_static, 1, flag=wx.EXPAND | wx.ALIGN_LEFT)
        company_edit_grid_sizer.Add(self.company_edit_name_text_ctrl, 1, flag=wx.EXPAND | wx.ALIGN_LEFT)

        company_edit_grid_sizer.Add(self.company_info_owner_text_static, 1, flag=wx.EXPAND | wx.ALIGN_LEFT)
        company_edit_grid_sizer.Add(self.company_edit_owner_text_ctrl, 1, flag=wx.EXPAND | wx.ALIGN_LEFT)

        company_edit_grid_sizer.Add(self.company_edit_vocation_text_static, 1, flag=wx.EXPAND | wx.ALIGN_LEFT)
        company_edit_grid_sizer.Add(self.company_edit_vocation_text_ctrl, 1, flag=wx.EXPAND | wx.ALIGN_LEFT)

        company_edit_grid_sizer.Add(self.company_edit_year_text_static, 1, flag=wx.EXPAND | wx.ALIGN_LEFT)
        company_edit_grid_sizer.Add(self.company_edit_year_text_ctrl, 1, flag=wx.EXPAND | wx.ALIGN_LEFT)

        company_edit_grid_sizer.Add(self.company_edit_address_text_static, 1, flag=wx.EXPAND | wx.ALIGN_LEFT)
        company_edit_grid_sizer.Add(self.company_edit_address_text_ctrl, 1, flag=wx.EXPAND | wx.ALIGN_LEFT)

        company_edit_grid_sizer.Add(self.company_edit_number_text_static, 1, flag=wx.EXPAND | wx.ALIGN_LEFT)
        company_edit_grid_sizer.Add(self.company_edit_number_text_ctrl, 1, flag=wx.EXPAND | wx.ALIGN_LEFT)

        company_edit_grid_sizer.Add(self.company_edit_logo_text_static, 1, flag=wx.EXPAND | wx.ALIGN_LEFT)
        company_edit_grid_sizer.Add(company_edit_logo_sizer, 1, flag=wx.EXPAND | wx.ALIGN_LEFT)
        # ----------------------------------------------------------------
        # Add grid sizer and button sizer to the inner sizer
        # ----------------------------------------------------------------
        company_edit_inner_sizer.AddSpacer(5)
        company_edit_inner_sizer.Add(company_edit_grid_sizer)
        company_edit_inner_sizer.AddSpacer(5)
        company_edit_inner_sizer.Add(company_edit_btn_sizer, 1, wx.ALIGN_CENTER)
        company_edit_inner_sizer.AddSpacer(5)
        # ----------------------------------------------------------------
        # Add the inner sizer to the main sizer
        # ----------------------------------------------------------------
        company_edit_wrapper_sizer.AddSpacer(10)
        company_edit_wrapper_sizer.Add(company_edit_inner_sizer)
        company_edit_wrapper_sizer.AddSpacer(10)

        # ----------------------------------------------------------------
        # Set the main sizer for the panel
        # ----------------------------------------------------------------
        self.SetSizer(company_edit_wrapper_sizer)
        company_edit_wrapper_sizer.Fit(self)

    def OnCancel(self, event):
        message_box = ShowMessageDlg(self,"Are you sure you with to do this without committing your changes ?",
                                     "Warning", wx.OK | wx.CANCEL | wx.ICON_QUESTION)
        if message_box == True:
            self.EndModal(True)

    def OnCommit(self, event, parent, company_name, company_owner, company_vocation, company_year_established,
                 company_address, company_contact_number, logo_file_path):

        parent.company_info_name_txt_display.SetLabel(company_name)
        parent.company_info_owner_txt_display.SetLabel(company_owner)
        parent.company_info_vocation_txt_display.SetLabel(company_vocation)
        parent.company_info_year_established_txt_display.SetLabel(company_year_established)
        parent.company_info_address_txt_display.SetLabel(company_address)
        parent.company_info_contact_number_txt_display.SetLabel(company_contact_number)
        parent.company_info_logo_file_path_text.SetLabel(logo_file_path)
        company_info_build_list = [ company_name, company_owner, company_vocation, company_year_established, company_address, company_contact_number, logo_file_path]

        #need update querry here

        #need to re-run the view function in the previous dialog to update the image !
        #update_logo =


        commit_to_file = Read_And_Write_Files.Build_File('test', company_info_build_list, 'comp_info.tuk')
        CompanyInfoDialog.OnView(parent)

        self.EndModal(True)

    def OnChoose(self, event, parent):
        wildcard = "Image files (*.jpg, *.png)|*.jpg"
        dialog = wx.FileDialog(None, "Choose a file",
                               wildcard=wildcard,
                               style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if dialog.ShowModal() == wx.ID_OK:
            self.company_edit_logo_text_ctrl.SetValue(dialog.GetPath())
        dialog.Destroy()
        #CompanyInfoDialog.OnView(parent)

# --------------------------------------------------------------------------------------------
# Tools drop down menu button
# --------------------------------------------------------------------------------------------

class DatabaseManagerDialog(wx.Dialog):
    def __init__(self, parent, title):
        super(DatabaseManagerDialog, self).__init__(parent, title=title, size=(600, 300))

        conn_read = Read_And_Write_Files.Read_File('data_conn.tuk')

        server = conn_read[0]
        database = conn_read[1]
        port = conn_read[2]
        driver = conn_read[3]

        data_base_manager_grid_sizer = wx.FlexGridSizer(4, 2, 10)
        data_base_wrapper_sizer = wx.BoxSizer(wx.VERTICAL)
        data_base_main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        data_base_btn_wrapper_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.info_static_text = wx.StaticText(self, label="Bellow is the connection information for your database")
        self.server_static_text = wx.StaticText(self, label="Server: ")
        self.database_static_text = wx.StaticText(self, label="Database: ")
        self.port_static_text = wx.StaticText(self, label="Port: ")
        self.driver_static_text = wx.StaticText(self, label="Driver: ")

        self.server_text_control = wx.TextCtrl(self, -1, server, size=(175, -1))
        self.database_text_ctrl = wx.TextCtrl(self, -1, database, size=(175, -1))
        self.port_text_control = wx.TextCtrl(self, -1, port, size=(175, -1))
        self.driver_text_ctrl = wx.TextCtrl(self, -1, driver, size=(175, -1))

        self.commit_btn = wx.Button(self, 0, label="Commit")
        self.commit_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnCommit(event,
                                                                        self.server_text_control.GetValue(),
                                                                        self.database_text_ctrl.GetValue(),
                                                                        self.port_text_control.GetValue(),
                                                                        self.driver_text_ctrl.GetValue()))
        self.test_connection_btn = wx.Button(self, 0, label="Test Connection")
        self.test_connection_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnTestConnection(event))
        self.cancel_btn = wx.Button(self, 0, label="Cancel")
        self.cancel_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnCancel(event))

        data_base_manager_grid_sizer.Add(self.server_static_text, 0, wx.ALIGN_LEFT, 10)
        data_base_manager_grid_sizer.Add(self.server_text_control, 0, wx.ALIGN_LEFT, 10)
        data_base_manager_grid_sizer.Add(self.database_static_text, 0, wx.ALIGN_LEFT, 10)
        data_base_manager_grid_sizer.Add(self.database_text_ctrl, 0, wx.ALIGN_LEFT, 10)
        data_base_manager_grid_sizer.Add(self.port_static_text, 0, wx.ALIGN_LEFT, 10)
        data_base_manager_grid_sizer.Add(self.port_text_control, 0, wx.ALIGN_LEFT, 10)
        data_base_manager_grid_sizer.Add(self.driver_static_text, 0, wx.ALIGN_LEFT, 10)
        data_base_manager_grid_sizer.Add(self.driver_text_ctrl, 0, wx.ALIGN_LEFT, 10)

        data_base_btn_wrapper_sizer.Add(self.commit_btn, 0, wx.ALIGN_RIGHT, 10)
        data_base_btn_wrapper_sizer.Add(self.test_connection_btn, 0, wx.ALIGN_CENTER, 10)
        data_base_btn_wrapper_sizer.Add(self.cancel_btn, 0, wx.ALIGN_LEFT, 10)

        data_base_wrapper_sizer.AddSpacer(10)
        data_base_wrapper_sizer.Add(self.info_static_text, 0, wx.ALIGN_LEFT, 10)
        data_base_wrapper_sizer.AddSpacer(5)
        data_base_wrapper_sizer.Add(data_base_manager_grid_sizer, 0, wx.ALIGN_LEFT | wx.ALL, 10)
        data_base_wrapper_sizer.AddSpacer(5)
        data_base_wrapper_sizer.Add(data_base_btn_wrapper_sizer, 0, wx.ALIGN_LEFT | wx.ALL, 10)
        data_base_wrapper_sizer.AddSpacer(10)

        data_base_main_sizer.AddSpacer(50)
        data_base_main_sizer.Add(data_base_wrapper_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        data_base_main_sizer.AddSpacer(50)

        self.SetSizer(data_base_main_sizer)
        data_base_main_sizer.Fit(self)

    def OnCommit(self,event, server, database, port, driver):
        database_manager_build_list = [server, database, port, driver]
        commit_to_file = Read_And_Write_Files.Build_File('N/A', database_manager_build_list, 'data_conn.tuk')
        self.EndModal(True)

    def OnTestConnection(self,event):
        self.EndModal(True)

    def OnCancel(self,event):
        self.EndModal(True)

class ReportBuilderDialog(wx.Dialog):
    def __init__(self, parent, title):
        super(ReportBuilderDialog, self).__init__(parent, title=title, size=(600, 300))

class LabelBuilderDialog(wx.Dialog):
    def __init__(self, parent, title):
        super(LabelBuilderDialog, self).__init__(parent, title=title, size=(600, 300))

# --------------------------------------------------------------------------------------------
# View drop down menu button
# --------------------------------------------------------------------------------------------

class UserLogsDialog(wx.Dialog):
    def __init__(self, parent, title):
        super(UserLogsDialog, self).__init__(parent, title=title, size=(600, 450))
        # ----------------------------------------------------------------
        self.user_logs_list_view = ObjectListView(self, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        # ----------------------------------------------------------------
        self.user_logs_ok_btn = wx.Button(self, 0, label="Ok")
        self.user_logs_ok_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnOk(event))
        self.user_logs_print_btn = wx.Button(self, 0, label="Print")
        self.user_logs_print_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnPrint(event))
        # ----------------------------------------------------------------
        user_logs_inner_sizer = wx.BoxSizer(wx.VERTICAL)
        user_logs_btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        user_logs_wrapper_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # ----------------------------------------------------------------
        user_logs_btn_sizer.Add(self.user_logs_ok_btn, 0, wx.ALIGN_CENTER, 10)
        user_logs_btn_sizer.Add(self.user_logs_print_btn, 0, wx.ALIGN_CENTER, 10)
        # ----------------------------------------------------------------
        user_logs_inner_sizer.AddSpacer(10)
        user_logs_inner_sizer.Add(self.user_logs_list_view, 1, wx.ALL | wx.EXPAND, 10)
        user_logs_inner_sizer.Add(user_logs_btn_sizer)
        user_logs_inner_sizer.AddSpacer(10)
        # ----------------------------------------------------------------
        user_logs_wrapper_sizer.AddSpacer(10)
        user_logs_wrapper_sizer.Add(user_logs_inner_sizer, 1,wx.ALL | wx.EXPAND)
        user_logs_wrapper_sizer.AddSpacer(10)
        # ----------------------------------------------------------------
        # --------------------------------------------------------------------------------------------
        Object_List_View_Builder.SetColumnsUserLog(self.user_logs_list_view)
        # --------------------------------------------------------------------------------------------
        self.SetSizer(user_logs_wrapper_sizer)

    def OnOk(self,event):
        self.EndModal(True)

    def OnPrint(self,event):
        ShowMessageDlg(self,"This function has not yet been implemented", "Print User Logs", wx.OK | wx.CANCEL | wx.ICON_QUESTION)
        self.EndModal(True)

# --------------------------------------------------------------------------------------------
# Help drop down menu button
# --------------------------------------------------------------------------------------------

class AboutDialog(wx.Dialog):
    def __init__(self, parent, title):
        super(AboutDialog, self).__init__(parent, title=title, size=(500, 500))

        self.about_ok_btn = wx.Button(self, 0, label="Ok")
        self.about_ok_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnOk(event))
        width = 490  # panel width
        self.about_text = wx.StaticText(self, label="This Dialog will explain about the program"
                                                    ""
                                                    "In fact, every generation fears the death of literacy at the "
                                                    "hands of some new media technology. And yet I am here to share "
                                                    "some optimism. After long existence as a confirmed cynic who "
                                                    "shared the general belief in our imminent cultural doom, "
                                                    "I felt an unfamiliar sensation 15 years ago when the Internet "
                                                    "came over the horizon: I found myself becoming excited and "
                                                    "hopeful."
                                                    ""
                                                    "In fact, every generation fears the death of literacy at the "
                                                    "hands of some new media technology. And yet I am here to share "
                                                    "some optimism. After long existence as a confirmed cynic who "
                                                    "shared the general belief in our imminent cultural doom, "
                                                    "I felt an unfamiliar sensation 15 years ago when the Internet "
                                                    "came over the horizon: I found myself becoming excited and "
                                                    "hopeful."
                                                    ""
                                                    "In fact, every generation fears the death of literacy at the "
                                                    "hands of some new media technology. And yet I am here to share "
                                                    "some optimism. After long existence as a confirmed cynic who "
                                                    "shared the general belief in our imminent cultural doom, "
                                                    "I felt an unfamiliar sensation 15 years ago when the Internet "
                                                    "came over the horizon: I found myself becoming excited and "
                                                    "hopeful."
                                                    ""
                                                    "In fact, every generation fears the death of literacy at the "
                                                    "hands of some new media technology. And yet I am here to share "
                                                    "some optimism. After long existence as a confirmed cynic who "
                                                    "shared the general belief in our imminent cultural doom, "
                                                    "I felt an unfamiliar sensation 15 years ago when the Internet "
                                                    "came over the horizon: I found myself becoming excited and "
                                                    "hopeful.")
        # ----------------------------------------------------------------
        self.about_text.Wrap(width)
        # ----------------------------------------------------------------
        about_inner_sizer = wx.BoxSizer(wx.VERTICAL)
        about_wrapper_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # ----------------------------------------------------------------
        about_inner_sizer.AddSpacer((10))
        about_inner_sizer.Add(self.about_text, 0, wx.ALIGN_CENTER, 10)
        about_inner_sizer.Add(self.about_ok_btn, 0, wx.ALIGN_CENTER, 10)
        about_inner_sizer.AddSpacer((10))
        # ----------------------------------------------------------------
        about_wrapper_sizer.AddSpacer((10))
        about_wrapper_sizer.Add(about_inner_sizer)
        about_wrapper_sizer.AddSpacer(10)
        # ----------------------------------------------------------------
        self.SetSizer(about_wrapper_sizer)
        about_wrapper_sizer.Fit(self)
        # ----------------------------------------------------------------
    def OnOk(self,event):
        self.EndModal(True)

class LicenceDialog(wx.Dialog):
    def __init__(self, parent, title):
        super(LicenceDialog, self).__init__(parent, title=title, size=(500, 500))

        self.licence_ok_btn = wx.Button(self, 0, label="Ok")
        self.licence_ok_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnOk(event))
        width = 490  # panel width
        self.licence_text = wx.StaticText(self, label="This Dialog will explain about the program"
                                                    ""
                                                    "In fact, every generation fears the death of literacy at the "
                                                    "hands of some new media technology. And yet I am here to share "
                                                    "some optimism. After long existence as a confirmed cynic who "
                                                    "shared the general belief in our imminent cultural doom, "
                                                    "I felt an unfamiliar sensation 15 years ago when the Internet "
                                                    "came over the horizon: I found myself becoming excited and "
                                                    "hopeful."
                                                    ""
                                                    "In fact, every generation fears the death of literacy at the "
                                                    "hands of some new media technology. And yet I am here to share "
                                                    "some optimism. After long existence as a confirmed cynic who "
                                                    "shared the general belief in our imminent cultural doom, "
                                                    "I felt an unfamiliar sensation 15 years ago when the Internet "
                                                    "came over the horizon: I found myself becoming excited and "
                                                    "hopeful."
                                                    ""
                                                    "In fact, every generation fears the death of literacy at the "
                                                    "hands of some new media technology. And yet I am here to share "
                                                    "some optimism. After long existence as a confirmed cynic who "
                                                    "shared the general belief in our imminent cultural doom, "
                                                    "I felt an unfamiliar sensation 15 years ago when the Internet "
                                                    "came over the horizon: I found myself becoming excited and "
                                                    "hopeful."
                                                    ""
                                                    "In fact, every generation fears the death of literacy at the "
                                                    "hands of some new media technology. And yet I am here to share "
                                                    "some optimism. After long existence as a confirmed cynic who "
                                                    "shared the general belief in our imminent cultural doom, "
                                                    "I felt an unfamiliar sensation 15 years ago when the Internet "
                                                    "came over the horizon: I found myself becoming excited and "
                                                    "hopeful.")
        # ----------------------------------------------------------------
        self.licence_text.Wrap(width)
        # ----------------------------------------------------------------
        licence_inner_sizer = wx.BoxSizer(wx.VERTICAL)
        licence_wrapper_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # ----------------------------------------------------------------
        licence_inner_sizer.AddSpacer((10, 10))
        licence_inner_sizer.Add(self.licence_text, 0, wx.ALIGN_CENTER, 10)
        licence_inner_sizer.Add(self.licence_ok_btn, 0, wx.ALIGN_CENTER, 10)
        licence_inner_sizer.AddSpacer((10, 10))
        # ----------------------------------------------------------------
        licence_wrapper_sizer.AddSpacer((10,10))
        licence_wrapper_sizer.Add(licence_inner_sizer)
        licence_wrapper_sizer.AddSpacer(10,10)
        # ----------------------------------------------------------------
        self.SetSizer(licence_wrapper_sizer)
        licence_wrapper_sizer.Fit(self)
        # ----------------------------------------------------------------
    def OnOk(self, event):
        self.EndModal(True)

class ContactDialog(wx.Dialog):
    def __init__(self, parent, title):
        super(ContactDialog, self).__init__(parent, title=title, size=(500, 500))

        self.contact_ok_btn = wx.Button(self, 0, label="Ok")
        self.contact_ok_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnOk(event))
        width = 490  # panel width
        self.contact_text = wx.StaticText(self, label="This Dialog will explain about the program"
                                                      ""
                                                      "In fact, every generation fears the death of literacy at the "
                                                      "hands of some new media technology. And yet I am here to share "
                                                      "some optimism. After long existence as a confirmed cynic who "
                                                      "shared the general belief in our imminent cultural doom, "
                                                      "I felt an unfamiliar sensation 15 years ago when the Internet "
                                                      "came over the horizon: I found myself becoming excited and "
                                                      "hopeful."
                                                      ""
                                                      "In fact, every generation fears the death of literacy at the "
                                                      "hands of some new media technology. And yet I am here to share "
                                                      "some optimism. After long existence as a confirmed cynic who "
                                                      "shared the general belief in our imminent cultural doom, "
                                                      "I felt an unfamiliar sensation 15 years ago when the Internet "
                                                      "came over the horizon: I found myself becoming excited and "
                                                      "hopeful."
                                                      ""
                                                      "In fact, every generation fears the death of literacy at the "
                                                      "hands of some new media technology. And yet I am here to share "
                                                      "some optimism. After long existence as a confirmed cynic who "
                                                      "shared the general belief in our imminent cultural doom, "
                                                      "I felt an unfamiliar sensation 15 years ago when the Internet "
                                                      "came over the horizon: I found myself becoming excited and "
                                                      "hopeful."
                                                      ""
                                                      "In fact, every generation fears the death of literacy at the "
                                                      "hands of some new media technology. And yet I am here to share "
                                                      "some optimism. After long existence as a confirmed cynic who "
                                                      "shared the general belief in our imminent cultural doom, "
                                                      "I felt an unfamiliar sensation 15 years ago when the Internet "
                                                      "came over the horizon: I found myself becoming excited and "
                                                      "hopeful.")
        # ----------------------------------------------------------------
        self.contact_text.Wrap(width)
        # ----------------------------------------------------------------
        contact_inner_sizer = wx.BoxSizer(wx.VERTICAL)
        contact_wrapper_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # ----------------------------------------------------------------
        contact_inner_sizer.AddSpacer((10, 10))
        contact_inner_sizer.Add(self.contact_text, 0, wx.ALIGN_CENTER, 10)
        contact_inner_sizer.Add(self.contact_ok_btn, 0, wx.ALIGN_CENTER, 10)
        contact_inner_sizer.AddSpacer((10, 10))
        # ----------------------------------------------------------------
        contact_wrapper_sizer.AddSpacer((10, 10))
        contact_wrapper_sizer.Add(contact_inner_sizer)
        contact_wrapper_sizer.AddSpacer(10, 10)
        # ----------------------------------------------------------------
        self.SetSizer(contact_wrapper_sizer)
        contact_wrapper_sizer.Fit(self)
        # ----------------------------------------------------------------
    def OnOk(self, event):
        self.EndModal(True)

################################################################################################################
################################################################################################################
# Modal main panel area!
################################################################################################################
################################################################################################################

# --------------------------------------------------------------------------------------------
# Customer Tab Modals
# --------------------------------------------------------------------------------------------

class AddCustomerDialog(wx.Dialog):
    def __init__(self, parent, title):
        super(AddCustomerDialog, self).__init__(parent, title=title, size=(600, 300))

        grid_sizer = wx.FlexGridSizer(5, 5, 10)
        wrapper_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_wrapper_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # ------------------------------------------------------------------------------
        # Create Widgets
        # ------------------------------------------------------------------------------
        conn_read = Read_And_Write_Files.Read_File('data_conn.tuk')
        server_in = conn_read[0]
        database_in = conn_read[1]
        port_in = conn_read[2]
        driver_in = conn_read[3]

        # Read current user info
        user_read = Read_And_Write_Files.Read_File('user.tuk')
        username = user_read[0]
        password = user_read[1]


        try:
            # Open connection
            open_con = SQL.SQLCon(server_in, database_in, username, password, driver_in, port_in)
            project_list_return = SQL.SQLSearchAllSingleColumn(open_con, username, "Projects", "name")
        except:
            pass

        output_list = Data_Transforms.TransformRowToList(project_list_return)


        self.info_static_text = wx.StaticText(self, label="To add a customer to the database please fill out all of the "
                                                          "following information: ")

        self.name_static_text = wx.StaticText(self, label="Name: ")
        self.name_txt_ctrl = wx.TextCtrl(self, -1, "", size=(200, -1))

        self.status_static_text = wx.StaticText(self, label="Status: ")
        self.status_txt_ctrl = wx.TextCtrl(self, -1, "", size=(200, -1))

        self.balance_static_text = wx.StaticText(self, label="Balance: ")
        self.balance_txt_ctrl = wx.TextCtrl(self, -1, "", size=(200, -1))

        self.contact_static_text = wx.StaticText(self, label="Contact: ")
        self.contact_code_txt_ctrl = wx.TextCtrl(self, -1, "", size=(200, -1))

        self.email_static_text = wx.StaticText(self, label="Email: ")
        self.email_txt_ctrl = wx.TextCtrl(self, -1, "", size=(200, -1))

        self.telephone_static_text = wx.StaticText(self, label="Telephone: ")
        self.telephone_txt_ctrl = wx.TextCtrl(self, -1, "", size=(200, -1))

        self.mobile_static_text = wx.StaticText(self, label="Mobile: ")
        self.mobile_txt_ctrl = wx.TextCtrl(self, -1, "", size=(200, -1))

        self.project_static_text = wx.StaticText(self, label="Project select: ")
        self.project_drop_down = wx.ComboBox(self, size=wx.DefaultSize, choices=output_list)

        self.project_create_btn = wx.Button(self, 0, label="Create project")
        self.project_create_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnCreateProject(event, self))

        self.commit_btn = wx.Button(self, 0, label="Commit")
        self.commit_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnCommit(event, parent))
        self.cancel_btn = wx.Button(self, 0, label="Cancel")
        self.cancel_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnCancel(event))

        grid_sizer.Add(self.name_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.name_txt_ctrl, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.AddSpacer(5)
        grid_sizer.Add(self.status_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.status_txt_ctrl, 0, wx.ALIGN_LEFT, 10)

        grid_sizer.Add(self.balance_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.balance_txt_ctrl, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.AddSpacer(5)
        grid_sizer.Add(self.contact_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.contact_code_txt_ctrl, 0, wx.ALIGN_LEFT, 10)

        grid_sizer.Add(self.email_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.email_txt_ctrl, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.AddSpacer(5)
        grid_sizer.Add(self.telephone_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.telephone_txt_ctrl, 0, wx.ALIGN_LEFT, 10)


        grid_sizer.Add(self.mobile_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.mobile_txt_ctrl, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.AddSpacer(5)
        grid_sizer.AddSpacer(5)
        grid_sizer.AddSpacer(5)

        grid_sizer.Add(self.project_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.project_drop_down, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.AddSpacer(5)

        grid_sizer.Add(self.project_create_btn, 0, wx.ALIGN_LEFT, 10)


        btn_wrapper_sizer.Add(self.commit_btn, 0, wx.ALIGN_RIGHT, 10)
        btn_wrapper_sizer.Add(self.cancel_btn, 0, wx.ALIGN_LEFT, 10)

        wrapper_sizer.AddSpacer(10)
        wrapper_sizer.Add(self.info_static_text, 0, wx.ALIGN_LEFT, 10)
        wrapper_sizer.AddSpacer(5)
        wrapper_sizer.Add(grid_sizer, 0, wx.ALIGN_LEFT | wx.ALL, 10)
        wrapper_sizer.AddSpacer(5)
        wrapper_sizer.Add(btn_wrapper_sizer, 0, wx.ALIGN_LEFT | wx.ALL, 10)
        wrapper_sizer.AddSpacer(10)

        main_sizer.AddSpacer(20)
        main_sizer.Add(wrapper_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        main_sizer.AddSpacer(20)

        self.SetSizer(main_sizer)
        main_sizer.Fit(self)

    def OnCommit(self,event, parent):


        conn_read = Read_And_Write_Files.Read_File('data_conn.tuk')
        server_in = conn_read[0]
        database_in = conn_read[1]
        port_in = conn_read[2]
        driver_in = conn_read[3]

        # Read current user info
        user_read = Read_And_Write_Files.Read_File('user.tuk')
        username = user_read[0]
        password = user_read[1]

        try:
            open_con = SQL.SQLCon(server_in, database_in, username, password, driver_in, port_in)
            ID = SQL.SQLGenerateNewID(open_con, "Customers")
            insert_list = [ID,
                           self.name_txt_ctrl.GetValue(),
                           self.status_txt_ctrl.GetValue(),
                           self.balance_txt_ctrl.GetValue(),
                           self.contact_code_txt_ctrl.GetValue(),
                           self.email_txt_ctrl.GetValue(),
                           self.telephone_txt_ctrl.GetValue(),
                           self.mobile_txt_ctrl.GetValue(),
                           self.project_drop_down.GetValue()]

            #need to check insert list against names in the database
            insert_list = Data_Transforms.InsertListFillNull(insert_list)
            SQL.SQLInsertInto(open_con, username, "Customers", insert_list)
            GUI.CustomersTab.OnSearch(parent, event)
            self.EndModal(True)
        except:
            # Error message
            ShowMessageDlg(self, "Failed to access the data base, please check with your system admin.", "Error"
                           , wx.OK | wx.CANCEL | wx.ICON_QUESTION)

    def OnCancel(self,event):
        self.EndModal(True)

    def OnCreateProject(self, event, parent):
        AddProjectDialog(self, 'Add A New Project To The Database!' , self.name_txt_ctrl.GetValue(), 1).ShowModal()

        conn_read = Read_And_Write_Files.Read_File('data_conn.tuk')
        server_in = conn_read[0]
        database_in = conn_read[1]
        port_in = conn_read[2]
        driver_in = conn_read[3]

        # Read current user info
        user_read = Read_And_Write_Files.Read_File('user.tuk')
        username = user_read[0]
        password = user_read[1]

        try:
            # Open connection
            open_con = SQL.SQLCon(server_in, database_in, username, password, driver_in, port_in)
            project_list_return = SQL.SQLSearchAllSingleColumn(open_con, username, "Projects", "name")

        except:
            pass

        self.output_list = Data_Transforms.TransformRowToList(project_list_return)
        self.Update()
        self.Refresh()

class EditCustomerDialog(wx.Dialog):
    def __init__(self, parent, title, id_to_edit):
        super(EditCustomerDialog, self).__init__(parent, title=title, size=(600, 300))

        conn_read = Read_And_Write_Files.Read_File('data_conn.tuk')

        server_in = conn_read[0]
        database_in = conn_read[1]
        port_in = conn_read[2]
        driver_in = conn_read[3]

        # Read current user info
        user_read = Read_And_Write_Files.Read_File('user.tuk')
        username = user_read[0]
        password = user_read[1]

        open_con = SQL.SQLCon(server_in, database_in, username, password, driver_in, port_in)
        row_info_return = SQL.SQLSearchMultipleRow(open_con, "Customers", "ID", id_to_edit)
        row_info_return = Data_Transforms.SplitAndCleanDBReturn(row_info_return)

        grid_sizer = wx.FlexGridSizer(5, 5, 10)
        wrapper_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_wrapper_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # ------------------------------------------------------------------------------
        # Create Widgets
        # ------------------------------------------------------------------------------

        grid_sizer = wx.FlexGridSizer(5, 5, 10)
        wrapper_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_wrapper_sizer = wx.BoxSizer(wx.HORIZONTAL)

        try:
            # Open connection
            open_con = SQL.SQLCon(server_in, database_in, username, password, driver_in, port_in)
            project_list_return = SQL.SQLSearchAllSingleColumn(open_con, username, "Projects", "name")
        except:
            pass

        output_list = Data_Transforms.TransformRowToList(project_list_return)


        self.info_static_text = wx.StaticText(self, label="To add a customer to the database please fill out all of the "
                                                          "following information: ")

        self.name_static_text = wx.StaticText(self, label="Name: ")
        self.name_txt_ctrl = wx.TextCtrl(self, -1, row_info_return[1], size=(200, -1))

        self.status_static_text = wx.StaticText(self, label="Status: ")
        self.status_txt_ctrl = wx.TextCtrl(self, -1, row_info_return[2], size=(200, -1))

        self.balance_static_text = wx.StaticText(self, label="Balance: ")
        self.balance_txt_ctrl = wx.TextCtrl(self, -1, row_info_return[3], size=(200, -1))

        self.contact_static_text = wx.StaticText(self, label="Contact: ")
        self.contact_code_txt_ctrl = wx.TextCtrl(self, -1, row_info_return[4], size=(200, -1))

        self.email_static_text = wx.StaticText(self, label="Email: ")
        self.email_txt_ctrl = wx.TextCtrl(self, -1, row_info_return[5], size=(200, -1))

        self.telephone_static_text = wx.StaticText(self, label="Telephone: ")
        self.telephone_txt_ctrl = wx.TextCtrl(self, -1, row_info_return[6], size=(200, -1))

        self.mobile_static_text = wx.StaticText(self, label="Mobile: ")
        self.mobile_txt_ctrl = wx.TextCtrl(self, -1, row_info_return[7], size=(200, -1))

        self.project_static_text = wx.StaticText(self, label="Project select: ")
        self.project_drop_down = wx.ComboBox(self, size=wx.DefaultSize, choices=output_list)
        self.project_drop_down.SetValue(row_info_return[8])
        self.project_create_btn = wx.Button(self, 0, label="Create project")
        self.project_create_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnCreateProject(event, self))

        self.commit_btn = wx.Button(self, 0, label="Commit")
        self.commit_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnCommit(event, id_to_edit, parent))
        self.cancel_btn = wx.Button(self, 0, label="Cancel")
        self.cancel_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnCancel(event))

        grid_sizer.Add(self.name_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.name_txt_ctrl, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.AddSpacer(5)
        grid_sizer.Add(self.status_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.status_txt_ctrl, 0, wx.ALIGN_LEFT, 10)

        grid_sizer.Add(self.balance_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.balance_txt_ctrl, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.AddSpacer(5)
        grid_sizer.Add(self.contact_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.contact_code_txt_ctrl, 0, wx.ALIGN_LEFT, 10)

        grid_sizer.Add(self.email_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.email_txt_ctrl, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.AddSpacer(5)
        grid_sizer.Add(self.telephone_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.telephone_txt_ctrl, 0, wx.ALIGN_LEFT, 10)


        grid_sizer.Add(self.mobile_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.mobile_txt_ctrl, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.AddSpacer(5)
        grid_sizer.AddSpacer(5)
        grid_sizer.AddSpacer(5)

        grid_sizer.Add(self.project_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.project_drop_down, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.AddSpacer(5)

        grid_sizer.Add(self.project_create_btn, 0, wx.ALIGN_LEFT, 10)


        btn_wrapper_sizer.Add(self.commit_btn, 0, wx.ALIGN_RIGHT, 10)
        btn_wrapper_sizer.Add(self.cancel_btn, 0, wx.ALIGN_LEFT, 10)

        wrapper_sizer.AddSpacer(10)
        wrapper_sizer.Add(self.info_static_text, 0, wx.ALIGN_LEFT, 10)
        wrapper_sizer.AddSpacer(5)
        wrapper_sizer.Add(grid_sizer, 0, wx.ALIGN_LEFT | wx.ALL, 10)
        wrapper_sizer.AddSpacer(5)
        wrapper_sizer.Add(btn_wrapper_sizer, 0, wx.ALIGN_LEFT | wx.ALL, 10)
        wrapper_sizer.AddSpacer(10)

        main_sizer.AddSpacer(20)
        main_sizer.Add(wrapper_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        main_sizer.AddSpacer(20)

        self.SetSizer(main_sizer)
        main_sizer.Fit(self)

    def OnCancel(self, event):
        self.EndModal(True)

    def OnCommit(self,event, id_to_edit, parent):

        entry_list = [id_to_edit,
                      self.name_txt_ctrl.GetValue(),
                      self.status_txt_ctrl.GetValue(),
                      self.balance_txt_ctrl.GetValue(),
                      self.contact_code_txt_ctrl.GetValue(),
                      self.email_txt_ctrl.GetValue(),
                      self.telephone_txt_ctrl.GetValue(),
                      self.mobile_txt_ctrl.GetValue(),
                      self.project_drop_down.GetValue()]

        conn_read = Read_And_Write_Files.Read_File('data_conn.tuk')
        server_in = conn_read[0]
        database_in = conn_read[1]
        port_in = conn_read[2]
        driver_in = conn_read[3]

        # Read current user info
        user_read = Read_And_Write_Files.Read_File('user.tuk')
        username = user_read[0]
        password = user_read[1]

        open_con = SQL.SQLCon(server_in, database_in, username, password, driver_in, port_in)
        column_list = SQL.SQLGetColumnNames(open_con, "Customers")

        SQL.SQLUpdateEntry(open_con, "Customers", id_to_edit, column_list, entry_list)
        GUI.CustomersTab.OnSearch(parent, event)

        self.EndModal(True)

# --------------------------------------------------------------------------------------------
# Project Tab Modals
# --------------------------------------------------------------------------------------------
#self.output_list = Data_Transforms.TransformRowToList(project_list_return)
            #parent.output_list = Data_Transforms.TransformRowToList(project_list_return)

# --------------------------------------------------------------------------------------------
# Project Tab Modals
# --------------------------------------------------------------------------------------------

class AddProjectDialog(wx.Dialog):
    def __init__(self, parent, title, customer_pass, load_point):
        super(AddProjectDialog, self).__init__(parent, title=title, size=(600, 300))
        grid_sizer = wx.FlexGridSizer(5, 5, 10)
        wrapper_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_wrapper_sizer = wx.BoxSizer(wx.HORIZONTAL)


        conn_read = Read_And_Write_Files.Read_File('data_conn.tuk')
        server_in = conn_read[0]
        database_in = conn_read[1]
        port_in = conn_read[2]
        driver_in = conn_read[3]

        # Read current user info
        user_read = Read_And_Write_Files.Read_File('user.tuk')
        username = user_read[0]
        password = user_read[1]


        try:
            # Open connection
            open_con = SQL.SQLCon(server_in, database_in, username, password, driver_in, port_in)
            customer_list_return = SQL.SQLSearchAllSingleColumn(open_con, username, "Customers", "name")

        except:
            pass

        output_list = Data_Transforms.TransformRowToList(customer_list_return)
        output_list.append(customer_pass)

        # ------------------------------------------------------------------------------
        # Create Widgets
        # ------------------------------------------------------------------------------
        self.info_static_text = wx.StaticText(self, label="To add a customer to the database please fill out all of the "
                                                          "following information: ")

        self.project_code_static_text = wx.StaticText(self, label="Project Code: ")
        self.project_code_txt_ctrl = wx.TextCtrl(self, -1, "", size=(200, -1))

        self.name_static_text = wx.StaticText(self, label="Name: ")
        self.name_txt_ctrl = wx.TextCtrl(self, -1, "", size=(200, -1))

        self.status_static_text = wx.StaticText(self, label="Status: ")
        self.status_txt_ctrl = wx.TextCtrl(self, -1, "", size=(200, -1))

        self.customer_static_text = wx.StaticText(self, label="Customer: ")
        self.customer_drop_down = wx.ComboBox(self, size=wx.DefaultSize, choices=output_list)

        self.commit_btn = wx.Button(self, 0, label="Commit")
        self.commit_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnCommit(event,parent, load_point))
        self.cancel_btn = wx.Button(self, 0, label="Cancel")
        self.cancel_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnCancel(event))

        grid_sizer.Add(self.project_code_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.project_code_txt_ctrl, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.AddSpacer(5)
        grid_sizer.Add(self.name_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.name_txt_ctrl, 0, wx.ALIGN_LEFT, 10)

        grid_sizer.Add(self.status_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.status_txt_ctrl, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.AddSpacer(5)
        grid_sizer.Add(self.customer_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.customer_drop_down, 0, wx.ALIGN_LEFT, 10)


        grid_sizer.AddSpacer(5)

        btn_wrapper_sizer.Add(self.commit_btn, 0, wx.ALIGN_RIGHT, 10)
        btn_wrapper_sizer.Add(self.cancel_btn, 0, wx.ALIGN_LEFT, 10)

        wrapper_sizer.AddSpacer(10)
        wrapper_sizer.Add(self.info_static_text, 0, wx.ALIGN_LEFT, 10)
        wrapper_sizer.AddSpacer(5)
        wrapper_sizer.Add(grid_sizer, 0, wx.ALIGN_LEFT | wx.ALL, 10)
        wrapper_sizer.AddSpacer(5)
        wrapper_sizer.Add(btn_wrapper_sizer, 0, wx.ALIGN_LEFT | wx.ALL, 10)
        wrapper_sizer.AddSpacer(10)

        main_sizer.AddSpacer(20)
        main_sizer.Add(wrapper_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        main_sizer.AddSpacer(20)

        self.SetSizer(main_sizer)
        main_sizer.Fit(self)

    def OnCommit(self,event, parent, load_point):


        conn_read = Read_And_Write_Files.Read_File('data_conn.tuk')
        server_in = conn_read[0]
        database_in = conn_read[1]
        port_in = conn_read[2]
        driver_in = conn_read[3]

        # Read current user info
        user_read = Read_And_Write_Files.Read_File('user.tuk')
        username = user_read[0]
        password = user_read[1]

        try:
            open_con = SQL.SQLCon(server_in, database_in, username, password, driver_in, port_in)
            ID = SQL.SQLGenerateNewID(open_con, "Projects")
            insert_list = [ID,
                           self.project_code_txt_ctrl.GetValue(),
                           self.name_txt_ctrl.GetValue(),
                           self.status_txt_ctrl.GetValue(),
                           self.customer_drop_down.GetValue()]

            #need to check insert list against names in the database
            insert_list = Data_Transforms.InsertListFillNull(insert_list)
            SQL.SQLInsertInto(open_con, username, "Projects", insert_list)
            self.EndModal(True)

        except:
            # Error message
            ShowMessageDlg(self, "Failed to access the data base, please check with your system admin.", "Error"
                           , wx.OK | wx.CANCEL | wx.ICON_QUESTION)
        open_con = SQL.SQLConAutoCommit(server_in, database_in, username, password, driver_in, port_in)
        run = SQL.SQLCreateProjectDatabase(open_con,self.project_code_txt_ctrl.GetValue(), username, password)
        open_con.close()
        GUI.ProjectsTab.OnSearch(parent, event)

    def OnCancel(self,event):
        self.EndModal(True)

class EditProjectDialog(wx.Dialog):
    def __init__(self, parent, title, id_to_edit):
        super(EditProjectDialog, self).__init__(parent, title=title, size=(600, 300))

        conn_read = Read_And_Write_Files.Read_File('data_conn.tuk')
        server_in = conn_read[0]
        database_in = conn_read[1]
        port_in = conn_read[2]
        driver_in = conn_read[3]

        # Read current user info
        user_read = Read_And_Write_Files.Read_File('user.tuk')
        username = user_read[0]
        password = user_read[1]

        open_con = SQL.SQLCon(server_in, database_in, username, password, driver_in, port_in)
        row_info_return = SQL.SQLSearchMultipleRow(open_con, "Projects", "ID", id_to_edit)
        row_info_return = Data_Transforms.SplitAndCleanDBReturn(row_info_return)

        try:
            # Open connection
            open_con = SQL.SQLCon(server_in, database_in, username, password, driver_in, port_in)
            customer_list_return = SQL.SQLSearchAllSingleColumn(open_con, username, "Customers", "name")

        except:
            pass

        output_list = Data_Transforms.TransformRowToList(customer_list_return)

        # ------------------------------------------------------------------------------
        # Create Widgets
        # ------------------------------------------------------------------------------

        grid_sizer = wx.FlexGridSizer(5, 5, 10)
        wrapper_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_wrapper_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.info_static_text = wx.StaticText(self, label="To edit a customer to the database please amend the field "
                                                          "you wish to change")

        self.project_code_static_text = wx.StaticText(self, label="Project Code: ")
        self.project_code_txt_ctrl = wx.TextCtrl(self, -1, row_info_return[1], size=(200, -1))

        self.name_static_text = wx.StaticText(self, label="Name: ")
        self.name_txt_ctrl = wx.TextCtrl(self, -1, row_info_return[2], size=(200, -1))

        self.status_static_text = wx.StaticText(self, label="Status: ")
        self.status_txt_ctrl = wx.TextCtrl(self, -1, row_info_return[3], size=(200, -1))

        self.customer_static_text = wx.StaticText(self, label="Customer: ")
        self.customer_drop_down = wx.ComboBox(self, size=wx.DefaultSize, choices=output_list)
        self.customer_drop_down.SetValue(row_info_return[4])


        self.commit_btn = wx.Button(self, 0, label="Commit")
        self.commit_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnCommit(event, id_to_edit, parent))
        self.cancel_btn = wx.Button(self, 0, label="Cancel")
        self.cancel_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnCancel(event))

        grid_sizer.Add(self.project_code_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.project_code_txt_ctrl, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.AddSpacer(5)
        grid_sizer.Add(self.name_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.name_txt_ctrl, 0, wx.ALIGN_LEFT, 10)

        grid_sizer.Add(self.status_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.status_txt_ctrl, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.AddSpacer(5)
        grid_sizer.Add(self.customer_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.customer_drop_down, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.AddSpacer(5)

        btn_wrapper_sizer.Add(self.commit_btn, 0, wx.ALIGN_RIGHT, 10)
        btn_wrapper_sizer.Add(self.cancel_btn, 0, wx.ALIGN_LEFT, 10)

        wrapper_sizer.AddSpacer(10)
        wrapper_sizer.Add(self.info_static_text, 0, wx.ALIGN_LEFT, 10)
        wrapper_sizer.AddSpacer(5)
        wrapper_sizer.Add(grid_sizer, 0, wx.ALIGN_LEFT | wx.ALL, 10)
        wrapper_sizer.AddSpacer(5)
        wrapper_sizer.Add(btn_wrapper_sizer, 0, wx.ALIGN_LEFT | wx.ALL, 10)
        wrapper_sizer.AddSpacer(10)

        main_sizer.AddSpacer(20)
        main_sizer.Add(wrapper_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        main_sizer.AddSpacer(20)

        self.SetSizer(main_sizer)
        main_sizer.Fit(self)

    def OnCancel(self, event):
        self.EndModal(True)

    def OnCommit(self,event, id_to_edit, parent):

        entry_list = [id_to_edit,
                      self.project_code_txt_ctrl.GetValue(),
                      self.name_txt_ctrl.GetValue(),
                      self.status_txt_ctrl.GetValue(),
                      self.customer_drop_down.GetValue()]

        conn_read = Read_And_Write_Files.Read_File('data_conn.tuk')
        server_in = conn_read[0]
        database_in = conn_read[1]
        port_in = conn_read[2]
        driver_in = conn_read[3]

        # Read current user info
        user_read = Read_And_Write_Files.Read_File('user.tuk')
        username = user_read[0]
        password = user_read[1]

        open_con = SQL.SQLCon(server_in, database_in, username, password, driver_in, port_in)
        column_list = SQL.SQLGetColumnNames(open_con, "Projects")

        SQL.SQLUpdateEntry(open_con, "Projects", id_to_edit, column_list, entry_list)
        GUI.ProjectsTab.OnSearch(parent, event)

        self.EndModal(True)

# --------------------------------------------------------------------------------------------
# Product Tab Modals
# --------------------------------------------------------------------------------------------

class AddProductDialog(wx.Dialog):
    def __init__(self, parent, title):
        super(AddProductDialog, self).__init__(parent, title=title, size=(600, 300))

        grid_sizer = wx.FlexGridSizer(5, 5, 10)
        wrapper_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_wrapper_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # ------------------------------------------------------------------------------
        # Create Widgets
        # ------------------------------------------------------------------------------

        self.info_static_text = wx.StaticText(self, label="To add a product to the database please fill out all of the "
                                                          "following information: ")

        self.model_static_text = wx.StaticText(self, label="Model: ")
        self.model_txt_ctrl = wx.TextCtrl(self, -1, "", size=(200, -1))

        self.brand_static_text = wx.StaticText(self, label="Brand: ")
        self.brand_txt_ctrl = wx.TextCtrl(self, -1, "", size=(200, -1))

        self.supplier_static_text = wx.StaticText(self, label="Supplier: ")
        self.supplier_txt_ctrl = wx.TextCtrl(self, -1, "", size=(200, -1))

        self.company_code_static_text = wx.StaticText(self, label="Company Code: ")
        self.company_code_txt_ctrl = wx.TextCtrl(self, -1, "", size=(200, -1))

        self.description_static_text = wx.StaticText(self, label="Description: ")
        self.description_txt_ctrl = wx.TextCtrl(self, -1, "", size=(200, -1))

        self.color_static_text = wx.StaticText(self, label="Color: ")
        self.color_txt_ctrl = wx.TextCtrl(self, -1, "", size=(200, -1))

        self.unit_of_measure_static_text = wx.StaticText(self, label="Unit Of Measure: ")
        self.unit_of_measure_txt_ctrl = wx.TextCtrl(self, -1, "", size=(200, -1))

        self.price_ex_vat_static_text = wx.StaticText(self, label="Price Ex VAT: ")
        self.price_ex_vat_txt_ctrl = wx.TextCtrl(self, -1, "", size=(200, -1))

        self.total_qty_static_text = wx.StaticText(self, label="Total Qty: ")
        self.total_qty_txt_ctrl = wx.TextCtrl(self, -1, "", size=(200, -1))

        self.project_qty_static_text = wx.StaticText(self, label="Project Qty: ")
        self.project_qty_txt_ctrl = wx.TextCtrl(self, -1, "", size=(200, -1))

        self.free_stock_qty_static_text = wx.StaticText(self, label="Free Stock Qty: ")
        self.free_stock_qty_txt_ctrl = wx.TextCtrl(self, -1, "", size=(200, -1))

        self.commit_btn = wx.Button(self, 0, label="Commit")
        self.commit_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnCommit(event, parent))
        self.cancel_btn = wx.Button(self, 0, label="Cancel")
        self.cancel_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnCancel(event))

        grid_sizer.Add(self.model_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.model_txt_ctrl, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.AddSpacer(5)
        grid_sizer.Add(self.brand_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.brand_txt_ctrl, 0, wx.ALIGN_LEFT, 10)

        grid_sizer.Add(self.supplier_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.supplier_txt_ctrl, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.AddSpacer(5)
        grid_sizer.Add(self.company_code_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.company_code_txt_ctrl, 0, wx.ALIGN_LEFT, 10)

        grid_sizer.Add(self.description_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.description_txt_ctrl, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.AddSpacer(5)
        grid_sizer.Add(self.color_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.color_txt_ctrl, 0, wx.ALIGN_LEFT, 10)


        grid_sizer.Add(self.unit_of_measure_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.unit_of_measure_txt_ctrl, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.AddSpacer(5)
        grid_sizer.Add(self.price_ex_vat_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.price_ex_vat_txt_ctrl, 0, wx.ALIGN_LEFT, 10)

        grid_sizer.Add(self.total_qty_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.total_qty_txt_ctrl, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.AddSpacer(5)
        grid_sizer.Add(self.project_qty_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.project_qty_txt_ctrl, 0, wx.ALIGN_LEFT, 10)

        grid_sizer.Add(self.free_stock_qty_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.free_stock_qty_txt_ctrl, 0, wx.ALIGN_LEFT, 10)

        btn_wrapper_sizer.Add(self.commit_btn, 0, wx.ALIGN_RIGHT, 10)
        btn_wrapper_sizer.Add(self.cancel_btn, 0, wx.ALIGN_LEFT, 10)

        wrapper_sizer.AddSpacer(10)
        wrapper_sizer.Add(self.info_static_text, 0, wx.ALIGN_LEFT, 10)
        wrapper_sizer.AddSpacer(5)
        wrapper_sizer.Add(grid_sizer, 0, wx.ALIGN_LEFT | wx.ALL, 10)
        wrapper_sizer.AddSpacer(5)
        wrapper_sizer.Add(btn_wrapper_sizer, 0, wx.ALIGN_LEFT | wx.ALL, 10)
        wrapper_sizer.AddSpacer(10)

        main_sizer.AddSpacer(20)
        main_sizer.Add(wrapper_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        main_sizer.AddSpacer(20)

        self.SetSizer(main_sizer)
        main_sizer.Fit(self)


    def OnCancel(self,event):
        self.EndModal(True)

    def OnCommit(self,event, parent):

        conn_read = Read_And_Write_Files.Read_File('data_conn.tuk')
        server_in = conn_read[0]
        database_in = conn_read[1]
        port_in = conn_read[2]
        driver_in = conn_read[3]

        # Read current user info
        user_read = Read_And_Write_Files.Read_File('user.tuk')
        username = user_read[0]
        password = user_read[1]

        try:
            open_con = SQL.SQLCon(server_in, database_in, username, password, driver_in, port_in)
            ID = SQL.SQLGenerateNewID(open_con, "Products")
            insert_list = [ID,
                           self.brand_txt_ctrl.GetValue(),
                           self.supplier_txt_ctrl.GetValue(),
                           self.model_txt_ctrl.GetValue(),
                           self.company_code_txt_ctrl.GetValue(),
                           self.description_txt_ctrl.GetValue(),
                           self.color_txt_ctrl.GetValue(),
                           self.unit_of_measure_txt_ctrl.GetValue(),
                           self.total_qty_txt_ctrl.GetValue(),
                           self.project_qty_txt_ctrl.GetValue(),
                           self.free_stock_qty_txt_ctrl.GetValue(),
                           self.price_ex_vat_txt_ctrl.GetValue(),
                           ]

            #need to check insert list against names in the database
            insert_list = Data_Transforms.InsertListFillNull(insert_list)
            SQL.SQLInsertInto(open_con, username, "Products", insert_list)
            GUI.ProductsTab.OnSearch(parent, event)
            self.EndModal(True)
        except:
            # Error message
            ShowMessageDlg(self, "Failed to access the data base, please check with your system admin.", "Error"
                                , wx.OK | wx.CANCEL | wx.ICON_QUESTION)

class EditProductDialog(wx.Dialog):
    def __init__(self, parent, title, id_to_edit):
        super(EditProductDialog, self).__init__(parent, title=title, size=(600, 300))

        conn_read = Read_And_Write_Files.Read_File('data_conn.tuk')

        server_in = conn_read[0]
        database_in = conn_read[1]
        port_in = conn_read[2]
        driver_in = conn_read[3]

        # Read current user info
        user_read = Read_And_Write_Files.Read_File('user.tuk')
        username = user_read[0]
        password = user_read[1]

        open_con = SQL.SQLCon(server_in, database_in, username, password, driver_in, port_in)
        row_info_return = SQL.SQLSearchMultipleRow(open_con, "Products", "ID", id_to_edit)
        row_info_return = Data_Transforms.SplitAndCleanDBReturn(row_info_return)

        grid_sizer = wx.FlexGridSizer(5, 5, 10)
        wrapper_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_wrapper_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # ------------------------------------------------------------------------------
        # Create Widgets
        # ------------------------------------------------------------------------------

        self.info_static_text = wx.StaticText(self, label="To add a product to the database please fill out all of the "
                                                          "following information: ")

        self.model_static_text = wx.StaticText(self, label="Model: ")
        self.model_txt_ctrl = wx.TextCtrl(self, -1, row_info_return[3], size=(200, -1))

        self.brand_static_text = wx.StaticText(self, label="Brand: ")
        self.brand_txt_ctrl = wx.TextCtrl(self, -1, row_info_return[1], size=(200, -1))

        self.supplier_static_text = wx.StaticText(self, label="Supplier: ")
        self.supplier_txt_ctrl = wx.TextCtrl(self, -1, row_info_return[2], size=(200, -1))

        self.company_code_static_text = wx.StaticText(self, label="Company Code: ")
        self.company_code_txt_ctrl = wx.TextCtrl(self, -1, row_info_return[4], size=(200, -1))

        self.description_static_text = wx.StaticText(self, label="Description: ")
        self.description_txt_ctrl = wx.TextCtrl(self, -1, row_info_return[5], size=(200, -1))

        self.color_static_text = wx.StaticText(self, label="Color: ")
        self.color_txt_ctrl = wx.TextCtrl(self, -1, row_info_return[6], size=(200, -1))

        self.unit_of_measure_static_text = wx.StaticText(self, label="Unit Of Measure: ")
        self.unit_of_measure_txt_ctrl = wx.TextCtrl(self, -1, row_info_return[7], size=(200, -1))

        self.price_ex_vat_static_text = wx.StaticText(self, label="Price Ex VAT: ")
        self.price_ex_vat_txt_ctrl = wx.TextCtrl(self, -1, row_info_return[11], size=(200, -1))

        self.total_qty_static_text = wx.StaticText(self, label="Total Qty: ")
        self.total_qty_txt_ctrl = wx.TextCtrl(self, -1, row_info_return[8], size=(200, -1))

        self.project_qty_static_text = wx.StaticText(self, label="Project Qty: ")
        self.project_qty_txt_ctrl = wx.TextCtrl(self, -1, row_info_return[9], size=(200, -1))

        self.free_stock_qty_static_text = wx.StaticText(self, label="Free Stock Qty: ")
        self.free_stock_qty_txt_ctrl = wx.TextCtrl(self, -1, row_info_return[10], size=(200, -1))

        self.commit_btn = wx.Button(self, 0, label="Commit")
        self.commit_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnCommit(event, id_to_edit, parent))
        self.cancel_btn = wx.Button(self, 0, label="Cancel")
        self.cancel_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnCancel(event))

        grid_sizer.Add(self.model_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.model_txt_ctrl, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.AddSpacer(5)
        grid_sizer.Add(self.brand_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.brand_txt_ctrl, 0, wx.ALIGN_LEFT, 10)

        grid_sizer.Add(self.supplier_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.supplier_txt_ctrl, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.AddSpacer(5)
        grid_sizer.Add(self.company_code_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.company_code_txt_ctrl, 0, wx.ALIGN_LEFT, 10)

        grid_sizer.Add(self.description_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.description_txt_ctrl, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.AddSpacer(5)
        grid_sizer.Add(self.color_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.color_txt_ctrl, 0, wx.ALIGN_LEFT, 10)

        grid_sizer.Add(self.unit_of_measure_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.unit_of_measure_txt_ctrl, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.AddSpacer(5)
        grid_sizer.Add(self.price_ex_vat_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.price_ex_vat_txt_ctrl, 0, wx.ALIGN_LEFT, 10)

        grid_sizer.Add(self.total_qty_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.total_qty_txt_ctrl, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.AddSpacer(5)
        grid_sizer.Add(self.project_qty_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.project_qty_txt_ctrl, 0, wx.ALIGN_LEFT, 10)

        grid_sizer.Add(self.free_stock_qty_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.free_stock_qty_txt_ctrl, 0, wx.ALIGN_LEFT, 10)

        btn_wrapper_sizer.Add(self.commit_btn, 0, wx.ALIGN_RIGHT, 10)
        btn_wrapper_sizer.Add(self.cancel_btn, 0, wx.ALIGN_LEFT, 10)

        wrapper_sizer.AddSpacer(10)
        wrapper_sizer.Add(self.info_static_text, 0, wx.ALIGN_LEFT, 10)
        wrapper_sizer.AddSpacer(5)
        wrapper_sizer.Add(grid_sizer, 0, wx.ALIGN_LEFT | wx.ALL, 10)
        wrapper_sizer.AddSpacer(5)
        wrapper_sizer.Add(btn_wrapper_sizer, 0, wx.ALIGN_LEFT | wx.ALL, 10)
        wrapper_sizer.AddSpacer(10)

        main_sizer.AddSpacer(20)
        main_sizer.Add(wrapper_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        main_sizer.AddSpacer(20)

        self.SetSizer(main_sizer)
        main_sizer.Fit(self)

    def OnCancel(self, event):
        self.EndModal(True)

    def OnCommit(self,event, id_to_edit, parent):

        entry_list = [id_to_edit,
                      self.brand_txt_ctrl.GetValue(),
                      self.supplier_txt_ctrl.GetValue(),
                      self.model_txt_ctrl.GetValue(),
                      self.company_code_txt_ctrl.GetValue(),
                      self.description_txt_ctrl.GetValue(),
                      self.color_txt_ctrl.GetValue(),
                      self.unit_of_measure_txt_ctrl.GetValue(),
                      self.total_qty_txt_ctrl.GetValue(),
                      self.project_qty_txt_ctrl.GetValue(),
                      self.free_stock_qty_txt_ctrl.GetValue(),
                      self.price_ex_vat_txt_ctrl.GetValue()]

        conn_read = Read_And_Write_Files.Read_File('data_conn.tuk')
        server_in = conn_read[0]
        database_in = conn_read[1]
        port_in = conn_read[2]
        driver_in = conn_read[3]

        # Read current user info
        user_read = Read_And_Write_Files.Read_File('user.tuk')
        username = user_read[0]
        password = user_read[1]

        open_con = SQL.SQLCon(server_in, database_in, username, password, driver_in, port_in)
        column_list = SQL.SQLGetColumnNames(open_con, "Products")

        SQL.SQLUpdateEntry(open_con, "Products", id_to_edit, column_list, entry_list)
        GUI.ProductsTab.OnSearch(parent, event)

        self.EndModal(True)

# --------------------------------------------------------------------------------------------
# Stock Adjustment Tab Modals
# --------------------------------------------------------------------------------------------

class AssignToProjectInternal(wx.Dialog):
    def __init__(self, parent, title, selected_product, selected_project):
        super(AssignToProjectInternal, self).__init__(parent, title=title, size=(600, 300))
        grid_sizer = wx.FlexGridSizer(5, 5, 10)
        wrapper_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_wrapper_sizer = wx.BoxSizer(wx.HORIZONTAL)

        conn_read = Read_And_Write_Files.Read_File('data_conn.tuk')
        server_in = conn_read[0]
        database_in = conn_read[1]
        port_in = conn_read[2]
        driver_in = conn_read[3]

        # Read current user info
        user_read = Read_And_Write_Files.Read_File('user.tuk')
        username = user_read[0]
        password = user_read[1]

        try:
            # Open connection
            open_con = SQL.SQLCon(server_in, database_in, username, password, driver_in, port_in)
            project_list_return = SQL.SQLSearchAllSingleColumn(open_con, username, "Projects", "name")
            product_list_return = SQL.SQLSearchAllSingleColumn(open_con, username, "Products", "model")

        except:
            pass

        project_output_list = Data_Transforms.TransformRowToList(project_list_return)
        product_output_list = Data_Transforms.TransformRowToList(product_list_return)

        product_free_stock_return = SQL.SQLSearchColumnSingleEntry(open_con, "Products", "free_stock_qty", "model",
                                                                   selected_product)
        if product_free_stock_return != None:
            product_free_stock_return = Data_Transforms.TransformRowToList(product_free_stock_return)
        else:
            list = ['0']
            product_free_stock_return = list

        # ------------------------------------------------------------------------------
        # Create Widgets
        # ------------------------------------------------------------------------------
        self.info_static_text = wx.StaticText(self,
                                              label="Set the amount of free stock you wish to assign to a project to "
                                                    "be held internally")

        self.project_static_text = wx.StaticText(self, label="Project: ")
        self.project_drop_down = wx.ComboBox(self, size=wx.DefaultSize, choices=project_output_list)
        self.project_drop_down.SetValue(selected_project)

        self.product_static_text = wx.StaticText(self, label="Product: ")
        self.product_drop_down = wx.ComboBox(self, size=wx.DefaultSize, choices=product_output_list)
        self.product_drop_down.Bind(wx.EVT_COMBOBOX_CLOSEUP, lambda event: self.OnDropDownPick(event, parent, open_con))
        self.product_drop_down.SetValue(selected_product)

        self.free_stock_static_text = wx.StaticText(self, label="Free stock amount = ")
        self.free_stock_qty_static_text = wx.StaticText(self,
                                                        label=product_free_stock_return[0])

        self.assign_amount = wx.StaticText(self, label="Amount to assign: ")
        self.assign_amount_txt_ctrl = wx.TextCtrl(self, -1, "", size=(200, -1))

        self.commit_btn = wx.Button(self, 0, label="Commit")
        self.commit_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnCommit(event, parent, open_con))
        self.cancel_btn = wx.Button(self, 0, label="Close")
        self.cancel_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnCancel(event))

        grid_sizer.Add(self.project_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.project_drop_down, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.AddSpacer(5)
        grid_sizer.Add(self.product_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.product_drop_down, 0, wx.ALIGN_LEFT, 10)

        grid_sizer.Add(self.free_stock_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.free_stock_qty_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.AddSpacer(5)
        grid_sizer.Add(self.assign_amount, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.assign_amount_txt_ctrl, 0, wx.ALIGN_LEFT, 10)

        btn_wrapper_sizer.Add(self.commit_btn, 0, wx.ALIGN_RIGHT, 10)
        btn_wrapper_sizer.Add(self.cancel_btn, 0, wx.ALIGN_LEFT, 10)

        wrapper_sizer.AddSpacer(10)
        wrapper_sizer.Add(self.info_static_text, 0, wx.ALIGN_LEFT, 10)
        wrapper_sizer.AddSpacer(5)
        wrapper_sizer.Add(grid_sizer, 0, wx.ALIGN_LEFT | wx.ALL, 10)
        wrapper_sizer.AddSpacer(5)
        wrapper_sizer.Add(btn_wrapper_sizer, 0, wx.ALIGN_LEFT | wx.ALL, 10)
        wrapper_sizer.AddSpacer(10)

        main_sizer.AddSpacer(20)
        main_sizer.Add(wrapper_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        main_sizer.AddSpacer(20)

        self.SetSizer(main_sizer)
        main_sizer.Fit(self)

    def OnCommit(self, event, parent, open_con):
        # ------------------------------------------------------------------------------
        # Get user vales and clean off any additional white space
        # ------------------------------------------------------------------------------
        free_stock_qty = self.free_stock_qty_static_text.GetLabel().lstrip().rstrip()
        project_name = self.project_drop_down.GetValue().lstrip().rstrip()
        product_model = self.product_drop_down.GetValue().lstrip().rstrip()
        assign_value = self.assign_amount_txt_ctrl.GetValue().lstrip().rstrip()
        # ------------------------------------------------------------------------------
        # Check to see if there is enough free stock to assign
        if int(free_stock_qty) >= int(assign_value):
            # ------------------------------------------------------------------------------
            # Run main database searches
            # ------------------------------------------------------------------------------
            # Obtain project code
            project_code_return = SQL.SQLSearchColumnSingleEntry(open_con,
                                                                 "Projects",
                                                                 "project_code",
                                                                 "name",
                                                       project_name)
            # Obtain product cost
            cost = SQL.SQLSearchColumnSingleEntry(open_con,
                                                  "Products",
                                                  "price_ex_vat",
                                                  "model",
                                                  product_model)
            # pass code from list into variable and then clean
            project_code_return = project_code_return[0].lstrip().rstrip()
            cost = Data_Transforms.TransformRowToList(cost)
            cost = cost[0]
            # ------------------------------------------------------------------------------
            # Open connection to sub database and run search for product
            # ------------------------------------------------------------------------------
            conn_read = Read_And_Write_Files.Read_File('data_conn.tuk')
            server_in = conn_read[0]
            database_in = 'Sub_DB_' + project_code_return
            port_in = conn_read[2]
            driver_in = conn_read[3]

            # Read current user info
            user_read = Read_And_Write_Files.Read_File('user.tuk')
            username = user_read[0]
            password = user_read[1]
            # open connection to sub database
            open_con = SQL.SQLCon(server_in, database_in, username, password, driver_in, port_in)
            product_check = SQL.SQLSearchColumnSingleEntry(open_con, "project_stock", "model", "model", product_model)
            # ------------------------------------------------------------------------------
            # if check to see if the product is already in the project's database, if == none then we run insert!
            # ------------------------------------------------------------------------------
            if product_check == None:
                # ------------------------------------------------------------------------------
                # Insert product into sub database
                # ------------------------------------------------------------------------------
                ID = SQL.SQLGenerateNewID(open_con, "project_stock")
                cost = int(cost)
                cost = cost * int(assign_value)
                insert_list = [ID,
                               product_model,
                               assign_value,
                               assign_value,
                               '0',
                               cost]

                # need to check insert list against names in the database
                insert_list = Data_Transforms.InsertListFillNull(insert_list)
                SQL.SQLInsertInto(open_con, username, "project_stock", insert_list)
                # ------------------------------------------------------------------------------
                # Update free stock list in the project table
                # ------------------------------------------------------------------------------
                # Need to updated free stock list in the project table
                database_in = conn_read[1]
                # Open connection to main database
                open_con = SQL.SQLCon(server_in, database_in, username, password, driver_in, port_in)
                # Get column names
                column_list = SQL.SQLGetColumnNames(open_con, "Products")
                # Get all of the project information
                search_result = SQL.SQLSearchColumnMutipleEntry(open_con, username, "Products", product_model, column_list)
                search_result = Data_Transforms.SplitAndCleanDBReturn(search_result)
                search_result = Data_Transforms.TransformRowToList(search_result)
                project_stock_qty = int(search_result[9]) + int(assign_value)
                free_stock_qty = int(search_result[10]) - int(assign_value)
                entry_list = [search_result[0],
                              search_result[1],
                              search_result[2],
                              search_result[3],
                              search_result[4],
                              search_result[5],
                              search_result[6],
                              search_result[7],
                              search_result[8],
                              project_stock_qty,
                              free_stock_qty,
                              search_result[11]]

                SQL.SQLUpdateEntry(open_con, "Products", search_result[0], column_list, entry_list)
                # ------------------------------------------------------------------------------
                # Update customer balance
                # ------------------------------------------------------------------------------
                column_list = SQL.SQLGetColumnNames(open_con, "Customers")
                search_result = SQL.SQLSearchColumnMutipleEntry(open_con, username, "Customers", project_name,
                                                                column_list)

                search_result = Data_Transforms.SplitAndCleanDBReturn(search_result)
                search_result = Data_Transforms.TransformRowToList(search_result)
                balance = cost + int(search_result[3])
                entry_list = [search_result[0],
                              search_result[1],
                              search_result[2],
                              balance,
                              search_result[4],
                              search_result[5],
                              search_result[6],
                              search_result[7],
                              search_result[8]]

                SQL.SQLUpdateEntry(open_con, "Customers", search_result[0], column_list, entry_list)

            # if the product is in the database we run edit
            elif product_check != None:
                # ------------------------------------------------------------------------------
                # Edit product into sub database
                # ------------------------------------------------------------------------------
                column_list = SQL.SQLGetColumnNames(open_con, "project_stock")
                search_result = SQL.SQLSearchColumnMutipleEntry(open_con,
                                                                username,
                                                                "project_stock",
                                                                product_model,
                                                                column_list)
                search_result = Data_Transforms.SplitAndCleanDBReturn(search_result)
                cost = int(cost)
                cost = cost * int(assign_value)
                sub_cost = cost + int(search_result[5])
                total_qty = int(assign_value) + int(search_result[2])
                internal_held_qty = int(assign_value) + int(search_result[3])

                entry_list = [search_result[0],
                              search_result[1],
                              total_qty,
                              internal_held_qty,
                              search_result[4],
                              sub_cost]

                # need to check insert list against names in the database
                insert_list = Data_Transforms.InsertListFillNull(entry_list)
                SQL.SQLUpdateEntry(open_con, "project_stock", search_result[0], column_list, entry_list)


                # ------------------------------------------------------------------------------
                # Update free stock list in the project table
                # ------------------------------------------------------------------------------
                # Need to updated free stock list in the project table
                database_in = conn_read[1]
                # Open connection to main database
                open_con = SQL.SQLCon(server_in, database_in, username, password, driver_in, port_in)
                # Get column names
                column_list = SQL.SQLGetColumnNames(open_con, "Products")
                # Get all of the project information
                search_result = SQL.SQLSearchColumnMutipleEntry(open_con, username, "Products", product_model,
                                                                column_list)
                search_result = Data_Transforms.SplitAndCleanDBReturn(search_result)
                search_result = Data_Transforms.TransformRowToList(search_result)
                project_stock_qty = int(search_result[9]) + int(assign_value)
                free_stock_qty = int(search_result[10]) - int(assign_value)
                entry_list = [search_result[0],
                              search_result[1],
                              search_result[2],
                              search_result[3],
                              search_result[4],
                              search_result[5],
                              search_result[6],
                              search_result[7],
                              search_result[8],
                              project_stock_qty,
                              free_stock_qty,
                              search_result[11]]

                SQL.SQLUpdateEntry(open_con, "Products", search_result[0], column_list, entry_list)
                # ------------------------------------------------------------------------------
                # Update customer balance
                # ------------------------------------------------------------------------------
                column_list = SQL.SQLGetColumnNames(open_con, "Customers")
                search_result = SQL.SQLSearchColumnMutipleEntry(open_con, username, "Customers", project_name,
                                                                column_list)

                search_result = Data_Transforms.SplitAndCleanDBReturn(search_result)
                search_result = Data_Transforms.TransformRowToList(search_result)
                balance = cost + int(search_result[3])
                entry_list = [search_result[0],
                              search_result[1],
                              search_result[2],
                              balance,
                              search_result[4],
                              search_result[5],
                              search_result[6],
                              search_result[7],
                              search_result[8]]

                SQL.SQLUpdateEntry(open_con, "Customers", search_result[0], column_list, entry_list)

        else:
            # Error message
            ShowMessageDlg(self, "Can only assign free stock to a project, the value you entered was too high.", "Error"
                           , wx.OK | wx.CANCEL | wx.ICON_QUESTION)
            # ------------------------------------------------------------------------------
            # Open connection to sub database and run search for product
            # ------------------------------------------------------------------------------

        product_free_stock_return = SQL.SQLSearchColumnSingleEntry(open_con, "Products", "free_stock_qty", "model",
                                                                   product_model)
        self.free_stock_qty_static_text.SetLabel(product_free_stock_return[0])

    def OnDropDownPick(self, event, parent, open_con):
        product_selected = self.product_drop_down.GetValue()
        product_selected = product_selected.lstrip()
        product_selected = product_selected.rstrip()
        product_free_stock_return = SQL.SQLSearchColumnSingleEntry(open_con, "Products", "free_stock_qty", "model",
                                                                   product_selected)
        product_free_stock_return = Data_Transforms.TransformRowToList(product_free_stock_return)

        self.free_stock_qty_static_text.SetLabel(product_free_stock_return[0])
        #AssignToProjectInternal(self, 'Assign Product To Project Internal', product_selected).Refresh()

    def OnCancel(self,event):
        self.EndModal(True)

class AssignToProjectSite(wx.Dialog):
    def __init__(self, parent, title, selected_product, selected_project):
        super(AssignToProjectSite, self).__init__(parent, title=title, size=(600, 300))
        grid_sizer = wx.FlexGridSizer(5, 5, 10)
        wrapper_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_wrapper_sizer = wx.BoxSizer(wx.HORIZONTAL)

        conn_read = Read_And_Write_Files.Read_File('data_conn.tuk')
        server_in = conn_read[0]
        database_in = conn_read[1]
        port_in = conn_read[2]
        driver_in = conn_read[3]

        # Read current user info
        user_read = Read_And_Write_Files.Read_File('user.tuk')
        username = user_read[0]
        password = user_read[1]

        try:
            # Open connection
            open_con = SQL.SQLCon(server_in, database_in, username, password, driver_in, port_in)
            project_list_return = SQL.SQLSearchAllSingleColumn(open_con, username, "Projects", "name")
            product_list_return = SQL.SQLSearchAllSingleColumn(open_con, username, "Products", "model")

        except:
            pass

        project_output_list = Data_Transforms.TransformRowToList(project_list_return)
        product_output_list = Data_Transforms.TransformRowToList(product_list_return)

        product_free_stock_return = SQL.SQLSearchColumnSingleEntry(open_con, "Products", "free_stock_qty", "model",
                                                                   selected_product)
        if product_free_stock_return != None:
            product_free_stock_return = Data_Transforms.TransformRowToList(product_free_stock_return)
        else:
            list = ['0']
            product_free_stock_return = list

        # ------------------------------------------------------------------------------
        # Create Widgets
        # ------------------------------------------------------------------------------
        self.info_static_text = wx.StaticText(self,
                                              label="Set the amount of free stock you wish to assign to a project to "
                                                    "be held internally")

        self.project_static_text = wx.StaticText(self, label="Project: ")
        self.project_drop_down = wx.ComboBox(self, size=wx.DefaultSize, choices=project_output_list)
        self.project_drop_down.SetValue(selected_project)

        self.product_static_text = wx.StaticText(self, label="Product: ")
        self.product_drop_down = wx.ComboBox(self, size=wx.DefaultSize, choices=product_output_list)
        self.product_drop_down.Bind(wx.EVT_COMBOBOX_CLOSEUP, lambda event: self.OnDropDownPick(event, parent, open_con))
        self.product_drop_down.SetValue(selected_product)


        self.free_stock_static_text = wx.StaticText(self, label="Free stock amount = ")
        self.free_stock_qty_static_text = wx.StaticText(self,
                                                        label=product_free_stock_return[0])

        self.assign_amount = wx.StaticText(self, label="Amount to assign: ")
        self.assign_amount_txt_ctrl = wx.TextCtrl(self, -1, "", size=(200, -1))

        self.commit_btn = wx.Button(self, 0, label="Commit")
        self.commit_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnCommit(event, parent, open_con))
        self.cancel_btn = wx.Button(self, 0, label="Close")
        self.cancel_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnCancel(event))

        grid_sizer.Add(self.project_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.project_drop_down, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.AddSpacer(5)
        grid_sizer.Add(self.product_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.product_drop_down, 0, wx.ALIGN_LEFT, 10)

        grid_sizer.Add(self.free_stock_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.free_stock_qty_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.AddSpacer(5)
        grid_sizer.Add(self.assign_amount, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.assign_amount_txt_ctrl, 0, wx.ALIGN_LEFT, 10)

        btn_wrapper_sizer.Add(self.commit_btn, 0, wx.ALIGN_RIGHT, 10)
        btn_wrapper_sizer.Add(self.cancel_btn, 0, wx.ALIGN_LEFT, 10)

        wrapper_sizer.AddSpacer(10)
        wrapper_sizer.Add(self.info_static_text, 0, wx.ALIGN_LEFT, 10)
        wrapper_sizer.AddSpacer(5)
        wrapper_sizer.Add(grid_sizer, 0, wx.ALIGN_LEFT | wx.ALL, 10)
        wrapper_sizer.AddSpacer(5)
        wrapper_sizer.Add(btn_wrapper_sizer, 0, wx.ALIGN_LEFT | wx.ALL, 10)
        wrapper_sizer.AddSpacer(10)

        main_sizer.AddSpacer(20)
        main_sizer.Add(wrapper_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        main_sizer.AddSpacer(20)

        self.SetSizer(main_sizer)
        main_sizer.Fit(self)

    def OnCommit(self, event, parent, open_con):
        # ------------------------------------------------------------------------------
        # Get user vales and clean off any additional white space
        # ------------------------------------------------------------------------------
        free_stock_qty = self.free_stock_qty_static_text.GetLabel().lstrip().rstrip()
        project_name = self.project_drop_down.GetValue().lstrip().rstrip()
        product_model = self.product_drop_down.GetValue().lstrip().rstrip()
        assign_value = self.assign_amount_txt_ctrl.GetValue().lstrip().rstrip()
        # ------------------------------------------------------------------------------
        # Check to see if there is enough free stock to assign
        if int(free_stock_qty) >= int(assign_value):
            # ------------------------------------------------------------------------------
            # Run main database searches
            # ------------------------------------------------------------------------------
            # Obtain project code
            project_code_return = SQL.SQLSearchColumnSingleEntry(open_con,
                                                                 "Projects",
                                                                 "project_code",
                                                                 "name",
                                                       project_name)
            # Obtain product cost
            cost = SQL.SQLSearchColumnSingleEntry(open_con,
                                                  "Products",
                                                  "price_ex_vat",
                                                  "model",
                                                  product_model)
            # pass code from list into variable and then clean
            project_code_return = project_code_return[0].lstrip().rstrip()
            cost = Data_Transforms.TransformRowToList(cost)
            cost = cost[0]
            # ------------------------------------------------------------------------------
            # Open connection to sub database and run search for product
            # ------------------------------------------------------------------------------
            conn_read = Read_And_Write_Files.Read_File('data_conn.tuk')
            server_in = conn_read[0]
            database_in = 'Sub_DB_' + project_code_return
            port_in = conn_read[2]
            driver_in = conn_read[3]

            # Read current user info
            user_read = Read_And_Write_Files.Read_File('user.tuk')
            username = user_read[0]
            password = user_read[1]
            # open connection to sub database
            open_con = SQL.SQLCon(server_in, database_in, username, password, driver_in, port_in)
            product_check = SQL.SQLSearchColumnSingleEntry(open_con, "project_stock", "model", "model", product_model)
            # ------------------------------------------------------------------------------
            # if check to see if the product is already in the project's database, if == none then we run insert!
            # ------------------------------------------------------------------------------
            if product_check == None:
                # ------------------------------------------------------------------------------
                # Insert product into sub database
                # ------------------------------------------------------------------------------
                ID = SQL.SQLGenerateNewID(open_con, "project_stock")
                cost = int(cost)
                cost = cost * int(assign_value)
                insert_list = [ID,
                               product_model,
                               assign_value,
                               '0',
                               assign_value,
                               cost]

                # need to check insert list against names in the database
                insert_list = Data_Transforms.InsertListFillNull(insert_list)
                SQL.SQLInsertInto(open_con, username, "project_stock", insert_list)
                # ------------------------------------------------------------------------------
                # Update free stock list in the project table
                # ------------------------------------------------------------------------------
                # Need to updated free stock list in the project table
                database_in = conn_read[1]
                # Open connection to main database
                open_con = SQL.SQLCon(server_in, database_in, username, password, driver_in, port_in)
                # Get column names
                column_list = SQL.SQLGetColumnNames(open_con, "Products")
                # Get all of the project information
                search_result = SQL.SQLSearchColumnMutipleEntry(open_con, username, "Products", product_model, column_list)
                search_result = Data_Transforms.SplitAndCleanDBReturn(search_result)
                search_result = Data_Transforms.TransformRowToList(search_result)
                project_stock_qty = int(search_result[9]) + int(assign_value)
                free_stock_qty = int(search_result[10]) - int(assign_value)
                entry_list = [search_result[0],
                              search_result[1],
                              search_result[2],
                              search_result[3],
                              search_result[4],
                              search_result[5],
                              search_result[6],
                              search_result[7],
                              search_result[8],
                              project_stock_qty,
                              free_stock_qty,
                              search_result[11]]

                SQL.SQLUpdateEntry(open_con, "Products", search_result[0], column_list, entry_list)
                # ------------------------------------------------------------------------------
                # Update customer balance
                # ------------------------------------------------------------------------------
                column_list = SQL.SQLGetColumnNames(open_con, "Customers")
                search_result = SQL.SQLSearchColumnMutipleEntry(open_con, username, "Customers", project_name,
                                                                column_list)

                search_result = Data_Transforms.SplitAndCleanDBReturn(search_result)
                search_result = Data_Transforms.TransformRowToList(search_result)
                balance = cost + int(search_result[3])
                entry_list = [search_result[0],
                              search_result[1],
                              search_result[2],
                              balance,
                              search_result[4],
                              search_result[5],
                              search_result[6],
                              search_result[7],
                              search_result[8]]

                SQL.SQLUpdateEntry(open_con, "Customers", search_result[0], column_list, entry_list)

            # if the product is in the database we run edit
            elif product_check != None:
                # ------------------------------------------------------------------------------
                # Edit product into sub database
                # ------------------------------------------------------------------------------
                column_list = SQL.SQLGetColumnNames(open_con, "project_stock")
                search_result = SQL.SQLSearchColumnMutipleEntry(open_con,
                                                                username,
                                                                "project_stock",
                                                                product_model,
                                                                column_list)
                search_result = Data_Transforms.SplitAndCleanDBReturn(search_result)
                cost = int(cost)
                cost = cost * int(assign_value)
                sub_cost = cost + int(search_result[5])
                total_qty = int(assign_value) + int(search_result[2])
                site_held_qty = int(assign_value) + int(search_result[4])

                entry_list = [search_result[0],
                              search_result[1],
                              total_qty,
                              search_result[3],
                              site_held_qty,
                              sub_cost]

                # need to check insert list against names in the database
                insert_list = Data_Transforms.InsertListFillNull(entry_list)
                SQL.SQLUpdateEntry(open_con, "project_stock", search_result[0], column_list, entry_list)


                # ------------------------------------------------------------------------------
                # Update free stock list in the project table
                # ------------------------------------------------------------------------------
                # Need to updated free stock list in the project table
                database_in = conn_read[1]
                # Open connection to main database
                open_con = SQL.SQLCon(server_in, database_in, username, password, driver_in, port_in)
                # Get column names
                column_list = SQL.SQLGetColumnNames(open_con, "Products")
                # Get all of the project information
                search_result = SQL.SQLSearchColumnMutipleEntry(open_con, username, "Products", product_model,
                                                                column_list)
                search_result = Data_Transforms.SplitAndCleanDBReturn(search_result)
                search_result = Data_Transforms.TransformRowToList(search_result)
                project_stock_qty = int(search_result[9]) + int(assign_value)
                free_stock_qty = int(search_result[10]) - int(assign_value)
                entry_list = [search_result[0],
                              search_result[1],
                              search_result[2],
                              search_result[3],
                              search_result[4],
                              search_result[5],
                              search_result[6],
                              search_result[7],
                              search_result[8],
                              project_stock_qty,
                              free_stock_qty,
                              search_result[11]]

                SQL.SQLUpdateEntry(open_con, "Products", search_result[0], column_list, entry_list)
                # ------------------------------------------------------------------------------
                # Update customer balance
                # ------------------------------------------------------------------------------
                column_list = SQL.SQLGetColumnNames(open_con, "Customers")
                search_result = SQL.SQLSearchColumnMutipleEntry(open_con, username, "Customers", project_name,
                                                                column_list)

                search_result = Data_Transforms.SplitAndCleanDBReturn(search_result)
                search_result = Data_Transforms.TransformRowToList(search_result)
                balance = cost + int(search_result[3])
                entry_list = [search_result[0],
                              search_result[1],
                              search_result[2],
                              balance,
                              search_result[4],
                              search_result[5],
                              search_result[6],
                              search_result[7],
                              search_result[8]]

                SQL.SQLUpdateEntry(open_con, "Customers", search_result[0], column_list, entry_list)

        else:
            # Error message
            ShowMessageDlg(self, "Can only assign free stock to a project, the value you entered was too high.", "Error"
                           , wx.OK | wx.CANCEL | wx.ICON_QUESTION)

        # ------------------------------------------------------------------------------
        # Reupdate the modal to show the new level of free stock
        # ------------------------------------------------------------------------------
        product_free_stock_return = SQL.SQLSearchColumnSingleEntry(open_con, "Products", "free_stock_qty", "model",
                                                                   product_model)
        self.free_stock_qty_static_text.SetLabel(product_free_stock_return[0])

    def OnDropDownPick(self, event, parent, open_con):
        product_selected = self.product_drop_down.GetValue()
        product_selected = product_selected.lstrip()
        product_selected = product_selected.rstrip()
        product_free_stock_return = SQL.SQLSearchColumnSingleEntry(open_con, "Products", "free_stock_qty", "model",
                                                                   product_selected)
        product_free_stock_return = Data_Transforms.TransformRowToList(product_free_stock_return)

        self.free_stock_qty_static_text.SetLabel(product_free_stock_return[0])
        #AssignToProjectInternal(self, 'Assign Product To Project Internal', product_selected).Refresh()

    def OnCancel(self,event):
        self.EndModal(True)

class AssignToProjectFreeStock(wx.Dialog):
    def __init__(self, parent, title, selected_product, project_selected):
        super(AssignToProjectFreeStock, self).__init__(parent, title=title, size=(600, 300))
        grid_sizer = wx.FlexGridSizer(5, 5, 10)
        wrapper_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_wrapper_sizer = wx.BoxSizer(wx.HORIZONTAL)

        conn_read = Read_And_Write_Files.Read_File('data_conn.tuk')
        server_in = conn_read[0]
        database_in = conn_read[1]
        port_in = conn_read[2]
        driver_in = conn_read[3]

        # Read current user info
        user_read = Read_And_Write_Files.Read_File('user.tuk')
        username = user_read[0]
        password = user_read[1]

        try:
            # Open connection
            open_con = SQL.SQLCon(server_in, database_in, username, password, driver_in, port_in)
            project_list_return = SQL.SQLSearchAllSingleColumn(open_con, username, "Projects", "name")
            product_list_return = SQL.SQLSearchAllSingleColumn(open_con, username, "Products", "model")

        except:
            pass

        project_output_list = Data_Transforms.TransformRowToList(project_list_return)
        product_output_list = Data_Transforms.TransformRowToList(product_list_return)


        # ------------------------------------------------------------------------------
        # Get project code
        # ------------------------------------------------------------------------------
        project_code_return = SQL.SQLSearchColumnSingleEntry(open_con,
                                                             "Projects",
                                                             "project_code",
                                                             "name",
                                                             project_selected)
        if project_code_return != None:
            project_code_return = project_code_return[0].lstrip().rstrip()
            # ------------------------------------------------------------------------------
            # Open connection to sub database and run search for product
            # ------------------------------------------------------------------------------
            conn_read = Read_And_Write_Files.Read_File('data_conn.tuk')
            server_in = conn_read[0]
            database_in = 'Sub_DB_' + project_code_return
            port_in = conn_read[2]
            driver_in = conn_read[3]

            # Read current user info
            user_read = Read_And_Write_Files.Read_File('user.tuk')
            username = user_read[0]
            password = user_read[1]
            # open connection to sub database
            open_con = SQL.SQLCon(server_in, database_in, username, password, driver_in, port_in)
            # ------------------------------------------------------------------------------
            product_internal_stock_return = SQL.SQLSearchColumnSingleEntry(open_con,
                                                                            "project_stock",
                                                                            "internal_held_qty",
                                                                            "model",
                                                                            selected_product)
        else:
            product_internal_stock_return = None
        # ------------------------------------------------------------------------------
        # Check for a value
        # ------------------------------------------------------------------------------
        if product_internal_stock_return != None:
            product_internal_stock_return = Data_Transforms.TransformRowToList(product_internal_stock_return)
        else:
            list = ['0']
            product_internal_stock_return = list
        # ------------------------------------------------------------------------------
        if project_code_return != None:
            product_site_stock_return = SQL.SQLSearchColumnSingleEntry(open_con,
                                                                    "project_stock",
                                                                    "site_held_qty",
                                                                    "model",
                                                                    selected_product)
        else:
            product_site_stock_return = None
        # ------------------------------------------------------------------------------
        # Check for a value
        # ------------------------------------------------------------------------------
        if product_site_stock_return != None:
            product_site_stock_return = Data_Transforms.TransformRowToList(product_site_stock_return)
        else:
            list = ['0']
            product_site_stock_return = list

        # ------------------------------------------------------------------------------
        # Create Widgets
        # ------------------------------------------------------------------------------
        self.info_static_text = wx.StaticText(self,
                                              label="Set the amount of free stock you wish to assign to a project to "
                                                    "be held internally")

        self.project_static_text = wx.StaticText(self, label="Project: ")
        self.project_drop_down = wx.ComboBox(self, size=wx.DefaultSize, choices=project_output_list)
        self.project_drop_down.SetValue(project_selected)

        self.product_static_text = wx.StaticText(self, label="Product: ")
        self.product_drop_down = wx.ComboBox(self, size=wx.DefaultSize, choices=product_output_list)
        self.product_drop_down.Bind(wx.EVT_COMBOBOX_CLOSEUP, lambda event: self.OnDropDownPick(event, parent, open_con))
        self.product_drop_down.SetValue(selected_product)

        self.internal_stock_static_text = wx.StaticText(self, label="Internal stock amount = ")
        self.internal_stock_qty_static_text = wx.StaticText(self,
                                                        label=product_internal_stock_return[0])

        self.internal_assign_amount = wx.StaticText(self, label="Amount to assign: ")
        self.internal_assign_amount_txt_ctrl = wx.TextCtrl(self, -1, "", size=(200, -1))

        self.site_stock_static_text = wx.StaticText(self, label="Site stock amount = ")
        self.site_stock_qty_static_text = wx.StaticText(self,
                                                        label=product_site_stock_return[0])

        self.site_assign_amount = wx.StaticText(self, label="Amount to assign: ")
        self.site_assign_amount_txt_ctrl = wx.TextCtrl(self, -1, "", size=(200, -1))


        self.commit_btn = wx.Button(self, 0, label="Commit")
        self.commit_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnCommit(event, parent, open_con))
        self.cancel_btn = wx.Button(self, 0, label="Close")
        self.cancel_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnCancel(event))

        grid_sizer.Add(self.project_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.project_drop_down, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.AddSpacer(5)
        grid_sizer.Add(self.product_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.product_drop_down, 0, wx.ALIGN_LEFT, 10)

        grid_sizer.Add(self.internal_stock_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.internal_stock_qty_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.AddSpacer(5)
        grid_sizer.Add(self.internal_assign_amount, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.internal_assign_amount_txt_ctrl, 0, wx.ALIGN_LEFT, 10)

        grid_sizer.Add(self.site_stock_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.site_stock_qty_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.AddSpacer(5)
        grid_sizer.Add(self.site_assign_amount, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.site_assign_amount_txt_ctrl, 0, wx.ALIGN_LEFT, 10)

        btn_wrapper_sizer.Add(self.commit_btn, 0, wx.ALIGN_RIGHT, 10)
        btn_wrapper_sizer.Add(self.cancel_btn, 0, wx.ALIGN_LEFT, 10)

        wrapper_sizer.AddSpacer(10)
        wrapper_sizer.Add(self.info_static_text, 0, wx.ALIGN_LEFT, 10)
        wrapper_sizer.AddSpacer(5)
        wrapper_sizer.Add(grid_sizer, 0, wx.ALIGN_LEFT | wx.ALL, 10)
        wrapper_sizer.AddSpacer(5)
        wrapper_sizer.Add(btn_wrapper_sizer, 0, wx.ALIGN_LEFT | wx.ALL, 10)
        wrapper_sizer.AddSpacer(10)

        main_sizer.AddSpacer(20)
        main_sizer.Add(wrapper_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        main_sizer.AddSpacer(20)

        self.SetSizer(main_sizer)
        main_sizer.Fit(self)

    def OnCommit(self, event, parent, open_con):
        # ------------------------------------------------------------------------------
        # Get user vales and clean off any additional white space
        # ------------------------------------------------------------------------------
        internal_stock_qty = self.internal_stock_qty_static_text.GetLabel().lstrip().rstrip()
        site_stock_qty = self.site_stock_qty_static_text.GetLabel().lstrip().rstrip()

        project_name = self.project_drop_down.GetValue().lstrip().rstrip()
        product_model = self.product_drop_down.GetValue().lstrip().rstrip()
        assign_internal_value = self.internal_assign_amount_txt_ctrl.GetValue().lstrip().rstrip()
        assign_site_value = self.site_assign_amount_txt_ctrl.GetValue().lstrip().rstrip()
        # ------------------------------------------------------------------------------
        # Check to ensure the user has not up in any non int values into the text control
        # ------------------------------------------------------------------------------
        if assign_internal_value == "":
            assign_internal_value = 0
        else:
            assign_internal_value = ''.join([c for c in assign_internal_value if c in '1234567890.'])

        if assign_site_value == "":
            assign_site_value = 0
        else:
            assign_site_value = ''. join([chars for chars in assign_site_value if chars in '1234567890.'])

        # ------------------------------------------------------------------------------
        # Check to see if there is enough internal stock to assign
        if int(internal_stock_qty) >= int(assign_internal_value):
            # Check to see if there is enough site stock to assign
            if int(site_stock_qty) >= int(assign_site_value):
                conn_read = Read_And_Write_Files.Read_File('data_conn.tuk')
                server_in = conn_read[0]
                database_in = conn_read[1]
                port_in = conn_read[2]
                driver_in = conn_read[3]

                # Read current user info
                user_read = Read_And_Write_Files.Read_File('user.tuk')
                username = user_read[0]
                password = user_read[1]
                open_con = SQL.SQLCon(server_in, database_in, username, password, driver_in, port_in)
                # ------------------------------------------------------------------------------
                # Run main database searches
                # ------------------------------------------------------------------------------
                # Obtain project code
                project_code_return = SQL.SQLSearchColumnSingleEntry(open_con,
                                                                     "Projects",
                                                                     "project_code",
                                                                     "name",
                                                                     project_name)
                # Obtain product cost
                cost = SQL.SQLSearchColumnSingleEntry(open_con,
                                                      "Products",
                                                      "price_ex_vat",
                                                      "model",
                                                      product_model)

                # pass code from list into variable and then clean
                project_code_return = project_code_return[0].lstrip().rstrip()
                cost = Data_Transforms.TransformRowToList(cost)
                cost = cost[0]
                # ------------------------------------------------------------------------------
                # Open connection to sub database and run search for product
                # ------------------------------------------------------------------------------
                conn_read = Read_And_Write_Files.Read_File('data_conn.tuk')
                server_in = conn_read[0]
                database_in = 'Sub_DB_' + project_code_return
                port_in = conn_read[2]
                driver_in = conn_read[3]

                # Read current user info
                user_read = Read_And_Write_Files.Read_File('user.tuk')
                username = user_read[0]
                password = user_read[1]
                # open connection to sub database
                open_con = SQL.SQLCon(server_in, database_in, username, password, driver_in, port_in)

                # ------------------------------------------------------------------------------
                # Edit product into sub database
                # ------------------------------------------------------------------------------
                column_list = SQL.SQLGetColumnNames(open_con, "project_stock")
                search_result = SQL.SQLSearchColumnMutipleEntry(open_con,
                                                                username,
                                                                "project_stock",
                                                                product_model,
                                                                column_list)
                search_result = Data_Transforms.SplitAndCleanDBReturn(search_result)
                cost = int(cost)
                assign_values = int(assign_internal_value) + int(assign_site_value)
                cost = cost * assign_values
                sub_cost = int(search_result[5]) - cost
                total_qty = int(search_result[2]) - int(assign_values)
                internal_held_qty = int(search_result[3]) - int(assign_internal_value)
                site_held_qty = int(search_result[4]) - int(assign_site_value)
                entry_list = [search_result[0],
                              search_result[1],
                              total_qty,
                              internal_held_qty,
                              site_held_qty,
                              sub_cost]
                if total_qty == 0:
                    SQL.SQLRemove(open_con,"project_stock", "ID", search_result[0])
                else:
                    # need to check insert list against names in the database
                    #edit_list = Data_Transforms.InsertListFillNull(entry_list)
                    SQL.SQLUpdateEntry(open_con, "project_stock", search_result[0], column_list, entry_list)

                # ------------------------------------------------------------------------------
                # Update free stock list in the project table
                # ------------------------------------------------------------------------------
                # Need to updated free stock list in the project table
                database_in = conn_read[1]
                # Open connection to main database
                open_con = SQL.SQLCon(server_in, database_in, username, password, driver_in, port_in)
                # Get column names
                column_list = SQL.SQLGetColumnNames(open_con, "Products")
                # Get all of the project information
                search_result = SQL.SQLSearchColumnMutipleEntry(open_con, username, "Products", product_model,
                                                                column_list)
                search_result = Data_Transforms.SplitAndCleanDBReturn(search_result)
                search_result = Data_Transforms.TransformRowToList(search_result)
                project_stock_qty = int(search_result[9]) - int(assign_values)
                free_stock_qty = int(assign_values) + int(search_result[10])
                entry_list = [search_result[0],
                              search_result[1],
                              search_result[2],
                              search_result[3],
                              search_result[4],
                              search_result[5],
                              search_result[6],
                              search_result[7],
                              search_result[8],
                              project_stock_qty,
                              free_stock_qty,
                              search_result[11]]

                SQL.SQLUpdateEntry(open_con, "Products", search_result[0], column_list, entry_list)
                # ------------------------------------------------------------------------------
                # Update customer balance
                # ------------------------------------------------------------------------------
                column_list = SQL.SQLGetColumnNames(open_con, "Customers")
                search_result = SQL.SQLSearchColumnMutipleEntry(open_con, username, "Customers", project_name,
                                                                column_list)

                search_result = Data_Transforms.SplitAndCleanDBReturn(search_result)
                search_result = Data_Transforms.TransformRowToList(search_result)
                balance = int(search_result[3]) - cost
                entry_list = [search_result[0],
                              search_result[1],
                              search_result[2],
                              balance,
                              search_result[4],
                              search_result[5],
                              search_result[6],
                              search_result[7],
                              search_result[8]]

                SQL.SQLUpdateEntry(open_con, "Customers", search_result[0], column_list, entry_list)

            else:
                # Error message
                ShowMessageDlg(self, "Can only assign site stock to free stock, if the value you entered is lower than the ammount shown.", "Error"
                               , wx.OK | wx.CANCEL | wx.ICON_QUESTION)
        else:
            # Error message
            ShowMessageDlg(self, "Can only assign internal stock to free stock, if the value you entered is lower than the ammount shown.", "Error"
                           , wx.OK | wx.CANCEL | wx.ICON_QUESTION)

        # ------------------------------------------------------------------------------
        # Open connection to sub database and run search for product
        # ------------------------------------------------------------------------------
        conn_read = Read_And_Write_Files.Read_File('data_conn.tuk')
        server_in = conn_read[0]
        database_in = 'Sub_DB_' + project_code_return
        port_in = conn_read[2]
        driver_in = conn_read[3]

        # Read current user info
        user_read = Read_And_Write_Files.Read_File('user.tuk')
        username = user_read[0]
        password = user_read[1]
        # open connection to sub database
        open_con = SQL.SQLCon(server_in, database_in, username, password, driver_in, port_in)
        # ------------------------------------------------------------------------------
        product_internal_stock_return = SQL.SQLSearchColumnSingleEntry(open_con,
                                                                       "project_stock",
                                                                       "internal_held_qty",
                                                                       "model",
                                                                       product_model)
        # ------------------------------------------------------------------------------
        # Check for a value
        # ------------------------------------------------------------------------------
        if product_internal_stock_return != None:
            product_interal_stock_return = Data_Transforms.TransformRowToList(product_internal_stock_return)
        else:
            list = ['0']
            product_internal_stock_return = list
        # ------------------------------------------------------------------------------
        product_site_stock_return = SQL.SQLSearchColumnSingleEntry(open_con,
                                                                   "project_stock",
                                                                   "site_held_qty",
                                                                   "model",
                                                                   product_model)
        # ------------------------------------------------------------------------------
        # Check for a value
        # ------------------------------------------------------------------------------
        if product_site_stock_return != None:
            product_site_stock_return = Data_Transforms.TransformRowToList(product_site_stock_return)
        else:
            list = ['0']
            product_site_stock_return = list
        # ------------------------------------------------------------------------------
        self.internal_stock_qty_static_text.SetLabel(product_internal_stock_return[0])
        self.site_stock_qty_static_text.SetLabel(product_site_stock_return[0])
        # ------------------------------------------------------------------------------

    def OnDropDownPick(self, event, parent, open_con):
        # ------------------------------------------------------------------------------
        # Open connection to main database and run search for project code
        # ------------------------------------------------------------------------------
        conn_read = Read_And_Write_Files.Read_File('data_conn.tuk')
        server_in = conn_read[0]
        database_in = conn_read[1]
        port_in = conn_read[2]
        driver_in = conn_read[3]

        # Read current user info
        user_read = Read_And_Write_Files.Read_File('user.tuk')
        username = user_read[0]
        password = user_read[1]
        # open connection to sub database
        open_con = SQL.SQLCon(server_in, database_in, username, password, driver_in, port_in)
        product_selected = self.product_drop_down.GetValue()
        project_selected = self.project_drop_down.GetValue()
        product_selected = product_selected.lstrip()
        product_selected = product_selected.rstrip()
        project_selected = project_selected.lstrip()
        project_selected = project_selected.rstrip()

        # ------------------------------------------------------------------------------
        # Get project code
        # ------------------------------------------------------------------------------
        project_code_return = SQL.SQLSearchColumnSingleEntry(open_con,
                                                             "Projects",
                                                             "project_code",
                                                             "name",
                                                             project_selected)
        project_code_return = project_code_return[0].lstrip().rstrip()
        # ------------------------------------------------------------------------------
        # Open connection to sub database and run search for product
        # ------------------------------------------------------------------------------
        conn_read = Read_And_Write_Files.Read_File('data_conn.tuk')
        server_in = conn_read[0]
        database_in = 'Sub_DB_' + project_code_return
        port_in = conn_read[2]
        driver_in = conn_read[3]

        # Read current user info
        user_read = Read_And_Write_Files.Read_File('user.tuk')
        username = user_read[0]
        password = user_read[1]
        # open connection to sub database
        open_con = SQL.SQLCon(server_in, database_in, username, password, driver_in, port_in)
        # ------------------------------------------------------------------------------
        product_internal_stock_return = SQL.SQLSearchColumnSingleEntry(open_con,
                                                                      "project_stock",
                                                                      "internal_held_qty",
                                                                      "model",
                                                                      product_selected)
        # ------------------------------------------------------------------------------
        # Check for a value
        # ------------------------------------------------------------------------------
        if product_internal_stock_return != None:
            product_interal_stock_return = Data_Transforms.TransformRowToList(product_internal_stock_return)
        else:
            list = ['0']
            product_internal_stock_return = list
        # ------------------------------------------------------------------------------
        product_site_stock_return = SQL.SQLSearchColumnSingleEntry(open_con,
                                                                   "project_stock",
                                                                   "site_held_qty",
                                                                   "model",
                                                                   product_selected)
        # ------------------------------------------------------------------------------
        # Check for a value
        # ------------------------------------------------------------------------------
        if product_site_stock_return != None:
            product_site_stock_return = Data_Transforms.TransformRowToList(product_site_stock_return)
        else:
            list = ['0']
            product_site_stock_return = list
        # ------------------------------------------------------------------------------
        self.internal_stock_qty_static_text.SetLabel(product_internal_stock_return[0])
        self.site_stock_qty_static_text.SetLabel(product_site_stock_return[0])
        # ------------------------------------------------------------------------------

class ProjectStock(wx.Dialog):
    def __init__(self, parent, title, project_selected):
        super(ProjectStock, self).__init__(parent, title=title, size=(600, 300))
        # ----------------------------------------------------------------
        self.product_stock_list_view = ObjectListView(self, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        # ----------------------------------------------------------------
        self.product_stock_ok_btn = wx.Button(self, 0, label="Ok")
        self.product_stock_ok_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnOk(event))
        self.product_stock_print_btn = wx.Button(self, 0, label="Print")
        self.product_stock_print_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnPrint(event))
        # ----------------------------------------------------------------
        product_stock_inner_sizer = wx.BoxSizer(wx.VERTICAL)
        product_stock_btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        product_stock_wrapper_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # ----------------------------------------------------------------
        product_stock_btn_sizer.Add(self.product_stock_ok_btn, 0, wx.ALIGN_CENTER, 10)
        product_stock_btn_sizer.Add(self.product_stock_print_btn, 0, wx.ALIGN_CENTER, 10)
        # ----------------------------------------------------------------
        product_stock_inner_sizer.AddSpacer(10)
        product_stock_inner_sizer.Add(self.product_stock_list_view, 1, wx.ALL | wx.EXPAND, 10)
        product_stock_inner_sizer.Add(product_stock_btn_sizer)
        product_stock_inner_sizer.AddSpacer(10)
        # ----------------------------------------------------------------
        product_stock_wrapper_sizer.AddSpacer(10)
        product_stock_wrapper_sizer.Add(product_stock_inner_sizer, 1, wx.ALL | wx.EXPAND)
        product_stock_wrapper_sizer.AddSpacer(10)
        # ----------------------------------------------------------------
        # --------------------------------------------------------------------------------------------
        Object_List_View_Builder.SetColumnsProjectStock(self.product_stock_list_view)
        # --------------------------------------------------------------------------------------------
        self.SetSizer(product_stock_wrapper_sizer)

        # Read database connection info
        conn_read = Read_And_Write_Files.Read_File('data_conn.tuk')
        server_in = conn_read[0]
        project_selected = project_selected.lstrip()
        project_selected = project_selected.rstrip()

        database_in = ("Sub_DB_" + project_selected)
        port_in = conn_read[2]
        driver_in = conn_read[3]

        # Read current user info
        user_read = Read_And_Write_Files.Read_File('user.tuk')
        username = user_read[0]
        password = user_read[1]



        try:
            # Open connection
            open_con = SQL.SQLCon(server_in, database_in, username, password, driver_in, port_in)
            # Get table column names
            column_list = SQL.SQLGetColumnNames(open_con, "project_stock")
            # Check to see if we should search all or a for a value

            # Search All
            search_result = SQL.SQLSearchAll(open_con, username, "project_stock", "Search All", "Search All")
            # Update table with return from database
            ProjectStock.UpdateDisplay(self, search_result)




        except:
            # Error message
            ShowMessageDlg(self, "Failed to access the data base, please check with your system admin.",
                                  "Error"
                                  , wx.OK | wx.CANCEL | wx.ICON_QUESTION)

    def OnOk(self, event):
        self.EndModal(True)

    def OnPrint(self, event):
        ShowMessageDlg(self, "This function has not yet been implemented", "Print User Logs",
                       wx.OK | wx.CANCEL | wx.ICON_QUESTION)
        self.EndModal(True)

    def UpdateDisplay(self, entry_list):
        # Create a list to be inserted into the table
        self.construction_list = []
        for row in entry_list:
                # Split the tuple returned from the data base into individual values
            build_list = str(row).split(',')
            ID = build_list[0].replace('(', "").replace("'", "")
            Project_Code = build_list[1].replace("'", "")
            Name = build_list[2].replace("'", "")
            Status = build_list[3].replace("'", "")
            Customer = build_list[4].replace("'", "")
            Cost = build_list[5].replace(')', "").replace("'", "")

            # Create the object that will build the list for the table
            self.construction_list.append(Object_List_View_Builder.ProjectStockRowBuilder(ID,
                                                                                        Project_Code,
                                                                                        Name,
                                                                                        Status,
                                                                                        Customer,
                                                                                        Cost
                                                                                        ))
            # Set the current object list for the table
            self.product_stock_list_view.SetObjects(self.construction_list)

class ProductAssign(wx.Dialog):
    def __init__(self, parent, title, product_selected):
        super(ProductAssign, self).__init__(parent, title=title, size=(600, 300))

# --------------------------------------------------------------------------------------------
# Order Menu Tab Modals
# --------------------------------------------------------------------------------------------

class MakeOrderRequest(wx.Dialog):
    def __init__(self, parent, title):
        super(MakeOrderRequest, self).__init__(parent, title=title, size=(600, 300))

        grid_sizer = wx.FlexGridSizer(5, 8, 10)
        wrapper_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_wrapper_sizer = wx.BoxSizer(wx.HORIZONTAL)
        width = 230

        conn_read = Read_And_Write_Files.Read_File('data_conn.tuk')
        server_in = conn_read[0]
        database_in = conn_read[1]
        port_in = conn_read[2]
        driver_in = conn_read[3]

        # Read current user info
        user_read = Read_And_Write_Files.Read_File('user.tuk')
        username = user_read[0]
        password = user_read[1]

        try:
            # Open connection
            open_con = SQL.SQLCon(server_in, database_in, username, password, driver_in, port_in)
            product_list_return = SQL.SQLSearchAllSingleColumn(open_con, username, "Products", "model")
            project_list_return = SQL.SQLSearchAllSingleColumn(open_con, username, "Projects", "name")
            product_list_return = Data_Transforms.TransformRowToList(product_list_return)
            project_list_return = Data_Transforms.TransformRowToList(project_list_return)
            project_list_return = ['Free Stock'] + project_list_return
        except:
            pass

        self.supplier = ''
        self.brand = ''
        self.company_code = ''
        self.unit_of_measure = ''
        self.color = ''
        self.description = ''
        self.line_total = ''
        self.cost_value = ''

        self.info_static_text = wx.StaticText(self, label="Create a order to be processed:")

        self.model_static_text = wx.StaticText(self, label="Model: ")
        self.model_drop_down = wx.ComboBox(self, size=wx.DefaultSize, choices=product_list_return)
        self.model_drop_down.Bind(wx.EVT_COMBOBOX_CLOSEUP, lambda event: self.OnProductDropDownPick(event, parent, open_con))

        self.project_static_text = wx.StaticText(self, label="Project: ")
        self.project_drop_down = wx.ComboBox(self, size=wx.DefaultSize, choices=project_list_return)

        self.order_raiser_static_text = wx.StaticText(self, label="Order Raiser: ")
        self.order_raiser_txt_ctrl = wx.TextCtrl(self, -1, username, size=(200, -1))

        self.supplier_static_text = wx.StaticText(self, label="Supplier: ")
        self.supplier_place_holder_text = wx.StaticText(self, label=self.supplier)

        self.status_static_text = wx.StaticText(self, label="Status: ")
        self.status_txt_ctrl = wx.TextCtrl(self, -1, "", size=(200, -1))

        self.brand_static_text = wx.StaticText(self, label="Brand: ")
        self.brand_place_holder_text = wx.StaticText(self, label=self.brand)

        self.qty_static_text = wx.StaticText(self, label="Qty: ")
        self.qty_txt_ctrl = wx.TextCtrl(self, -1, "", size=(200, -1))
        self.qty_txt_ctrl.Bind(wx.EVT_TEXT, lambda event: self.QtyTextEnter(event))

        self.company_code_static_text = wx.StaticText(self, label="Company Code: ")
        self.company_code_place_holder_text = wx.StaticText(self, label=self.company_code)

        self.date_to_order_static_text = wx.StaticText(self, label="Date To Order By: ")
        self.date_to_order_txt_ctrl = wx.TextCtrl(self, -1, "", size=(200, -1))

        self.unit_of_measure_static_text = wx.StaticText(self, label="Unit Of Measure: ")
        self.unit_of_measure_place_holder_text = wx.StaticText(self, label=self.unit_of_measure)

        self.order_comments_static_text = wx.StaticText(self, label="Order Comments: ")
        self.order_comments_txt_ctrl = wx.TextCtrl(self, -1, "", size=(200, -1))

        self.color_static_text = wx.StaticText(self, label="Color: ")
        self.color_place_holder_text = wx.StaticText(self, label=self.color)

        self.description_static_text = wx.StaticText(self, label="Description: ")
        self.description_place_holder_text = wx.StaticText(self, label=self.description)
        self.description_place_holder_text.Wrap(width)

        self.line_total_static_text = wx.StaticText(self, label="Line Total: ")
        self.line_total_place_holder_text = wx.StaticText(self, label=self.line_total)

        self.commit_btn = wx.Button(self, 0, label="Commit")
        self.commit_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnCommit(event, parent))
        self.cancel_btn = wx.Button(self, 0, label="Cancel")
        self.cancel_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnCancel(event))

        grid_sizer.Add(self.model_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.model_drop_down, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.AddSpacer(5)
        grid_sizer.Add(self.project_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.project_drop_down, 0, wx.ALIGN_LEFT, 10)

        grid_sizer.Add(self.order_raiser_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.order_raiser_txt_ctrl, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.AddSpacer(5)
        grid_sizer.Add(self.supplier_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.supplier_place_holder_text, 0, wx.ALIGN_LEFT, 10)

        grid_sizer.Add(self.status_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.status_txt_ctrl, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.AddSpacer(5)
        grid_sizer.Add(self.brand_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.brand_place_holder_text, 0, wx.ALIGN_LEFT, 10)

        grid_sizer.Add(self.qty_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.qty_txt_ctrl, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.AddSpacer(5)
        grid_sizer.Add(self.company_code_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.company_code_place_holder_text, 0, wx.ALIGN_LEFT, 10)

        grid_sizer.Add(self.date_to_order_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.date_to_order_txt_ctrl, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.AddSpacer(5)
        grid_sizer.Add(self.unit_of_measure_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.unit_of_measure_place_holder_text, 0, wx.ALIGN_LEFT, 10)

        grid_sizer.Add(self.order_comments_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.order_comments_txt_ctrl, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.AddSpacer(5)
        grid_sizer.Add(self.color_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.color_place_holder_text, 0, wx.ALIGN_LEFT, 10)

        grid_sizer.Add(self.description_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.description_place_holder_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.AddSpacer(5)
        grid_sizer.Add(self.line_total_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.line_total_place_holder_text, 0, wx.ALIGN_LEFT, 10)

        btn_wrapper_sizer.Add(self.commit_btn, 0, wx.ALIGN_RIGHT, 10)
        btn_wrapper_sizer.Add(self.cancel_btn, 0, wx.ALIGN_LEFT, 10)

        wrapper_sizer.AddSpacer(10)
        wrapper_sizer.Add(self.info_static_text, 0, wx.ALIGN_LEFT, 10)
        wrapper_sizer.AddSpacer(5)
        wrapper_sizer.Add(grid_sizer, 0, wx.ALIGN_LEFT | wx.ALL, 10)
        wrapper_sizer.AddSpacer(5)
        wrapper_sizer.Add(btn_wrapper_sizer, 0, wx.ALIGN_LEFT | wx.ALL, 10)
        wrapper_sizer.AddSpacer(10)

        main_sizer.AddSpacer(20)
        main_sizer.Add(wrapper_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        main_sizer.AddSpacer(20)

        self.SetSizer(main_sizer)
        main_sizer.Fit(self)

    def QtyTextEnter(self, event):
        # get the qty and the line total
        qty = self.qty_txt_ctrl.GetValue()
        line_total = self.line_total_place_holder_text.GetLabel()

        if self.cost_value == '':
            line_total = '0'
        else:
            line_total = self.cost_value

        line_total = ''.join([c for c in line_total if c in '1234567890.'])

        if qty.isdigit():
            int_qty = int(qty)
            line_total = int(line_total)

            line_total = line_total * int_qty
            line_total = str(line_total)
            self.line_total_place_holder_text.SetLabel(line_total)
            return
        else:
            qty = ''.join(c for c in qty if c.isdigit())
            if qty == '':
                qty = '0'
            int_qty = int(qty)
            line_total = int(line_total)
            line_total = line_total * int_qty
            line_total = str(line_total)
            self.line_total_place_holder_text.SetLabel(line_total)
            self.qty_txt_ctrl.SetValue(qty)

    def OnProductDropDownPick(self, event, parent, open_con):
        product_selected = self.model_drop_down.GetValue().lstrip().rstrip()

        column_list = SQL.SQLGetColumnNames(open_con, "Products")
        search_result = SQL.SQLSearchColumnMutipleEntry(open_con, 'pass', "Products", product_selected,
                                                        column_list)
        search_result = Data_Transforms.SplitAndCleanDBReturn(search_result)

        qty = self.qty_txt_ctrl.GetValue()
        if qty == '':
            qty = 0
        self.cost_value = search_result[11]
        line_total = int(qty) * int(search_result[11])

        self.supplier_place_holder_text.SetLabel(search_result[2])
        self.brand_place_holder_text.SetLabel(search_result[1])
        self.company_code_place_holder_text.SetLabel(search_result[4])
        self.unit_of_measure_place_holder_text.SetLabel(search_result[7])
        self.color_place_holder_text.SetLabel(search_result[6])
        self.description_place_holder_text.SetLabel(search_result[5])
        self.line_total_place_holder_text.SetLabel(str(line_total))

    def OnCommit(self,event, parent):

        conn_read = Read_And_Write_Files.Read_File('data_conn.tuk')
        server_in = conn_read[0]
        database_in = conn_read[1]
        port_in = conn_read[2]
        driver_in = conn_read[3]

        # Read current user info
        user_read = Read_And_Write_Files.Read_File('user.tuk')
        username = user_read[0]
        password = user_read[1]

        try:
            open_con = SQL.SQLCon(server_in, database_in, username, password, driver_in, port_in)
            ID = SQL.SQLGenerateNewID(open_con, "Order_Menu")
            insert_list = [ID,
                           self.status_txt_ctrl.GetValue(),
                           self.order_raiser_txt_ctrl.GetValue(),
                           self.project_drop_down.GetValue(),
                           self.supplier_place_holder_text.GetLabel(),
                           self.brand_place_holder_text.GetLabel(),
                           self.model_drop_down.GetValue(),
                           self.company_code_place_holder_text.GetLabel(),
                           self.description_place_holder_text.GetLabel(),
                           self.unit_of_measure_place_holder_text.GetLabel(),
                           self.qty_txt_ctrl.GetValue(),
                           self.line_total_place_holder_text.GetLabel(),
                           self.color_place_holder_text.GetLabel(),
                           self.date_to_order_txt_ctrl.GetValue(),
                           self.order_comments_txt_ctrl.GetValue(),
                           '',
                           '',
                           ''
                           ]

            #need to check insert list against names in the database
            insert_list = Data_Transforms.InsertListFillNull(insert_list)
            SQL.SQLInsertInto(open_con, username, "Order_Menu", insert_list)
            GUI.OrderMenuTab.OnSearch(parent, event)
            self.EndModal(True)
        except:
            # Error message
            ShowMessageDlg(self, "Failed to access the data base, please check with your system admin.", "Error"
                                , wx.OK | wx.CANCEL | wx.ICON_QUESTION)

    def OnCancel(self, event):
        self.EndModal(True)

class ConfirmOrder(wx.Dialog):
    def __init__(self, parent, title, row_to_edit):
        super(ConfirmOrder, self).__init__(parent, title=title, size=(600, 300))

        conn_read = Read_And_Write_Files.Read_File('data_conn.tuk')
        server_in = conn_read[0]
        database_in = conn_read[1]
        port_in = conn_read[2]
        driver_in = conn_read[3]

        # Read current user info
        user_read = Read_And_Write_Files.Read_File('user.tuk')
        username = user_read[0]
        password = user_read[1]

        open_con = SQL.SQLCon(server_in, database_in, username, password, driver_in, port_in)

        column_list = SQL.SQLGetColumnNames(open_con, "Order_Menu")
        open_con = SQL.SQLCon(server_in, database_in, username, password, driver_in, port_in)

        row_info_return = SQL.SQLSearchMultipleRow(open_con, "Order_Menu", "ID", row_to_edit)
        row_info_return = Data_Transforms.SplitAndCleanDBReturn(row_info_return)

        ID = row_info_return[0]
        project = row_info_return[3]
        order_raiser = row_info_return[2]
        supplier = row_info_return[5]
        status = row_info_return[1]
        brand = row_info_return[4]
        model = row_info_return[6]
        order_comments = row_info_return[14]
        date_to_order = row_info_return[13]

        grid_sizer = wx.FlexGridSizer(5, 5, 10)
        wrapper_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_wrapper_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.info_static_text = wx.StaticText(self, label="Confirm a order has been placed:")

        self.order_id_static_text = wx.StaticText(self, label="Order ID: ")
        self.order_id_place_holder_text = wx.StaticText(self, label=ID)

        self.project_static_text = wx.StaticText(self, label="Project: ")
        self.project_place_holder_text = wx.StaticText(self, label=project)

        self.order_raiser_static_text = wx.StaticText(self, label="Order Raiser: ")
        self.order_raiser_place_holder_text = wx.StaticText(self, label=order_raiser)

        self.supplier_static_text = wx.StaticText(self, label="Supplier: ")
        self.supplier_place_holder_text = wx.StaticText(self, label=supplier)

        self.brand_static_text = wx.StaticText(self, label="Brand: ")
        self.brand_place_holder_text = wx.StaticText(self, label=brand)

        self.model_static_text = wx.StaticText(self, label="Model: ")
        self.model_place_holder_text = wx.StaticText(self, label=model)

        self.order_comments_static_text = wx.StaticText(self, label="Order Comments: ")
        self.order_comments_place_holder_text = wx.StaticText(self, label=order_comments)

        self.date_to_order_static_text = wx.StaticText(self, label="Order Comments: ")
        self.date_to_order_place_holder_text = wx.StaticText(self, label=date_to_order)

        self.status_static_text = wx.StaticText(self, label="Status: ")
        self.status_txt_ctrl = wx.TextCtrl(self, -1, "", size=(200, -1))

        self.date_ordered_static_text = wx.StaticText(self, label="Date Ordered: ")
        self.date_ordered_txt_ctrl = wx.TextCtrl(self, -1, "", size=(200, -1))

        self.purchase_order_static_text = wx.StaticText(self, label="Purchase Order: ")
        self.purchase_order_txt_ctrl = wx.TextCtrl(self, -1, "", size=(200, -1))

        self.expected_delivery_date_static_text = wx.StaticText(self, label="Expected Delivery: ")
        self.expected_delivery_txt_ctrl = wx.TextCtrl(self, -1, "", size=(200, -1))

        self.commit_btn = wx.Button(self, 0, label="Commit")
        self.commit_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnCommit(event, parent, ID, row_info_return))
        self.cancel_btn = wx.Button(self, 0, label="Cancel")
        self.cancel_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnCancel(event))

        grid_sizer.Add(self.order_id_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.order_id_place_holder_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.AddSpacer(5)
        grid_sizer.Add(self.project_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.project_place_holder_text, 0, wx.ALIGN_LEFT, 10)

        grid_sizer.Add(self.order_raiser_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.order_raiser_place_holder_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.AddSpacer(5)
        grid_sizer.Add(self.supplier_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.supplier_place_holder_text, 0, wx.ALIGN_LEFT, 10)

        grid_sizer.Add(self.brand_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.brand_place_holder_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.AddSpacer(5)
        grid_sizer.Add(self.model_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.model_place_holder_text, 0, wx.ALIGN_LEFT, 10)


        grid_sizer.Add(self.order_comments_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.order_comments_place_holder_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.AddSpacer(5)
        grid_sizer.Add(self.date_to_order_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.date_to_order_place_holder_text, 0, wx.ALIGN_LEFT, 10)

        grid_sizer.AddSpacer(5)
        grid_sizer.AddSpacer(5)
        grid_sizer.AddSpacer(5)
        grid_sizer.AddSpacer(5)
        grid_sizer.AddSpacer(5)

        grid_sizer.Add(self.status_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.status_txt_ctrl, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.AddSpacer(5)
        grid_sizer.Add(self.date_ordered_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.date_ordered_txt_ctrl, 0, wx.ALIGN_LEFT, 10)

        grid_sizer.Add(self.purchase_order_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.purchase_order_txt_ctrl, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.AddSpacer(5)
        grid_sizer.Add(self.expected_delivery_date_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.expected_delivery_txt_ctrl, 0, wx.ALIGN_LEFT, 10)


        btn_wrapper_sizer.Add(self.commit_btn, 0, wx.ALIGN_RIGHT, 10)
        btn_wrapper_sizer.Add(self.cancel_btn, 0, wx.ALIGN_LEFT, 10)

        wrapper_sizer.AddSpacer(10)
        wrapper_sizer.Add(self.info_static_text, 0, wx.ALIGN_LEFT, 10)
        wrapper_sizer.AddSpacer(5)
        wrapper_sizer.Add(grid_sizer, 0, wx.ALIGN_LEFT | wx.ALL, 10)
        wrapper_sizer.AddSpacer(5)
        wrapper_sizer.Add(btn_wrapper_sizer, 0, wx.ALIGN_LEFT | wx.ALL, 10)
        wrapper_sizer.AddSpacer(10)

        main_sizer.AddSpacer(20)
        main_sizer.Add(wrapper_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        main_sizer.AddSpacer(20)

        self.SetSizer(main_sizer)
        main_sizer.Fit(self)

    def OnCommit(self, event, parent, id_to_edit, row_info_return):
        entry_list = [id_to_edit,
                      self.status_txt_ctrl.GetValue(),
                      row_info_return[2],
                      row_info_return[3],
                      row_info_return[4],
                      row_info_return[5],
                      row_info_return[6],
                      row_info_return[7],
                      row_info_return[8],
                      row_info_return[9],
                      row_info_return[10],
                      row_info_return[11],
                      row_info_return[12],
                      row_info_return[13],
                      row_info_return[14],
                      self.date_ordered_txt_ctrl.GetValue(),
                      self.purchase_order_txt_ctrl.GetValue(),
                      self.expected_delivery_txt_ctrl.GetValue()]



        conn_read = Read_And_Write_Files.Read_File('data_conn.tuk')
        server_in = conn_read[0]
        database_in = conn_read[1]
        port_in = conn_read[2]
        driver_in = conn_read[3]

        # Read current user info
        user_read = Read_And_Write_Files.Read_File('user.tuk')
        username = user_read[0]
        password = user_read[1]

        open_con = SQL.SQLCon(server_in, database_in, username, password, driver_in, port_in)
        column_list = SQL.SQLGetColumnNames(open_con, "Order_Menu")

        SQL.SQLUpdateEntry(open_con, "Order_Menu", id_to_edit, column_list, entry_list)
        GUI.OrderMenuTab.OnSearch(parent, event)

        self.EndModal(True)

    def OnCancel(self, event):
        self.EndModal(True)

class NoteOrderReceivedProject(wx.Dialog):
    def __init__(self, parent, title, row_to_edit):
        super(NoteOrderReceivedProject, self).__init__(parent, title=title, size=(600, 300))

        conn_read = Read_And_Write_Files.Read_File('data_conn.tuk')
        server_in = conn_read[0]
        database_in = conn_read[1]
        port_in = conn_read[2]
        driver_in = conn_read[3]

        # Read current user info
        user_read = Read_And_Write_Files.Read_File('user.tuk')
        username = user_read[0]
        password = user_read[1]

        open_con = SQL.SQLCon(server_in, database_in, username, password, driver_in, port_in)

        column_list = SQL.SQLGetColumnNames(open_con, "Order_Menu")
        open_con = SQL.SQLCon(server_in, database_in, username, password, driver_in, port_in)

        row_info_return = SQL.SQLSearchMultipleRow(open_con, "Order_Menu", "ID", row_to_edit)
        row_info_return = Data_Transforms.SplitAndCleanDBReturn(row_info_return)

        ID = row_info_return[0]
        free_stock = row_info_return[10]
        purchase_order = row_info_return[16]

        grid_sizer = wx.FlexGridSizer(5, 5, 10)
        wrapper_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_wrapper_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.info_static_text = wx.StaticText(self, label="Confirm a order has been received:")

        self.free_stock_static_text = wx.StaticText(self, label="Free Stock Amount: ")
        self.free_stock_place_holder_text = wx.StaticText(self, label=free_stock)

        self.purchase_order_static_text = wx.StaticText(self, label="Purchase Order: ")
        self.purchase_order_place_holder_text = wx.StaticText(self, label=purchase_order)

        self.status_static_text = wx.StaticText(self, label="Status: ")
        self.status_confirm_static_text = wx.StaticText(self, label="Order Completed")

        self.order_comments_static_text = wx.StaticText(self, label="Order Comments: ")
        self.order_comments_txt_ctrl = wx.TextCtrl(self, -1, "", size=(200, -1))

        self.commit_btn = wx.Button(self, 0, label="Commit")
        self.commit_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnCommit(event, parent, ID, row_info_return))
        self.cancel_btn = wx.Button(self, 0, label="Cancel")
        self.cancel_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnCancel(event))

        grid_sizer.Add(self.free_stock_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.free_stock_place_holder_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.AddSpacer(5)
        grid_sizer.Add(self.purchase_order_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.purchase_order_place_holder_text, 0, wx.ALIGN_LEFT, 10)

        grid_sizer.Add(self.status_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.status_confirm_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.AddSpacer(5)
        grid_sizer.Add(self.order_comments_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.order_comments_txt_ctrl, 0, wx.ALIGN_LEFT, 10)

        btn_wrapper_sizer.Add(self.commit_btn, 0, wx.ALIGN_RIGHT, 10)
        btn_wrapper_sizer.Add(self.cancel_btn, 0, wx.ALIGN_LEFT, 10)

        wrapper_sizer.AddSpacer(10)
        wrapper_sizer.Add(self.info_static_text, 0, wx.ALIGN_LEFT, 10)
        wrapper_sizer.AddSpacer(5)
        wrapper_sizer.Add(grid_sizer, 0, wx.ALIGN_LEFT | wx.ALL, 10)
        wrapper_sizer.AddSpacer(5)
        wrapper_sizer.Add(btn_wrapper_sizer, 0, wx.ALIGN_LEFT | wx.ALL, 10)
        wrapper_sizer.AddSpacer(10)

        main_sizer.AddSpacer(20)
        main_sizer.Add(wrapper_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        main_sizer.AddSpacer(20)

        self.SetSizer(main_sizer)
        main_sizer.Fit(self)

    def OnCommit(self, event, parent, id_to_edit, row_info_return):
        entry_list = [id_to_edit,
                      self.status_confirm_static_text.GetLabel(),
                      row_info_return[2],
                      row_info_return[3],
                      row_info_return[4],
                      row_info_return[5],
                      row_info_return[6],
                      row_info_return[7],
                      row_info_return[8],
                      row_info_return[9],
                      row_info_return[10],
                      row_info_return[11],
                      row_info_return[12],
                      row_info_return[13],
                      self.order_comments_txt_ctrl.GetValue(),
                      row_info_return[15],
                      row_info_return[16],
                      row_info_return[17]]

        qty = row_info_return[10]
        project_name = row_info_return[3]
        project_name = project_name.lstrip().rstrip()

        conn_read = Read_And_Write_Files.Read_File('data_conn.tuk')
        server_in = conn_read[0]
        database_in = conn_read[1]
        port_in = conn_read[2]
        driver_in = conn_read[3]

        # Read current user info
        user_read = Read_And_Write_Files.Read_File('user.tuk')
        username = user_read[0]
        password = user_read[1]

        open_con = SQL.SQLCon(server_in, database_in, username, password, driver_in, port_in)
        column_list = SQL.SQLGetColumnNames(open_con, "Order_Menu")

        SQL.SQLUpdateEntry(open_con, "Order_Menu", id_to_edit, column_list, entry_list)

        product_model = row_info_return[6]
        product_model = product_model.lstrip().rstrip()

        id_return = SQL.SQLSearchColumnSingleEntry(open_con, "Products", "ID", "model", product_model)
        id_return = Data_Transforms.TransformRowToList(id_return)

        row_info_return = SQL.SQLSearchMultipleRow(open_con, "Products", "ID", id_return[0])
        row_info_return = Data_Transforms.SplitAndCleanDBReturn(row_info_return)

        project_stock = int(row_info_return[9]) + int(qty)

        project_stock = str(project_stock)

        total_stock = int(row_info_return[8]) + int(qty)

        total_stock = str(total_stock)

        entry_list = [id_return[0],
                      row_info_return[1],
                      row_info_return[2],
                      row_info_return[3],
                      row_info_return[4],
                      row_info_return[5],
                      row_info_return[6],
                      row_info_return[7],
                      total_stock,
                      project_stock,
                      row_info_return[10],
                      row_info_return[11]]

        column_list = SQL.SQLGetColumnNames(open_con, "Products")
        SQL.SQLUpdateEntry(open_con, "Products", id_return[0], column_list, entry_list)

        # -----------------------------------------------------------------------------------------------------

        # -----------------------------------------------------------------------------------------------------



        project_code_return = SQL.SQLSearchColumnSingleEntry(open_con,
                                                             "Projects",
                                                             "project_code",
                                                             "name",
                                                             project_name)
        # Obtain product cost
        cost = SQL.SQLSearchColumnSingleEntry(open_con,
                                              "Products",
                                              "price_ex_vat",
                                              "model",
                                              product_model)
        # pass code from list into variable and then clean
        project_code_return = project_code_return[0].lstrip().rstrip()
        cost = Data_Transforms.TransformRowToList(cost)
        cost = cost[0]
        # ------------------------------------------------------------------------------
        # Open connection to sub database and run search for product
        # ------------------------------------------------------------------------------
        conn_read = Read_And_Write_Files.Read_File('data_conn.tuk')
        server_in = conn_read[0]
        database_in = 'Sub_DB_' + project_code_return
        port_in = conn_read[2]
        driver_in = conn_read[3]

        # Read current user info
        user_read = Read_And_Write_Files.Read_File('user.tuk')
        username = user_read[0]
        password = user_read[1]
        # open connection to sub database
        open_con = SQL.SQLCon(server_in, database_in, username, password, driver_in, port_in)
        product_check = SQL.SQLSearchColumnSingleEntry(open_con, "project_stock", "model", "model", product_model)
        # ------------------------------------------------------------------------------
        # if check to see if the product is already in the project's database, if == none then we run insert!
        # ------------------------------------------------------------------------------
        if product_check == None:
            # ------------------------------------------------------------------------------
            # Insert product into sub database
            # ------------------------------------------------------------------------------
            ID = SQL.SQLGenerateNewID(open_con, "project_stock")
            cost = int(cost)
            cost = cost * int(project_stock)
            insert_list = [ID,
                           product_model,
                           project_stock,
                           project_stock,
                           '0',
                           cost]

            # need to check insert list against names in the database
            insert_list = Data_Transforms.InsertListFillNull(insert_list)
            SQL.SQLInsertInto(open_con, username, "project_stock", insert_list)
            # -----------------------------------------------------------------------------

        elif product_check != None:
            # ------------------------------------------------------------------------------
            # Edit product into sub database
            # ------------------------------------------------------------------------------
            column_list = SQL.SQLGetColumnNames(open_con, "project_stock")
            search_result = SQL.SQLSearchColumnMutipleEntry(open_con,
                                                            username,
                                                            "project_stock",
                                                            product_model,
                                                            column_list)
            search_result = Data_Transforms.SplitAndCleanDBReturn(search_result)
            cost = int(cost)
            cost = cost * int(project_stock)
            sub_cost = cost + int(search_result[5])
            total_qty = int(project_stock) + int(search_result[2])
            internal_held_qty = int(project_stock) + int(search_result[3])

            entry_list = [search_result[0],
                          search_result[1],
                          total_qty,
                          internal_held_qty,
                          search_result[4],
                          sub_cost]

            # need to check insert list against names in the database
            insert_list = Data_Transforms.InsertListFillNull(entry_list)
            SQL.SQLUpdateEntry(open_con, "project_stock", search_result[0], column_list, entry_list)

            # ------------------------------------------------------------------------------
            # Update free stock list in the project table
            # ------------------------------------------------------------------------------
            # Need to updated free stock list in the project table
            database_in = conn_read[1]
            # Open connection to main database
            open_con = SQL.SQLCon(server_in, database_in, username, password, driver_in, port_in)
            # Get column names
            column_list = SQL.SQLGetColumnNames(open_con, "Products")
            # Get all of the project information
            search_result = SQL.SQLSearchColumnMutipleEntry(open_con, username, "Products", product_model,
                                                            column_list)
            search_result = Data_Transforms.SplitAndCleanDBReturn(search_result)
            search_result = Data_Transforms.TransformRowToList(search_result)
            project_stock_qty = int(search_result[9]) + int(project_stock)
            free_stock_qty = int(search_result[10]) - int(project_stock)
            entry_list = [search_result[0],
                          search_result[1],
                          search_result[2],
                          search_result[3],
                          search_result[4],
                          search_result[5],
                          search_result[6],
                          search_result[7],
                          search_result[8],
                          project_stock_qty,
                          free_stock_qty,
                          search_result[11]]

            SQL.SQLUpdateEntry(open_con, "Products", search_result[0], column_list, entry_list)


        GUI.OrderMenuTab.OnSearch(parent, event)

        self.EndModal(True)

    def OnCancel(self, event):
        self.EndModal(True)



class NoteOrderReceivedFreeStock(wx.Dialog):
    def __init__(self, parent, title, row_to_edit):
        super(NoteOrderReceivedFreeStock, self).__init__(parent, title=title, size=(600, 300))

        conn_read = Read_And_Write_Files.Read_File('data_conn.tuk')
        server_in = conn_read[0]
        database_in = conn_read[1]
        port_in = conn_read[2]
        driver_in = conn_read[3]

        # Read current user info
        user_read = Read_And_Write_Files.Read_File('user.tuk')
        username = user_read[0]
        password = user_read[1]

        open_con = SQL.SQLCon(server_in, database_in, username, password, driver_in, port_in)

        column_list = SQL.SQLGetColumnNames(open_con, "Order_Menu")
        open_con = SQL.SQLCon(server_in, database_in, username, password, driver_in, port_in)

        row_info_return = SQL.SQLSearchMultipleRow(open_con, "Order_Menu", "ID", row_to_edit)
        row_info_return = Data_Transforms.SplitAndCleanDBReturn(row_info_return)

        ID = row_info_return[0]
        free_stock = row_info_return[10]
        purchase_order = row_info_return[16]

        grid_sizer = wx.FlexGridSizer(5, 5, 10)
        wrapper_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_wrapper_sizer = wx.BoxSizer(wx.HORIZONTAL)


        self.info_static_text = wx.StaticText(self, label="Confirm a order has been received:")

        self.free_stock_static_text = wx.StaticText(self, label="Free Stock Amount: ")
        self.free_stock_place_holder_text = wx.StaticText(self, label=free_stock)

        self.purchase_order_static_text = wx.StaticText(self, label="Purchase Order: ")
        self.purchase_order_place_holder_text = wx.StaticText(self, label=purchase_order)

        self.status_static_text = wx.StaticText(self, label="Status: ")
        self.status_confirm_static_text = wx.StaticText(self, label="Order Completed")

        self.order_comments_static_text = wx.StaticText(self, label="Order Comments: ")
        self.order_comments_txt_ctrl = wx.TextCtrl(self, -1, "", size=(200, -1))

        self.commit_btn = wx.Button(self, 0, label="Commit")
        self.commit_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnCommit(event, parent, ID, row_info_return))
        self.cancel_btn = wx.Button(self, 0, label="Cancel")
        self.cancel_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnCancel(event))

        grid_sizer.Add(self.free_stock_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.free_stock_place_holder_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.AddSpacer(5)
        grid_sizer.Add(self.purchase_order_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.purchase_order_place_holder_text, 0, wx.ALIGN_LEFT, 10)

        grid_sizer.Add(self.status_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.status_confirm_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.AddSpacer(5)
        grid_sizer.Add(self.order_comments_static_text, 0, wx.ALIGN_LEFT, 10)
        grid_sizer.Add(self.order_comments_txt_ctrl, 0, wx.ALIGN_LEFT, 10)

        btn_wrapper_sizer.Add(self.commit_btn, 0, wx.ALIGN_RIGHT, 10)
        btn_wrapper_sizer.Add(self.cancel_btn, 0, wx.ALIGN_LEFT, 10)

        wrapper_sizer.AddSpacer(10)
        wrapper_sizer.Add(self.info_static_text, 0, wx.ALIGN_LEFT, 10)
        wrapper_sizer.AddSpacer(5)
        wrapper_sizer.Add(grid_sizer, 0, wx.ALIGN_LEFT | wx.ALL, 10)
        wrapper_sizer.AddSpacer(5)
        wrapper_sizer.Add(btn_wrapper_sizer, 0, wx.ALIGN_LEFT | wx.ALL, 10)
        wrapper_sizer.AddSpacer(10)

        main_sizer.AddSpacer(20)
        main_sizer.Add(wrapper_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        main_sizer.AddSpacer(20)

        self.SetSizer(main_sizer)
        main_sizer.Fit(self)

    def OnCommit(self, event, parent, id_to_edit, row_info_return):
        entry_list = [id_to_edit,
                      self.status_confirm_static_text.GetLabel(),
                      row_info_return[2],
                      row_info_return[3],
                      row_info_return[4],
                      row_info_return[5],
                      row_info_return[6],
                      row_info_return[7],
                      row_info_return[8],
                      row_info_return[9],
                      row_info_return[10],
                      row_info_return[11],
                      row_info_return[12],
                      row_info_return[13],
                      self.order_comments_txt_ctrl.GetValue(),
                      row_info_return[15],
                      row_info_return[16],
                      row_info_return[17]]

        qty = row_info_return[10]

        conn_read = Read_And_Write_Files.Read_File('data_conn.tuk')
        server_in = conn_read[0]
        database_in = conn_read[1]
        port_in = conn_read[2]
        driver_in = conn_read[3]

        # Read current user info
        user_read = Read_And_Write_Files.Read_File('user.tuk')
        username = user_read[0]
        password = user_read[1]

        open_con = SQL.SQLCon(server_in, database_in, username, password, driver_in, port_in)
        column_list = SQL.SQLGetColumnNames(open_con, "Order_Menu")

        SQL.SQLUpdateEntry(open_con, "Order_Menu", id_to_edit, column_list, entry_list)

        model = row_info_return[6]
        model = model.lstrip().rstrip()

        id_return = SQL.SQLSearchColumnSingleEntry(open_con, "Products", "ID", "model", model)
        id_return = Data_Transforms.TransformRowToList(id_return)

        row_info_return = SQL.SQLSearchMultipleRow(open_con, "Products", "ID", id_return[0])
        row_info_return = Data_Transforms.SplitAndCleanDBReturn(row_info_return)

        free_stock = int(row_info_return[10]) + int(qty)

        free_stock = str(free_stock)

        total_stock = int(row_info_return[8]) + int(qty)

        total_stock = str(total_stock)

        entry_list = [id_return[0],
                      row_info_return[1],
                      row_info_return[2],
                      row_info_return[3],
                      row_info_return[4],
                      row_info_return[5],
                      row_info_return[6],
                      row_info_return[7],
                      total_stock,
                      row_info_return[9],
                      free_stock,
                      row_info_return[11]]

        column_list = SQL.SQLGetColumnNames(open_con, "Products")
        SQL.SQLUpdateEntry(open_con, "Products", id_return[0], column_list, entry_list)

        GUI.OrderMenuTab.OnSearch(parent, event)

        self.EndModal(True)

    def OnCancel(self, event):
        self.EndModal(True)




# --------------------------------------------------------------------------------------------
# General Modals
# --------------------------------------------------------------------------------------------

class RemoveDialog(wx.Dialog):
    def __init__(self, parent, title, table, what_to_remove, id_to_remove):
        super(RemoveDialog, self).__init__(parent, title=title, size=(600, 300))
        # ------------------------------------------------------------------------------------
        # GUI for the modal
        # ------------------------------------------------------------------------------------
        removal_text = ("Would you like to remove " + str(what_to_remove) + " from " + table)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        wrapper_sizer = wx.BoxSizer(wx.VERTICAL)
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.removal_static_text = wx.StaticText(self, label=removal_text)
        self.yes_btn = wx.Button(self, 0, label="Yes")
        self.yes_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnYes(event, table, id_to_remove, parent))
        self.no_btn = wx.Button(self, 0, label="No")
        self.no_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnNo(event))


        wrapper_sizer.AddSpacer(5)
        wrapper_sizer.Add(self.removal_static_text, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        wrapper_sizer.AddSpacer(5)

        button_sizer.Add(self.yes_btn, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        button_sizer.AddSpacer(5)
        button_sizer.Add(self.no_btn, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        main_sizer.AddSpacer(10)
        main_sizer.Add(wrapper_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        main_sizer.AddSpacer(5)
        main_sizer.Add(button_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        main_sizer.AddSpacer(10)

        self.SetSizer(main_sizer)
        main_sizer.Fit(self)

    # ------------------------------------------------------------------------------------
    # Yes function bound to button
    # ------------------------------------------------------------------------------------
    def OnYes(self, event, table, id_to_remove, parent):
        # read database local file
        conn_read = Read_And_Write_Files.Read_File('data_conn.tuk')
        server_in = conn_read[0]
        database_in = conn_read[1]
        port_in = conn_read[2]
        driver_in = conn_read[3]
        # Read current user info
        user_read = Read_And_Write_Files.Read_File('user.tuk')
        username = user_read[0]
        password = user_read[1]
        # open connection
        open_con = SQL.SQLCon(server_in, database_in, username, password, driver_in, port_in)

        # --------------------------------------------------------------------------------------------
        # Remove project sub database
        # --------------------------------------------------------------------------------------------
        if table == "Projects":
            try:
                # Get project code which the sub database use as there name
                project = SQL.SQLSearchColumnSingleEntry(open_con, "Projects", "project_code", "ID", id_to_remove)
                project = str(project).split(',')
                project = project[0].replace('(', "").replace("'", "")

                # use master for auto commit statement to drop database, this is done in the first as this is more
                # likely  to fail
                open_con = SQL.SQLConAutoCommit(server_in, "master", username, password, driver_in, port_in)
                SQL.SQLRemoveProjectDatabase(open_con, project)
                # have to re-open connection as drop database kills all first
                open_con = SQL.SQLCon(server_in, database_in, username, password, driver_in, port_in)
                SQL.SQLRemove(open_con, table, "ID", id_to_remove)
            except:
                ShowMessageDlg(self, "Failed to remove project " + project + " as it is currently in use.", "Error"
                               , wx.OK | wx.CANCEL | wx.ICON_QUESTION)

        else:
            SQL.SQLRemove(open_con, table, "ID", id_to_remove)


        self.EndModal(True)
        # run search so the list updates
        parent.OnSearch(event)
    # ------------------------------------------------------------------------------------
    # No function bound to button
    # ------------------------------------------------------------------------------------
    def OnNo(self, event):
        self.EndModal(True)

class FilterDialog(wx.Dialog):
    def __init__(self, parent, title):
        super(FilterDialog, self).__init__(parent, title=title, size=(600, 300))

