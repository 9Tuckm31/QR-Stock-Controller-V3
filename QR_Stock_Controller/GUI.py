
import Modals
import wx
import Read_And_Write_Files
import Object_List_View_Builder
import SQL
from ObjectListView import ObjectListView, ColumnDefn

########################################################################################################################
# The TabBar class, using the note book function we create the frame for multiple pages
########################################################################################################################
class TabBar(wx.Notebook):

       #----------------------------------------------------------------------
       def __init__(self, parent):
           wx.Notebook.__init__(self, parent, id=wx.ID_ANY, style=
                                wx.BK_DEFAULT
                                #wx.BK_TOP
                                #wx.BK_BOTTOM |
                                #wx.BK_LEFT |
                                #wx.BK_RIGHT
                                )

           # Create the tabs and add them to the panel
           customers_tab = CustomersTab(self)
           projects_tab = ProjectsTab(self)
           products_tab = ProductsTab(self)
           stock_adjustment_tab = StockAdjustmentTab(self)
           order_menu_tab = OrderMenuTab(self)
           qr_code_tab = QrCodeTab(self)

           # Create the pages of the individual tabs
           self.AddPage(customers_tab, "Customers")
           self.AddPage(projects_tab, "Projects")
           self.AddPage(products_tab, "Products")
           self.AddPage(stock_adjustment_tab, "Stock Adjustment")
           self.AddPage(order_menu_tab, "Order Menu")
           self.AddPage(qr_code_tab, "QR Code Generator")


           # Events that trigger when changing tabs. Im not using this at the moment this is a hang over from some
           # Test code i was using. May have a use for them later for displaying messages when certain action are not
           # completed in another tab!
           self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, lambda event: self.OnPageChanged(event,
                                                                                    parent,projects_tab
                                                                                    ))

           self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, lambda event: self.OnPageChanging(event, parent))




       def OnPageChanged(self, event, parent, projects_tab):
           old = event.GetOldSelection()
           new = event.GetSelection()
           sel = self.GetSelection()
           print ('OnPageChanged,  old:%d, new:%d, sel:%d\n' % (old, new, sel))

           event.Skip()

       def OnPageChanging(self, event, parent):
           old = event.GetOldSelection()
           new = event.GetSelection()
           sel = self.GetSelection()
           print ('OnPageChanging, old:%d, new:%d, sel:%d\n' % (old, new, sel))

           event.Skip()

########################################################################################################################
# The following classes create the layout for each tab page
########################################################################################################################
class CustomersTab(wx.Panel):


    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # --------------------------------------------------------------------------------------------
        # Create the size's for the tab page
        # --------------------------------------------------------------------------------------------
        customers_tab_main_sizer = wx.BoxSizer(wx.VERTICAL)
        customers_tab_option_btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        customers_tab_filter_btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        customers_tab_list_sizer = wx.BoxSizer(wx.HORIZONTAL)


        # --------------------------------------------------------------------------------------------
        # populate the first sizer with widgets
        # --------------------------------------------------------------------------------------------
        # Add new customer to the list -> use this button to open a modal that will input information
        # and create a new entry in the data base
        self.customer_add_btn = wx.Button(self, -1, "Add Customer")
        self.customer_add_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnAddCustomer(event))
        # Edit customer info -> open a modal that will allow the user to edit the customers information
        # a then re-write the entry in the data base
        self.customer_edit_btn = wx.Button(self, -1, "Edit Customer")
        self.customer_edit_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnEditCustomer(event))
        # Delete customer -> open a modal that will allow the user to remove the customer from the data
        # base
        self.customer_delete_btn = wx.Button(self, -1, "Remove Customer")
        self.customer_delete_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnRemoveCustomer(event))
        # Add the widgets to the sizer
        customers_tab_option_btn_sizer.Add(self.customer_add_btn, 0, wx.ALIGN_CENTER, 10)
        customers_tab_option_btn_sizer.Add(self.customer_edit_btn, 0, wx.ALIGN_CENTER, 10)
        customers_tab_option_btn_sizer.Add(self.customer_delete_btn, 0, wx.ALIGN_CENTER, 10)
        # --------------------------------------------------------------------------------------------
        # populate the second sizer with widgets
        # --------------------------------------------------------------------------------------------
        # Will bring up modal that will have more advanced query options for the user to select from
        # for advanced searching
        self.customer_filter_options_btn = wx.Button(self, -1, "Filter Options")
        self.customer_filter_options_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnFilterOptions(event))
        # Will run a basic SQL query based on the information in the text control
        self.customer_filter_search_btn = wx.Button(self, -1, "Search")
        self.customer_filter_search_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnSearch(event))
        self.customer_filter_text_ctrl = wx.TextCtrl(self, -1, "", size=(175, -1))
        # Will provide feed back on query
        self.customer_filter_feedback_text = wx.StaticText(self, -1, "Filter feedback information will appear here", (20, 20))

        # Add the widgets to the sizer
        customers_tab_filter_btn_sizer.Add(self.customer_filter_options_btn, 0, wx.ALIGN_CENTER, 10)
        customers_tab_filter_btn_sizer.Add(self.customer_filter_search_btn, 0, wx.ALIGN_CENTER, 10)
        customers_tab_filter_btn_sizer.Add(self.customer_filter_text_ctrl, 0, wx.ALIGN_CENTER, 10)
        customers_tab_filter_btn_sizer.AddSpacer(20)
        customers_tab_filter_btn_sizer.Add(self.customer_filter_feedback_text, 0, wx.ALIGN_CENTER, 10)

        # --------------------------------------------------------------------------------------------
        # populate the third sizer with widgets
        # --------------------------------------------------------------------------------------------
        # Create the customer object list view
        self.customer_list_view = ObjectListView(self, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.customer_list_view.Bind(wx.EVT_LEFT_DCLICK, lambda event: self.OnDoubleClick(event))
        customers_tab_list_sizer.Add(self.customer_list_view, 1, wx.EXPAND)

        # --------------------------------------------------------------------------------------------
        # populate the main sizer with the sub sizer
        # --------------------------------------------------------------------------------------------
        customers_tab_main_sizer.Add(customers_tab_option_btn_sizer, 0, wx.ALL, 1)
        customers_tab_main_sizer.Add(customers_tab_filter_btn_sizer, 0, wx.ALL, 1)
        customers_tab_main_sizer.Add(customers_tab_list_sizer, 1, wx.EXPAND, 5)
        Object_List_View_Builder.SetColumnsCustomers(self.customer_list_view)
        self.SetSizerAndFit(customers_tab_main_sizer)

    def OnAddCustomer(self, event):
        Modals.AddCustomerDialog(self,'Add A New Customer To The Database!').ShowModal()

    def OnEditCustomer(self, event):
        row_to_edit = self.customer_list_view.GetFocusedRow()
        if row_to_edit == -1:
            pass

        else:
            id_to_edit = self.customer_list_view.GetItemText(row_to_edit, 0)
            Modals.EditCustomerDialog(self,  'Edit Existing Customer In The database!', id_to_edit).ShowModal()

    def OnRemoveCustomer(self, event):
        row_to_remove = self.customer_list_view.GetFocusedRow()
        if row_to_remove == -1:
            pass

        else:
            what_to_remove = self.customer_list_view.GetItemText(row_to_remove, 1)
            id_to_remove = self.customer_list_view.GetItemText(row_to_remove, 0)
            Modals.RemoveDialog(self,  'Remove A Customer From The Database!', "Customers",what_to_remove, id_to_remove).ShowModal()

    def OnFilterOptions(self, event):
        Modals.FilterDialog(self,  'Filter Options').ShowModal()

    def OnDoubleClick(self, event):
        double_click_edit = self.OnEditCustomer(event)

    ###########################################################################################################
    # Function for searching this table in the data base
    ###########################################################################################################
    def OnSearch(self, event):
        # Read database connection info
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
            # Get table column names
            column_list = SQL.SQLGetColumnNames(open_con, "Customers")
            # Check to see if we should search all or a for a value
            if self.customer_filter_text_ctrl.GetValue() == "":
                # Search All
                search_result = SQL.SQLSearchAll(open_con, username, "Customers", self.customer_filter_text_ctrl.GetValue(), "Search All")
                # Update table with return from database
                CustomersTab.UpdateDisplay(self, search_result)

            else:
                # Search for a value
                search_result = SQL.SQLSearchColumnMutipleEntry(open_con, username, "Customers", self.customer_filter_text_ctrl.GetValue(), column_list)
                # Update table with return from database
                CustomersTab.UpdateDisplay(self, search_result)


        except:
            # Error message
            Modals.ShowMessageDlg(self, "Failed to access the data base, please check with your system admin.", "Error"
                                  , wx.OK | wx.CANCEL | wx.ICON_QUESTION)

    ###########################################################################################################
    # Update the rows in the table from information in the database
    ###########################################################################################################
    def UpdateDisplay(self, entry_list):
        # Create a list to be inserted into the table
        self.construction_list = []
        for row in entry_list:
            # Split the tuple returned from the data base into individual values
            build_list = str(row).split(',')
            ID = build_list[0].replace('(', "").replace("'", "")
            Name = build_list[1].replace("'", "")
            Staus = build_list[2].replace("'", "")
            Balance = build_list[3].replace("'", "")
            Contact = build_list[4].replace("'", "")
            Email = build_list[5].replace("'", "")
            Telephone = build_list[6].replace("'", "")
            Mobile = build_list[7].replace("'", "")
            Project = build_list[8].replace(')', "").replace("'", "")
            # Create the object that will build the list for the table
            self.construction_list.append(Object_List_View_Builder.CustomersRowBuilder(ID,
                                                                Name,
                                                                Staus,
                                                                Balance,
                                                                Contact,
                                                                Email,
                                                                Telephone,
                                                                Mobile,
                                                                Project))
        # Set the current object list for the table
        self.customer_list_view.SetObjects(self.construction_list)

class ProjectsTab(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # --------------------------------------------------------------------------------------------
        # Create the size's for the tab page
        # --------------------------------------------------------------------------------------------
        project_tab_main_sizer = wx.BoxSizer(wx.VERTICAL)
        project_tab_option_btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        project_tab_filter_btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        project_tab_list_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # --------------------------------------------------------------------------------------------
        # populate the first sizer with widgets
        # --------------------------------------------------------------------------------------------
        # Add new project to the list -> use this button to open a modal that will input information
        # and create a new entry in the data base
        self.project_add_btn = wx.Button(self, -1, "Add Project")
        self.project_add_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnAddProject(event))
        # Edit project info -> open a modal that will allow the user to edit the customers information
        # a then re-write the entry in the data base
        self.project_edit_btn = wx.Button(self, -1, "Edit Project")
        self.project_edit_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnEditProject(event))
        # Delete project -> open a modal that will allow the user to remove the customer from the data
        # base
        self.project_delete_btn = wx.Button(self, -1, "Remove Project")
        self.project_delete_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnRemoveProject(event))
        # Add the widgets to the sizer
        project_tab_option_btn_sizer.Add(self.project_add_btn, 0, wx.ALIGN_CENTER, 10)
        project_tab_option_btn_sizer.Add(self.project_edit_btn, 0, wx.ALIGN_CENTER, 10)
        project_tab_option_btn_sizer.Add(self.project_delete_btn, 0, wx.ALIGN_CENTER, 10)
        # --------------------------------------------------------------------------------------------
        # populate the second sizer with widgets
        # --------------------------------------------------------------------------------------------
        # Will bring up modal that will have more advanced query options for the user to select from
        # for advanced searching
        self.project_filter_options_btn = wx.Button(self, -1, "Filter Options")
        self.project_filter_options_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnFilterOptions(event))
        # Will run a basic SQL query based on the information in the text control
        self.project_filter_search_btn = wx.Button(self, -1, "Search")
        self.project_filter_search_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnSearch(event))
        self.project_filter_text_ctrl = wx.TextCtrl(self, -1, "", size=(175, -1))
        # Will provide feed back on query
        self.project_filter_feedback_text = wx.StaticText(self, -1, "Filter feedback information will appear here", (20, 20))

        # Add the widgets to the sizer
        project_tab_filter_btn_sizer.Add(self.project_filter_options_btn, 0, wx.ALIGN_CENTER, 10)
        project_tab_filter_btn_sizer.Add(self.project_filter_search_btn, 0, wx.ALIGN_CENTER, 10)
        project_tab_filter_btn_sizer.Add(self.project_filter_text_ctrl, 0, wx.ALIGN_CENTER, 10)
        project_tab_filter_btn_sizer.AddSpacer(20)
        project_tab_filter_btn_sizer.Add(self.project_filter_feedback_text, 0, wx.ALIGN_CENTER, 10)

        # --------------------------------------------------------------------------------------------
        # populate the third sizer with widgets
        # --------------------------------------------------------------------------------------------
        # Create the customer object list view
        self.project_list_view = ObjectListView(self, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.project_list_view.Bind(wx.EVT_LEFT_DCLICK, lambda event: self.OnDoubleClick(event))
        project_tab_list_sizer.Add(self.project_list_view, 1, wx.EXPAND)

        # --------------------------------------------------------------------------------------------
        # populate the main sizer with the sub sizer
        # --------------------------------------------------------------------------------------------
        project_tab_main_sizer.Add(project_tab_option_btn_sizer, 0, wx.ALL, 1)
        project_tab_main_sizer.Add(project_tab_filter_btn_sizer, 0, wx.ALL, 1)
        project_tab_main_sizer.Add(project_tab_list_sizer, 1, wx.EXPAND, 5)
        # --------------------------------------------------------------------------------------------
        Object_List_View_Builder.SetColumnsProjects(self.project_list_view)
        # --------------------------------------------------------------------------------------------
        self.SetSizerAndFit(project_tab_main_sizer)

    def OnAddProject(self, event):
        Modals.AddProjectDialog(self,'Add A New Project To The Database!', "", 0).ShowModal()

    def OnEditProject(self, event):
        row_to_edit = self.project_list_view.GetFocusedRow()
        if row_to_edit == -1:
            pass

        else:
            id_to_edit = self.project_list_view.GetItemText(row_to_edit, 0)
            Modals.EditProjectDialog(self,  'Edit Existing Project In The database!', id_to_edit).ShowModal()

    def OnRemoveProject(self, event):
        row_to_remove = self.project_list_view.GetFocusedRow()
        if row_to_remove == -1:
            pass

        else:
            what_to_remove = self.project_list_view.GetItemText(row_to_remove, 2)
            id_to_remove = self.project_list_view.GetItemText(row_to_remove, 0)
            Modals.RemoveDialog(self, 'Remove A Project From The Database!', "Projects", what_to_remove,
                                id_to_remove).ShowModal()

    def OnFilterOptions(self, event):
        Modals.FilterDialog(self,  'Filter Options').ShowModal()

    def OnDoubleClick(self, event):
        double_click_edit = self.OnEditProject(event)

    # --------------------------------------------------------------------------------------------
    # Function for searching this table in the data base
    # --------------------------------------------------------------------------------------------
    def OnSearch(self, event):
        # Read database connection info
        conn_read = Read_And_Write_Files.Read_File('data_conn.tuk')
        server_in = conn_read[0]
        database_in = conn_read[1]
        port_in = conn_read[2]
        driver_in = conn_read[3]

        # Read current user info
        user_read = Read_And_Write_Files.Read_File('user.tuk')
        username = user_read[0]
        password = user_read[1]

        #try:
            # Open connection
        open_con = SQL.SQLCon(server_in, database_in, username, password, driver_in, port_in)
            # Get table column names
        column_list = SQL.SQLGetColumnNames(open_con, "Projects")
            # Check to see if we should search all or a for a value
        if self.project_filter_text_ctrl.GetValue() == "":
                # Search All
            search_result = SQL.SQLSearchAll(open_con, username, "Projects", self.project_filter_text_ctrl.GetValue(), "Search All")
                # Update table with return from database
            ProjectsTab.UpdateDisplay(self, search_result)

        else:
                # Search for a value
            search_result = SQL.SQLSearchColumnMutipleEntry(open_con, username, "Projects", self.project_filter_text_ctrl.GetValue(), column_list)
                # Update table with return from database
            ProjectsTab.UpdateDisplay(self, search_result)


        #except:
            # Error message
            Modals.ShowMessageDlg(self, "Failed to access the data base, please check with your system admin.", "Error",
                                wx.OK | wx.CANCEL | wx.ICON_QUESTION)

    # --------------------------------------------------------------------------------------------
    # Update the rows in the table from information in the database
    # --------------------------------------------------------------------------------------------
    def UpdateDisplay(self, entry_list):
        # Create a list to be inserted into the table
        self.construction_list = []
        for row in entry_list:
            # Split the tuple returned from the data base into individual values
            build_list = str(row).split(',')
            ID = build_list[0].replace('(', "").replace("'", "")
            ProjectCode = build_list[1].replace("'", "")
            Name = build_list[2].replace("'", "")
            Status = build_list[3].replace("'", "")
            Customer = build_list[4].replace(')', "").replace("'", "")

            # Create the object that will build the list for the table
            self.construction_list.append(Object_List_View_Builder.ProjectsRowBuilder(ID,
                                                                                       ProjectCode,
                                                                                       Name,
                                                                                       Status,
                                                                                       Customer))
        # Set the current object list for the table
        self.project_list_view.SetObjects(self.construction_list)

class ProductsTab(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # --------------------------------------------------------------------------------------------
        # Create the size's for the tab page
        # --------------------------------------------------------------------------------------------
        product_tab_main_sizer = wx.BoxSizer(wx.VERTICAL)
        product_tab_option_btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        product_tab_filter_btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        product_tab_list_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # --------------------------------------------------------------------------------------------
        # populate the first sizer with widgets
        # --------------------------------------------------------------------------------------------
        # Add new project to the list -> use this button to open a modal that will input information
        # and create a new entry in the data base
        self.product_add_btn = wx.Button(self, -1, "Add Product")
        self.product_add_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnAddProducts(event))
        # Edit project info -> open a modal that will allow the user to edit the customers information
        # a then re-write the entry in the data base
        self.product_edit_btn = wx.Button(self, -1, "Edit Product")
        self.product_edit_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnEditProducts(event))
        # Delete product -> open a modal that will allow the user to remove the customer from the data
        # base
        self.product_delete_btn = wx.Button(self, -1, "Remove Product")
        self.product_delete_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnRemoveProducts(event))
        # Add the widgets to the sizer
        product_tab_option_btn_sizer.Add(self.product_add_btn, 0, wx.ALIGN_CENTER, 10)
        product_tab_option_btn_sizer.Add(self.product_edit_btn, 0, wx.ALIGN_CENTER, 10)
        product_tab_option_btn_sizer.Add(self.product_delete_btn, 0, wx.ALIGN_CENTER, 10)
        # --------------------------------------------------------------------------------------------
        # populate the second sizer with widgets
        # --------------------------------------------------------------------------------------------
        # Will bring up modal that will have more advanced query options for the user to select from
        # for advanced searching
        self.product_filter_options_btn = wx.Button(self, -1, "Filter Options")
        self.product_filter_options_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnFilterOptions(event))
        # Will run a basic SQL query based on the information in the text control
        self.product_filter_search_btn = wx.Button(self, -1, "Search")
        self.product_filter_search_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnSearch(event))
        self.product_filter_text_ctrl = wx.TextCtrl(self, -1, "", size=(175, -1))
        # Will provide feed back on query
        self.product_filter_feedback_text = wx.StaticText(self, -1, "Filter feedback information will appear here",
                                                          (20, 20))

        # Add the widgets to the sizer
        product_tab_filter_btn_sizer.Add(self.product_filter_options_btn, 0, wx.ALIGN_CENTER, 10)
        product_tab_filter_btn_sizer.Add(self.product_filter_search_btn, 0, wx.ALIGN_CENTER, 10)
        product_tab_filter_btn_sizer.Add(self.product_filter_text_ctrl, 0, wx.ALIGN_CENTER, 10)
        product_tab_filter_btn_sizer.AddSpacer(20)
        product_tab_filter_btn_sizer.Add(self.product_filter_feedback_text, 0, wx.ALIGN_CENTER, 10)

        # --------------------------------------------------------------------------------------------
        # populate the third sizer with widgets
        # --------------------------------------------------------------------------------------------
        # Create the product object list view
        self.product_list_view = ObjectListView(self, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.product_list_view.Bind(wx.EVT_LEFT_DCLICK, lambda event: self.OnDoubleClick(event))
        product_tab_list_sizer.Add(self.product_list_view, 1, wx.EXPAND)

        # --------------------------------------------------------------------------------------------
        # populate the main sizer with the sub sizer
        # --------------------------------------------------------------------------------------------
        product_tab_main_sizer.Add(product_tab_option_btn_sizer, 0, wx.ALL, 1)
        product_tab_main_sizer.Add(product_tab_filter_btn_sizer, 0, wx.ALL, 1)
        product_tab_main_sizer.Add(product_tab_list_sizer, 1, wx.EXPAND, 5)
        # --------------------------------------------------------------------------------------------
        Object_List_View_Builder.SetColumnsProducts(self.product_list_view)
        # --------------------------------------------------------------------------------------------
        self.SetSizerAndFit(product_tab_main_sizer)

    def OnAddProducts(self, event):
        Modals.AddProductDialog(self, 'Add A New Product To The Database!').ShowModal()

    def OnEditProducts(self, event):
        row_to_edit = self.product_list_view.GetFocusedRow()
        if row_to_edit == -1:
            pass

        else:
            id_to_edit = self.product_list_view.GetItemText(row_to_edit, 0)
            Modals.EditProductDialog(self, 'Edit Existing Product In The database!',id_to_edit).ShowModal()

    def OnRemoveProducts(self, event):
        row_to_remove = self.product_list_view.GetFocusedRow()
        if row_to_remove == -1:
            pass

        else:
            what_to_remove = self.product_list_view.GetItemText(row_to_remove, 2)
            id_to_remove = self.product_list_view.GetItemText(row_to_remove, 0)
            Modals.RemoveDialog(self, 'Remove A Product From The Database!', "Products", what_to_remove,
                                id_to_remove).ShowModal()

    def OnFilterOptions(self, event):
        Modals.FilterDialog(self,  'Filter Options').ShowModal()

    def OnDoubleClick(self, event):
        double_click_edit = self.OnEditProducts(event)

    # --------------------------------------------------------------------------------------------
    # Function for searching this table in the data base
    # --------------------------------------------------------------------------------------------
    def OnSearch(self, event):
        # Read database connection info
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
            # Get table column names
            column_list = SQL.SQLGetColumnNames(open_con, "Products")
            # Check to see if we should search all or a for a value
            if self.product_filter_text_ctrl.GetValue() == "":
                # Search All
                search_result = SQL.SQLSearchAll(open_con, username, "Products", self.product_filter_text_ctrl.GetValue(), "Search All")
                # Update table with return from database
                ProductsTab.UpdateDisplay(self, search_result)

            else:
                # Search for a value
                search_result = SQL.SQLSearchColumnMutipleEntry(open_con, username, "Products", self.product_filter_text_ctrl.GetValue(), column_list)
                # Update table with return from database
                ProductsTab.UpdateDisplay(self, search_result)


        except:
            # Error message
            Modals.ShowMessageDlg("Failed to access the data base, please check with your system admin.",
                                "Error"
                                , wx.OK | wx.CANCEL | wx.ICON_QUESTION)

    # --------------------------------------------------------------------------------------------
    # Update the rows in the table from information in the database
    # --------------------------------------------------------------------------------------------
    def UpdateDisplay(self, entry_list):
        # Create a list to be inserted into the table
        self.construction_list = []
        for row in entry_list:
            # Split the tuple returned from the data base into individual values
            build_list = str(row).split(',')
            ID = build_list[0].replace('(', "").replace("'", "")
            Brand = build_list[1].replace("'", "")
            Supplider = build_list[2].replace("'", "")
            Model = build_list[3].replace("'", "")
            Company_Code = build_list[4].replace("'", "")
            Description = build_list[5].replace("'", "")
            Color = build_list[6].replace("'", "")
            Unit_Of_Measure = build_list[7].replace("'", "")
            Total_Qty = build_list[8].replace("'", "")
            Project_Qty = build_list[9].replace("'", "")
            Free_Stock_Qty = build_list[10].replace("'", "")
            Price_Ex_Vat = build_list[11].replace(')', "").replace("'", "")
            # Create the object that will build the list for the table
            self.construction_list.append(Object_List_View_Builder.ProductsRowBuilder(ID,
                                                                                      Brand,
                                                                                      Supplider,
                                                                                      Model,
                                                                                      Company_Code,
                                                                                      Description,
                                                                                      Color,
                                                                                      Unit_Of_Measure,
                                                                                      Total_Qty,
                                                                                      Project_Qty,
                                                                                      Free_Stock_Qty,
                                                                                      Price_Ex_Vat
                                                                                      ))
        # Set the current object list for the table
        self.product_list_view.SetObjects(self.construction_list)

class StockAdjustmentTab(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.clicked_project = ""
        self.clicked_product = ""
        # --------------------------------------------------------------------------------------------
        # Create the size's for the tab page
        # --------------------------------------------------------------------------------------------
        stock_adjustment_tab_main_sizer = wx.BoxSizer(wx.VERTICAL)
        stock_adjustment_option_btn_sizer = wx.BoxSizer(wx.HORIZONTAL)

        stock_adjustment_filter_sub_first_sizer = wx.BoxSizer(wx.HORIZONTAL)
        stock_adjustment_filter_sub_second_sizer = wx.BoxSizer(wx.HORIZONTAL)

        stock_adjustment_list_sub_first_sizer = wx.BoxSizer(wx.HORIZONTAL)
        stock_adjustment_list_sub_second_sizer = wx.BoxSizer(wx.HORIZONTAL)


        stock_adjustment_grid_sizer = wx.FlexGridSizer(2, 2, 10, 10)
        stock_adjustment_grid_sizer.AddGrowableRow(1, 1)
        #stock_adjustment_grid_sizer.AddGrowableRow(0, 0)
        stock_adjustment_grid_sizer.AddGrowableCol(1, 1)
        stock_adjustment_grid_sizer.AddGrowableCol(0, 1)


        # --------------------------------------------------------------------------------------------
        # populate the first sizer with widgets
        # --------------------------------------------------------------------------------------------
        # Moves the selected stock from free stock to the project Internal
        self.stock_adjustment_assign_internal_btn = wx.Button(self, -1, "Assign To Project Internal")
        self.stock_adjustment_assign_internal_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnAssignToProjectInternal(event))
        # Moves the selected stock from free stock to the project
        self.stock_adjustment_assign_site_btn = wx.Button(self, -1, "Assign To Project Site")
        self.stock_adjustment_assign_site_btn.Bind(wx.EVT_BUTTON,
                                                       lambda event: self.OnAssignToProjectSite(event))
        # Edit project info -> open a modal that will allow the user to edit the customers information
        # a then re-write the entry in the data base
        self.stock_adjustment_assign_free_stock_btn = wx.Button(self, -1, "Assign To Free Stock")
        self.stock_adjustment_assign_free_stock_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnAssignToProjectFreeStock(event))

        # Add the widgets to the sizer
        stock_adjustment_option_btn_sizer.Add(self.stock_adjustment_assign_internal_btn, 0, wx.ALIGN_CENTER, 10)
        stock_adjustment_option_btn_sizer.Add(self.stock_adjustment_assign_site_btn, 0, wx.ALIGN_CENTER, 10)
        stock_adjustment_option_btn_sizer.Add(self.stock_adjustment_assign_free_stock_btn, 0, wx.ALIGN_CENTER, 10)

        # --------------------------------------------------------------------------------------------
        # populate the second sizer with widgets
        # --------------------------------------------------------------------------------------------
        # Will bring up modal that will have more advanced query options for the user to select from
        # for advanced searching
        self.stock_adjustment_filter_options_first_btn = wx.Button(self, -1, "Filter Options 1")
        self.stock_adjustment_filter_options_first_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnFilterOptions(event))
        # Will run a basic SQL query based on the information in the text control
        self.stock_adjustment_filter_first_search_btn = wx.Button(self, -1, "Search")
        self.stock_adjustment_filter_first_search_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnProjectSearch(event))
        self.stock_adjustment_filter_first_text_ctrl = wx.TextCtrl(self, -1, "", size=(175, -1))
        # Will provide feed back on query


        self.stock_adjustment_filter_options_second_btn = wx.Button(self, -1, "Filter Options 2")
        self.stock_adjustment_filter_options_second_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnFilterOptions(event))
        # Will run a basic SQL query based on the information in the text control
        self.stock_adjustment_filter_second_search_btn = wx.Button(self, -1, "Search")
        self.stock_adjustment_filter_second_search_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnProductSearch(event))
        self.stock_adjustment_filter_second_text_ctrl = wx.TextCtrl(self, -1, "", size=(175, -1))
        # Will provide feed back on query


        # Add the widgets to the first sub sizer
        stock_adjustment_filter_sub_first_sizer.Add(self.stock_adjustment_filter_options_first_btn, 0,  wx.ALIGN_CENTER,
                                                    10)
        stock_adjustment_filter_sub_first_sizer.Add(self.stock_adjustment_filter_first_search_btn, 0,  wx.ALIGN_CENTER,
                                                    10)
        stock_adjustment_filter_sub_first_sizer.Add(self.stock_adjustment_filter_first_text_ctrl, 0,  wx.ALIGN_CENTER,
                                                    10)

        stock_adjustment_filter_sub_second_sizer.Add(self.stock_adjustment_filter_options_second_btn, 0, wx.ALIGN_CENTER,
                                                    10)
        stock_adjustment_filter_sub_second_sizer.Add(self.stock_adjustment_filter_second_search_btn, 0,  wx.ALIGN_CENTER,
                                                    10)
        stock_adjustment_filter_sub_second_sizer.Add(self.stock_adjustment_filter_second_text_ctrl, 0,  wx.ALIGN_CENTER,
                                                    10)
        # --------------------------------------------------------------------------------------------
        # populate the third sizer with widgets
        # --------------------------------------------------------------------------------------------
        # Create the customer object list view
        self.stock_adjustment_project_list_view = ObjectListView(self, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.stock_adjustment_project_list_view.Bind(wx.EVT_LEFT_DCLICK, lambda event: self.OnDoubleClickProject(event))
        self.stock_adjustment_project_list_view.Bind(wx.EVT_LIST_ITEM_FOCUSED, lambda event: self.OnSelectListItem(event, "Project"))

        self.stock_adjustment_product_list_view = ObjectListView(self, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.stock_adjustment_product_list_view.Bind(wx.EVT_LEFT_DCLICK, lambda event: self.OnDoubleClickProduct(event))
        self.stock_adjustment_product_list_view.Bind(wx.EVT_LIST_ITEM_FOCUSED, lambda event: self.OnSelectListItem(event, "Product"))

        stock_adjustment_list_sub_first_sizer.Add(self.stock_adjustment_project_list_view, 1, wx.EXPAND)
        stock_adjustment_list_sub_second_sizer.Add(self.stock_adjustment_product_list_view, 1, wx.EXPAND)

        stock_adjustment_grid_sizer.Add(stock_adjustment_filter_sub_first_sizer, 1, flag=wx.ALL | wx.ALIGN_LEFT)
        stock_adjustment_grid_sizer.Add(stock_adjustment_filter_sub_second_sizer, 1, flag=wx.ALL | wx.ALIGN_LEFT)
        stock_adjustment_grid_sizer.Add(stock_adjustment_list_sub_first_sizer, 1, flag=wx.EXPAND, border=10)
        stock_adjustment_grid_sizer.Add(stock_adjustment_list_sub_second_sizer, 1, flag=wx.EXPAND, border=10)


        # --------------------------------------------------------------------------------------------
        # populate the main sizer with the sub sizer
        # --------------------------------------------------------------------------------------------
        stock_adjustment_tab_main_sizer.Add(stock_adjustment_option_btn_sizer, 0, wx.EXPAND, 10)
        stock_adjustment_tab_main_sizer.Add(stock_adjustment_grid_sizer, 1,wx.EXPAND, 10)


        # --------------------------------------------------------------------------------------------
        Object_List_View_Builder.SetColumnsStockAdjustmentProjects(self.stock_adjustment_project_list_view)
        # --------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------
        Object_List_View_Builder.SetColumnsProducts(self.stock_adjustment_product_list_view)
        # --------------------------------------------------------------------------------------------


        self.SetSizerAndFit(stock_adjustment_tab_main_sizer)

    def OnFilterOptions(self, event):
        Modals.FilterDialog(self,  'Filter Options').ShowModal()

    def OnAssignToProjectInternal(self, event):


        product_selected = self.clicked_product
        project_selected = self.clicked_project

        Modals.AssignToProjectInternal(self, 'Assign Product To Project Internal', product_selected, project_selected).ShowModal()

    def OnAssignToProjectSite(self, event):

        product_selected = self.clicked_product
        project_selected = self.clicked_project

        Modals.AssignToProjectSite(self, 'Assign Product To Project External Site', product_selected, project_selected).ShowModal()

    def OnAssignToProjectFreeStock(self, event):

        product_selected = self.clicked_product
        project_selected = self.clicked_project

        Modals.AssignToProjectFreeStock(self, 'Assign Product To Free Stock', product_selected, project_selected).ShowModal()

    def OnDoubleClickProject(self, event):
        project_selected = self.stock_adjustment_project_list_view.GetFocusedRow()
        if project_selected == -1:
            pass

        else:
            project_selected = self.stock_adjustment_project_list_view.GetItemText(project_selected, 0)
            project_selected.lstrip()
            project_selected.rstrip()
        Modals.ProjectStock(self, 'Project ' + project_selected + ' stock', project_selected).ShowModal()

    def OnDoubleClickProduct(self, event):
        product_selected = self.stock_adjustment_product_list_view.GetFocusedRow()

        Modals.ProductAssign(self, 'Assign Product To Project', product_selected).ShowModal()

    def OnSelectListItem(self, event, table):

        if table == "Project":

            project_selected = self.stock_adjustment_project_list_view.GetFocusedRow()
            project_selected = self.stock_adjustment_project_list_view.GetItemText(project_selected, 1)
            project_selected = project_selected.lstrip()
            project_selected = project_selected.rstrip()
            self.clicked_project = project_selected


        elif table == "Product":
            product_selected = self.stock_adjustment_product_list_view.GetFocusedRow()
            product_selected = self.stock_adjustment_product_list_view.GetItemText(product_selected, 3)
            product_selected = product_selected.lstrip()
            product_selected = product_selected.rstrip()
            self.clicked_product = product_selected

    ###########################################################################################################
    # Function for searching this table in the data base
    ###########################################################################################################
    def OnProjectSearch(self, event):
        # Read database connection info
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
            # Get table column names
            column_list = SQL.SQLGetColumnNames(open_con, "Projects")
            # Check to see if we should search all or a for a value
            if self.stock_adjustment_filter_first_text_ctrl.GetValue() == "":
                # Search All
                search_result = SQL.SQLSearchAll(open_con, username, "Projects", self.stock_adjustment_filter_first_text_ctrl.GetValue(), "Search All")
                # Update table with return from database
                StockAdjustmentTab.UpdateProjectDisplay(self, search_result)

            else:
                # Search for a value
                search_result = SQL.SQLSearchColumnMutipleEntry(open_con, username, "Projects", self.stock_adjustment_filter_first_text_ctrl.GetValue(), column_list)
                # Update table with return from database
                StockAdjustmentTab.UpdateProjectDisplay(self, search_result)


        except:
            # Error message
            Modals.ShowMessageDlg("Failed to access the data base, please check with your system admin.",
                                "Error",
                                wx.OK | wx.CANCEL | wx.ICON_QUESTION)

    ###########################################################################################################
    # Update the rows in the table from information in the database
    ###########################################################################################################
    def UpdateProjectDisplay(self, entry_list):
        # Create a list to be inserted into the table
        self.construction_list = []
        for row in entry_list:
            # Split the tuple returned from the data base into individual values
            build_list = str(row).split(',')
            ProjectCode = build_list[1].replace("'", "")
            Name = build_list[2].replace("'", "")


            # Create the object that will build the list for the table
            self.construction_list.append(Object_List_View_Builder.ProjectsAdjustmentRowBuilder(ProjectCode, Name))
        # Set the current object list for the table
        self.stock_adjustment_project_list_view.SetObjects(self.construction_list)

    ###########################################################################################################
    # Function for searching this table in the data base
    ###########################################################################################################
    def OnProductSearch(self, event):
        # Read database connection info
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
            # Get table column names
            column_list = SQL.SQLGetColumnNames(open_con, "Products")
            # Check to see if we should search all or a for a value
            if self.stock_adjustment_filter_second_text_ctrl.GetValue() == "":
                # Search All
                search_result = SQL.SQLSearchAll(open_con, username, "Products", self.stock_adjustment_filter_second_text_ctrl.GetValue(), "Search All")
                # Update table with return from database
                StockAdjustmentTab.UpdateProductDisplay(self, search_result)

            else:
                # Search for a value
                search_result = SQL.SQLSearchColumnMutipleEntry(open_con, username, "Products", self.stock_adjustment_filter_second_text_ctrl.GetValue(), column_list)
                # Update table with return from database
                StockAdjustmentTab.UpdateProductDisplay(self, search_result)


        except:
            # Error message
            Modals.ShowMessageDlg(self, "Failed to access the data base, please check with your system admin.",
                                "Error"
                                , wx.OK | wx.CANCEL | wx.ICON_QUESTION)

    ###########################################################################################################
    # Update the rows in the table from information in the database
    ###########################################################################################################
    def UpdateProductDisplay(self, entry_list):
        # Create a list to be inserted into the table
        self.construction_list = []
        for row in entry_list:
            # Split the tuple returned from the data base into individual values
            build_list = str(row).split(',')
            ID = build_list[0].replace('(', "").replace("'", "")
            Brand = build_list[1].replace("'", "")
            Supplider = build_list[2].replace("'", "")
            Model = build_list[3].replace("'", "")
            Company_Code = build_list[4].replace("'", "")
            Description = build_list[5].replace("'", "")
            Color = build_list[6].replace("'", "")
            Unit_Of_Measure = build_list[7].replace("'", "")
            Total_Qty = build_list[8].replace("'", "")
            Project_Qty = build_list[9].replace("'", "")
            Free_Stock_Qty = build_list[10].replace("'", "")
            Price_Ex_Vat = build_list[11].replace(')', "").replace("'", "")
            # Create the object that will build the list for the table
            self.construction_list.append(Object_List_View_Builder.ProductsRowBuilder(ID,
                                                                                      Brand,
                                                                                      Supplider,
                                                                                      Model,
                                                                                      Company_Code,
                                                                                      Description,
                                                                                      Color,
                                                                                      Unit_Of_Measure,
                                                                                      Total_Qty,
                                                                                      Project_Qty,
                                                                                      Free_Stock_Qty,
                                                                                      Price_Ex_Vat
                                                                                      ))
            # Set the current object list for the table

        self.stock_adjustment_product_list_view.SetObjects(self.construction_list)

class OrderMenuTab(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # --------------------------------------------------------------------------------------------
        # Create the size's for the tab page
        # --------------------------------------------------------------------------------------------
        order_menu_tab_main_sizer = wx.BoxSizer(wx.VERTICAL)
        order_menu_tab_option_btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        order_menu_tab_filter_btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        order_menu_tab_list_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # --------------------------------------------------------------------------------------------
        # populate the first sizer with widgets
        # --------------------------------------------------------------------------------------------

        self.order_menu_request_btn = wx.Button(self, -1, "Make Order Request")
        self.order_menu_request_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnMakeOrderRequest(event))


        self.order_menu_raise_btn = wx.Button(self, -1, "Confirm Order")
        self.order_menu_raise_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnConfirmOrder(event))

        self.order_menu_received_btn = wx.Button(self, -1, "Note Order Received")
        self.order_menu_received_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnNoteOrderReceived(event))


        # Add the widgets to the sizer
        order_menu_tab_option_btn_sizer.Add(self.order_menu_request_btn, 0, wx.ALIGN_CENTER, 10)
        order_menu_tab_option_btn_sizer.Add(self.order_menu_raise_btn, 0, wx.ALIGN_CENTER, 10)
        order_menu_tab_option_btn_sizer.Add(self.order_menu_received_btn, 0, wx.ALIGN_CENTER, 10)
        # --------------------------------------------------------------------------------------------
        # populate the second sizer with widgets
        # --------------------------------------------------------------------------------------------
        # Will bring up modal that will have more advanced query options for the user to select from
        # for advanced searching
        self.order_menu_filter_options_btn = wx.Button(self, -1, "Filter Options")
        self.order_menu_filter_options_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnFilterOptions(event))
        # Will run a basic SQL query based on the information in the text control
        self.order_menu_filter_search_btn = wx.Button(self, -1, "Search")
        self.order_menu_filter_search_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnSearch(event))
        self.order_menu_btn_filter_text_ctrl = wx.TextCtrl(self, -1, "", size=(175, -1))
        # Will provide feed back on query
        self.order_menu_btn_filter_feedback_text = wx.StaticText(self, -1, "Filter feedback information will appear "
                                                                           "here", (20, 20))

        # Add the widgets to the sizer
        order_menu_tab_filter_btn_sizer.Add(self.order_menu_filter_options_btn, 0, wx.ALIGN_CENTER, 10)
        order_menu_tab_filter_btn_sizer.Add(self.order_menu_filter_search_btn, 0, wx.ALIGN_CENTER, 10)
        order_menu_tab_filter_btn_sizer.Add(self.order_menu_btn_filter_text_ctrl, 0, wx.ALIGN_CENTER, 10)
        order_menu_tab_filter_btn_sizer.AddSpacer(20)
        order_menu_tab_filter_btn_sizer.Add(self.order_menu_btn_filter_feedback_text, 0, wx.ALIGN_CENTER, 10)

        # --------------------------------------------------------------------------------------------
        # populate the third sizer with widgets
        # --------------------------------------------------------------------------------------------
        # Create the customer object list view
        self.order_menu_list_view = ObjectListView(self, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        order_menu_tab_list_sizer.Add(self.order_menu_list_view, 1, wx.EXPAND)

        # --------------------------------------------------------------------------------------------
        # populate the main sizer with the sub sizer
        # --------------------------------------------------------------------------------------------
        order_menu_tab_main_sizer.Add(order_menu_tab_option_btn_sizer, 0, wx.ALL, 1)
        order_menu_tab_main_sizer.Add(order_menu_tab_filter_btn_sizer, 0, wx.ALL, 1)
        order_menu_tab_main_sizer.Add(order_menu_tab_list_sizer, 1, wx.EXPAND, 5)
        # --------------------------------------------------------------------------------------------
        Object_List_View_Builder.SetColumnsOrderMenu(self.order_menu_list_view)
        # --------------------------------------------------------------------------------------------
        self.SetSizerAndFit(order_menu_tab_main_sizer)

    # --------------------------------------------------------------------------------------------
    # Define functions that activate on the user clicking buttons
    # --------------------------------------------------------------------------------------------
    def OnFilterOptions(self, event):
        Modals.FilterDialog(self,  'Filter Options').ShowModal()

    def OnMakeOrderRequest(self, event):
        Modals.MakeOrderRequest(self,  'Make Order Request').ShowModal()

    def OnConfirmOrder(self, event):
        row_to_edit = self.order_menu_list_view.GetFocusedRow()
        if row_to_edit == -1:
            Modals.ShowMessageDlg(self, "Please select a order from the list!.", "Error"
                                  , wx.OK | wx.CANCEL | wx.ICON_QUESTION)

        else:
            id_to_edit = self.order_menu_list_view.GetItemText(row_to_edit, 0)
            Modals.ConfirmOrder(self,  'Confirm Order', id_to_edit).ShowModal()

    def OnNoteOrderReceived(self, event):
        row_to_edit = self.order_menu_list_view.GetFocusedRow()
        if row_to_edit == -1:
            Modals.ShowMessageDlg(self, "Please select a order from the list!.", "Error"
                                  , wx.OK | wx.CANCEL | wx.ICON_QUESTION)

        else:
            project_check = self.order_menu_list_view.GetItemText(row_to_edit, 3).lstrip().rstrip()
            id_to_edit = self.order_menu_list_view.GetItemText(row_to_edit, 0)
            if project_check == "Free Stock":
                Modals.NoteOrderReceivedFreeStock(self, 'Note Free Stock Order Received', id_to_edit).ShowModal()
            else:
                Modals.NoteOrderReceivedProject(self, 'Note Project Order Received', id_to_edit).ShowModal()

    # --------------------------------------------------------------------------------------------
    # Function for searching this table in the data base
    # --------------------------------------------------------------------------------------------
    def OnSearch(self, event):
        # Read database connection info
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
            # Get table column names
            column_list = SQL.SQLGetColumnNames(open_con, "Order_Menu")
            # Check to see if we should search all or a for a value
            if self.order_menu_btn_filter_text_ctrl.GetValue() == "":
                # Search All
                search_result = SQL.SQLSearchAll(open_con, username, "Order_Menu",
                                                    self.order_menu_btn_filter_text_ctrl.GetValue(), "Search All")
                # Update table with return from database
                OrderMenuTab.UpdateDisplay(self, search_result)

            else:
                # Search for a value
                search_result = SQL.SQLSearchColumnMutipleEntry(open_con, username, "Order_Menu",
                                                                self.order_menu_btn_filter_text_ctrl.GetValue(),
                                                                column_list)
                # Update table with return from database
                OrderMenuTab.UpdateDisplay(self, search_result)


        except:
            # Error message
            Modals.ShowMessageDlg(self, "Failed to access the database, please check with your system admin.",
                                  "Error",wx.OK | wx.CANCEL | wx.ICON_QUESTION)

    # --------------------------------------------------------------------------------------------
    # Update the rows in the table from information in the database
    # --------------------------------------------------------------------------------------------
    def UpdateDisplay(self, entry_list):
        # Create a list to be inserted into the table
        self.construction_list = []
        for row in entry_list:
            # Split the tuple returned from the data base into individual values
            build_list = str(row).split(',')
            ID = build_list[0].replace('(', "").replace("'", "")
            Status = build_list[1].replace("'", "")
            Order_Raiser = build_list[2].replace("'", "")
            Project = build_list[3].replace("'", "")
            Supplier = build_list[4].replace("'", "")
            Brand = build_list[5].replace("'", "")
            Model = build_list[6].replace("'", "")
            Company_Code = build_list[7].replace("'", "")
            Description = build_list[8].replace("'", "")
            Unit_Of_Measure = build_list[9].replace("'", "")
            Qty = build_list[10].replace("'", "")
            Line_Total_Ex_VAT = build_list[11].replace("'", "")
            Color = build_list[12].replace("'", "")
            Date_To_Order = build_list[13].replace("'", "")
            Order_Comments = build_list[14].replace("'", "")
            Date_Ordered = build_list[15].replace("'", "")
            Purchase_Order = build_list[16].replace("'", "")
            Expected_Delivery = build_list[17].replace(')', "").replace("'", "")
            # Create the object that will build the list for the table
            self.construction_list.append(Object_List_View_Builder.OrderMenuRowBuilder(ID,
                                                                                      Status,
                                                                                      Order_Raiser,
                                                                                      Project,
                                                                                      Supplier,
                                                                                      Brand,
                                                                                      Model,
                                                                                      Company_Code,
                                                                                      Description,
                                                                                      Unit_Of_Measure,
                                                                                      Qty,
                                                                                      Line_Total_Ex_VAT,
                                                                                      Color,
                                                                                      Date_To_Order,
                                                                                      Order_Comments,
                                                                                      Date_Ordered,
                                                                                      Purchase_Order,
                                                                                      Expected_Delivery))
        # Set the current object list for the table
        self.order_menu_list_view.SetObjects(self.construction_list)


    # --------------------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------------------

class QrCodeTab(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # --------------------------------------------------------------------------------------------
        # Create the size's for the tab page
        # --------------------------------------------------------------------------------------------

        qr_code_tab_main_sizer = wx.BoxSizer(wx.VERTICAL)
        qr_code_tab_wrapper_sizer = wx.BoxSizer(wx.HORIZONTAL)

        qr_code_tab_vert_one_sizer = wx.BoxSizer(wx.VERTICAL)
        qr_code_tab_vert_two_sizer = wx.BoxSizer(wx.VERTICAL)
        qr_code_tab_vert_three_sizer = wx.BoxSizer(wx.VERTICAL)
        qr_code_tab_vert_four_sizer = wx.BoxSizer(wx.VERTICAL)

        qr_code_tab_filter_btn_sizer = wx.BoxSizer(wx.HORIZONTAL)


        # --------------------------------------------------------------------------------------------
        # populate the first sizer with widgets
        # --------------------------------------------------------------------------------------------
        # Add new project to the list -> use this button to open a modal that will input information
        # and create a new entry in the data base

        hold = ['Somerset Square', 'proj2', 'proj3', 'proj4']

        self.qr_code_drop_down_description_text = wx.StaticText(self, -1, "Projects", (100, 100))
        qr_code_tab_vert_two_sizer.Add(self.qr_code_drop_down_description_text, 0, wx.ALIGN_LEFT | wx.ALL, 1)

        self.qr_code_project_drop_down = wx.ComboBox(self, size=wx.DefaultSize, choices=hold)
        qr_code_tab_vert_two_sizer.Add(self.qr_code_project_drop_down, 0, wx.ALIGN_LEFT | wx.ALL, 1)

        self.qr_code_count_description_text = wx.StaticText(self, -1, "Count", (100, 100))
        qr_code_tab_vert_two_sizer.Add(self.qr_code_count_description_text, 0, wx.ALIGN_LEFT | wx.ALL, 1)

        self.qr_code_count_text_ctrl = wx.TextCtrl(self, -1, "0", size=(100, -1))
        qr_code_tab_vert_two_sizer.Add(self.qr_code_count_text_ctrl, 0, wx.ALIGN_LEFT | wx.ALL, 1)

        self.qr_code_generate_btn_btn = wx.Button(self, -1, "Generate Code")
        qr_code_tab_vert_two_sizer.Add(self.qr_code_generate_btn_btn, 0, wx.ALIGN_BOTTOM | wx.ALL, 1)

        # --------------------------------------------------------------------------------------------
        # populate the second sizer with widgets
        # --------------------------------------------------------------------------------------------
        # Will bring up modal that will have more advanced query options for the user to select from
        # for advanced searching
        self.qr_code_filter_options_btn = wx.Button(self, -1, "Filter Options")
        self.qr_code_filter_options_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnFilterOptions(event))
        # Will run a basic SQL query based on the information in the text control
        self.qr_code_filter_search_btn = wx.Button(self, -1, "Search")
        self.qr_code_filter_search_btn.Bind(wx.EVT_BUTTON, lambda event: self.OnProductSearch(event))
        self.qr_code_btn_filter_text_ctrl = wx.TextCtrl(self, -1, "", size=(175, -1))
        # Will provide feed back on query

        # Add the widgets to the sizer
        qr_code_tab_filter_btn_sizer.Add(self.qr_code_filter_options_btn, 0, wx.ALIGN_CENTER, 10)
        qr_code_tab_filter_btn_sizer.Add(self.qr_code_filter_search_btn, 0, wx.ALIGN_CENTER, 10)
        qr_code_tab_filter_btn_sizer.Add(self.qr_code_btn_filter_text_ctrl, 0, wx.ALIGN_CENTER, 10)
        qr_code_tab_filter_btn_sizer.AddSpacer(20)

        self.qr_code_list_view = ObjectListView(self, style=wx.LC_REPORT | wx.SUNKEN_BORDER)

        # --------------------------------------------------------------------------------------------
        # populate the main sizer with the sub sizer
        # --------------------------------------------------------------------------------------------

        qr_code_tab_vert_one_sizer.Add(qr_code_tab_filter_btn_sizer, 0, wx.EXPAND, 10)
        qr_code_tab_vert_one_sizer.Add(self.qr_code_list_view, 1, wx.EXPAND, 10)

        qr_code_tab_wrapper_sizer.Add(qr_code_tab_vert_one_sizer, 1, wx.EXPAND, 10)
        qr_code_tab_wrapper_sizer.Add(qr_code_tab_vert_two_sizer, 0, wx.ALL, 10)
        qr_code_tab_wrapper_sizer.Add(qr_code_tab_vert_three_sizer, 1, wx.ALL, 10)
        qr_code_tab_wrapper_sizer.Add(qr_code_tab_vert_four_sizer, 1, wx.ALL, 10)

        qr_code_tab_main_sizer.Add(qr_code_tab_wrapper_sizer, 1, wx.EXPAND, 10)

        # --------------------------------------------------------------------------------------------
        Object_List_View_Builder.SetColumnsProducts(self.qr_code_list_view)
        # --------------------------------------------------------------------------------------------
        self.SetSizerAndFit(qr_code_tab_main_sizer)

    def OnFilterOptions(self, event):
        Modals.FilterDialog(self,  'Filter Options').ShowModal()

    # --------------------------------------------------------------------------------------------
    # Function for searching this table in the data base
    # --------------------------------------------------------------------------------------------
    def OnProductSearch(self, event):
        # Read database connection info
        conn_read = Read_And_Write_Files.Read_File('data_conn.tuk')
        server_in = conn_read[0]
        database_in = conn_read[1]
        port_in = conn_read[2]
        driver_in = conn_read[3]

        # Read current user info
        user_read = Read_And_Write_Files.Read_File('user.tuk')
        username = user_read[0]
        password = user_read[1]

        #try:
            # Open connection
        open_con = SQL.SQLCon(server_in, database_in, username, password, driver_in, port_in)
            # Get table column names
        column_list = SQL.SQLGetColumnNames(open_con, "Products")
            # Check to see if we should search all or a for a value
        if self.qr_code_btn_filter_text_ctrl.GetValue() == "":
                # Search All
            search_result = SQL.SQLSearchAll(open_con, username, "Products", self.qr_code_btn_filter_text_ctrl.GetValue(), "Search All")
                # Update table with return from database
            QrCodeTab.UpdateProductDisplay(self, search_result)

        else:
                # Search for a value
            search_result = SQL.SQLSearchColumnMutipleEntry(open_con, username, "Products", self.qr_code_btn_filter_text_ctrl.GetValue(), column_list)
                # Update table with return from database
            QrCodeTab.UpdateProductDisplay(self, search_result)


        #except:
            # Error message
        #   Modals.ShowMessageDlg(self, "Failed to access the data base, please check with your system admin.","Error",
        #                          wx.OK | wx.CANCEL | wx.ICON_QUESTION)

    # --------------------------------------------------------------------------------------------
    # Update the rows in the table from information in the database
    # --------------------------------------------------------------------------------------------
    def UpdateProductDisplay(self, entry_list):
        # Create a list to be inserted into the table
        self.construction_list = []
        for row in entry_list:
            # Split the tuple returned from the data base into individual values
            build_list = str(row).split(',')
            ID = build_list[0].replace('(', "").replace("'", "")
            Brand = build_list[1].replace("'", "")
            Supplider = build_list[2].replace("'", "")
            Model = build_list[3].replace("'", "")
            Company_Code = build_list[4].replace("'", "")
            Description = build_list[5].replace("'", "")
            Color = build_list[6].replace("'", "")
            Unit_Of_Measure = build_list[7].replace("'", "")
            Total_Qty = build_list[8].replace("'", "")
            Project_Qty = build_list[9].replace("'", "")
            Free_Stock_Qty = build_list[10].replace("'", "")
            price_ex_vat = build_list[11].replace(')', "").replace("'", "")
            # Create the object that will build the list for the table
            self.construction_list.append(Object_List_View_Builder.ProductsRowBuilder(ID,
                                                                                      Brand,
                                                                                      Supplider,
                                                                                      Model,
                                                                                      Company_Code,
                                                                                      Description,
                                                                                      Color,
                                                                                      Unit_Of_Measure,
                                                                                      Total_Qty,
                                                                                      Project_Qty,
                                                                                      Free_Stock_Qty,
                                                                                      price_ex_vat
                                                                                      ))
        # Set the current object list for the table
        self.qr_code_list_view.SetObjects(self.construction_list)

########################################################################################################################
# The Main panel class ! This is the area inside of the windows "Python" program boarder
########################################################################################################################
class MainPanel(wx.Panel):
    # ----------------------------------------------------------------------

    # ----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)

########################################################################################################################
# The Main Menu Bar Class where we create the buttons for the menu bar!
########################################################################################################################
class MainMenuBar(wx.MenuBar):

    def __new__(self, panel):
        panel = wx.MenuBar

        menu_bar = wx.MenuBar()

        # --------------------------------------------------------------------------------------------
        # Menu buttons created here!
        # --------------------------------------------------------------------------------------------
        file_menu_button = wx.Menu()
        edit_menu_button = wx.Menu()
        tools_menu_button = wx.Menu()
        view_menu_button = wx.Menu()
        help_menu_button = wx.Menu()

        # --------------------------------------------------------------------------------------------
        # Add the menu buttons to the menu bar!
        # --------------------------------------------------------------------------------------------
        menu_bar.Append(file_menu_button, 'File')
        menu_bar.Append(edit_menu_button, 'Edit')
        menu_bar.Append(tools_menu_button, 'Tools')
        menu_bar.Append(view_menu_button, 'View')
        menu_bar.Append(help_menu_button, 'Help')


        ##############################################################################################
        # Add sub menu buttons to the menu bar!
        ##############################################################################################

        # --------------------------------------------------------------------------------------------
        # Add sub buttons for the file button
        # --------------------------------------------------------------------------------------------
        self.open_sub_btn = file_menu_button.Append(wx.ID_ANY, 'Open', 'Add a file to the list')
        self.login_sub_btn = file_menu_button.Append(wx.ID_ANY, 'Login', 'Add a file to the list')
        self.log_out_sub_btn = file_menu_button.Append(wx.ID_ANY, 'Logout', 'Add a file to the list')
        self.exit_sub_btn = file_menu_button.Append(wx.ID_EXIT, 'Exit', 'Exit Program')

        # --------------------------------------------------------------------------------------------
        # Add sub buttons for the edit button
        # --------------------------------------------------------------------------------------------
        self.customers_sub_btn = edit_menu_button.Append(wx.ID_ANY, 'Customers', 'Customer records')
        self.projects_sub_btn = edit_menu_button.Append(wx.ID_ANY, 'Projects', 'Project records')
        self.products_sub_btn = edit_menu_button.Append(wx.ID_ANY, 'Products', 'Product records')
        self.stock_adjustment_sub_btn = edit_menu_button.Append(wx.ID_ANY, 'Stock Adjustment', 'Made adjustments '
                                                                                  'to the stock in you inventory')
        self.order_menu_sub_btn = edit_menu_button.Append(wx.ID_ANY, 'Order Menu', 'Products that have been requested '
                                                                            'to be ordered')
        self.company_info_menu_sub_btn = edit_menu_button.Append(wx.ID_ANY, 'Company Info', 'Your company information')

        # --------------------------------------------------------------------------------------------
        # Add sub buttons for the tools button
        # --------------------------------------------------------------------------------------------
        self.database_manager_sub_btn = tools_menu_button.Append(wx.ID_ANY, 'Database Manager', 'Manage the central '
                                                                                           'database system')

        self.report_builder_sub_btn = tools_menu_button.Append(wx.ID_ANY, 'Report Builder', 'Manage the central '
                                                                                           'database system')
        self.lable_builder_sub_btn = tools_menu_button.Append(wx.ID_ANY, 'Label Builder', 'Manage the central '
                                                                                           'database system')


        # --------------------------------------------------------------------------------------------
        # Add sub buttons for the view button
        # --------------------------------------------------------------------------------------------
        self.user_logs_menu_sub_btn = view_menu_button.Append(wx.ID_ANY, 'Users Logs',
                                                              'View a log of quires made to the '
                                                              'data base')


        # --------------------------------------------------------------------------------------------
        # Add sub buttons for the help button
        #--------------------------------------------------------------------------------------------
        self.about_sub_btn = help_menu_button.Append(wx.ID_ANY, 'About', 'About the program')
        self.licence_sub_btn = help_menu_button.Append(wx.ID_ANY, 'Licence', 'The legal stuff')
        self.contact_sub_btn = help_menu_button.Append(wx.ID_ANY, 'Contact', 'Contact the team for help!')



        # --------------------------------------------------------------------------------------------
        # Return the menu bar
        # --------------------------------------------------------------------------------------------
        return(menu_bar)

########################################################################################################################
# The InfoBar Class that create the bar at the bottom of the program that shows the user updates to as they happen
########################################################################################################################
class InfoBar(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        info_bar_main_sizer = wx.BoxSizer(wx.VERTICAL)

        t = wx.StaticText(self, -1, "This is the area where there will be some info on about who is logged in and "
                                    "what else if happening in the program", (20, 20))
        info_bar_main_sizer.Add(t, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 0)
        self.SetSizerAndFit(info_bar_main_sizer)

########################################################################################################################
# Class for the "Windows Fame"
########################################################################################################################
class MainFrame(wx.Frame):


    def __init__(self):
        # create a instance of the frame and set the parameters of it
        wx.Frame.__init__(self, None, title="Tuck Stock Control And QR Code Creator, Time To Tuck In!", size=(800, 600))

        # Call the MainPanel class
        panel = MainPanel(self)

        #Call the MenuBar class and set it as the menu bar for the frame!
        self.SetMenuBar(MainMenuBar(panel))

        #Bind events to the buttons of the menu bar!
        ################################################################################################################
        #---------------------------------------------------------------------------------------------------------------
        # File menu bar binds
        # ---------------------------------------------------------------------------------------------------------------
        self.Bind(wx.EVT_MENU, lambda event: self.OnOpen(event), MainMenuBar.open_sub_btn)
        self.Bind(wx.EVT_MENU, lambda event: self.OnLogin(event), MainMenuBar.login_sub_btn)
        self.Bind(wx.EVT_MENU, lambda event: self.OnLogout(event), MainMenuBar.log_out_sub_btn)
        # ---------------------------------------------------------------------------------------------------------------
        # Edit menu bar binds
        # ---------------------------------------------------------------------------------------------------------------
        self.Bind(wx.EVT_MENU, lambda event: self.OnCompanyInfo(event), MainMenuBar.company_info_menu_sub_btn)
        self.Bind(wx.EVT_MENU, lambda event: self.OnUserLogs(event), MainMenuBar.user_logs_menu_sub_btn)
        # ---------------------------------------------------------------------------------------------------------------
        # Tools menu bar binds
        # ---------------------------------------------------------------------------------------------------------------
        self.Bind(wx.EVT_MENU, lambda event: self.OnDataBaseManager(event), MainMenuBar.database_manager_sub_btn)
        self.Bind(wx.EVT_MENU, lambda event: self.OnReportBuilder(event), MainMenuBar.report_builder_sub_btn)
        self.Bind(wx.EVT_MENU, lambda event: self.OnLabelBuilder(event), MainMenuBar.lable_builder_sub_btn)
        # ---------------------------------------------------------------------------------------------------------------
        # Help menu bar binds
        # ---------------------------------------------------------------------------------------------------------------
        self.Bind(wx.EVT_MENU, lambda event: self.OnAbout(event), MainMenuBar.about_sub_btn)
        self.Bind(wx.EVT_MENU, lambda event: self.OnLicence(event), MainMenuBar.licence_sub_btn)
        self.Bind(wx.EVT_MENU, lambda event: self.OnContact(event), MainMenuBar.contact_sub_btn)
        ################################################################################################################
        # Call the TabBar class and add it to the panel
        tab_bar = TabBar(panel)
        # Need to create and call a class for the info bar that will be at the bottom of the frame!
        info_bar = InfoBar(panel)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(tab_bar, 1, wx.ALL | wx.EXPAND, 5)
        sizer.Add(info_bar, 0, wx.ALL | wx.EXPAND, 5)

        # We add the sizer to the panel
        panel.SetSizerAndFit(sizer)

        # Call the layout -> need to read more into the exact function of this.
        self.Layout()

        # The the frame that when it is loaded it should appear in the centre of the screen!
        self.Centre(True)

        self.Show()

    def OnOpen(self, event):
        Modals.OpenDialog(self, 'Open File').ShowModal()

    def OnLogin(self, event):
        Modals.LoginDialog(self, 'Login').ShowModal()

    def OnLogout(self, event):
        Modals.LogOutDialog(self, 'Logout').ShowModal()

    def OnCompanyInfo(self, event):
        # need to run a search query to find this info in the database, and then when we run the edit modal we need to
        # use a insert Querry to update the information to the database so that when it is re-run here it will be updated
        # every time.
        comp_read = Read_And_Write_Files.Read_File('comp_info.tuk')

        company_name = comp_read[0]
        company_owner = comp_read[1]
        company_vocation = comp_read[2]
        company_year_established = comp_read[3]
        company_address = comp_read[4]
        company_contact_number = comp_read[5]
        logo_file_path = comp_read[6]


        Modals.CompanyInfoDialog(self, 'Company Info',company_name,company_owner,company_vocation,
                                 company_year_established,company_address,company_contact_number,logo_file_path).ShowModal()

    def OnUserLogs(self, event):
        Modals.UserLogsDialog(self, 'User Logs').ShowModal()

    def OnDataBaseManager(self, event):
        Modals.DatabaseManagerDialog(self, 'Database Manager').ShowModal()

    def OnReportBuilder(self, event):
        Modals.ReportBuilderDialog(self, 'Report Builder').ShowModal()

    def OnLabelBuilder(self, event):
        Modals.LabelBuilderDialog(self, 'Label Builder').ShowModal()

    def OnAbout(self, event):
        Modals.AboutDialog(self, 'About').ShowModal()

    def OnLicence(self, event):
        Modals.LicenceDialog(self, 'Licence Info').ShowModal()

    def OnContact(self, event):
        Modals.ContactDialog(self, 'Contact Info').ShowModal()
