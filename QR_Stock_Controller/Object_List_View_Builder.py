from ObjectListView import ObjectListView, ColumnDefn

class CustomersRowBuilder(object):
    def __init__(self, ID, name, status, balance, contact,
                 email, telephone, mobile, project):
        self.ID = ID
        self.name = name
        self.status = status
        self.balance = balance
        self.contact = contact
        self.email = email
        self.telephone = telephone
        self.mobile = mobile
        self.project = project

def SetColumnsCustomers(self):

    self.SetColumns([

        ColumnDefn("ID", "left", 80, "ID"),
        ColumnDefn("Name", "left", 100, "name"),
        ColumnDefn("Status", "left", 100, "status"),
        ColumnDefn("Balance", "left", 100, "balance"),
        ColumnDefn("Contact", "left", 150, "contact"),
        ColumnDefn("Email", "left", 220, "email"),
        ColumnDefn("Telephone", "left", 220, "telephone"),
        ColumnDefn("Mobile", "left", 220, "mobile"),
        ColumnDefn("Project", "left", 220, "project")
    ])

class ProjectsRowBuilder(object):
    def __init__(self, ID, project_code, name, status, customer):
        self.ID = ID
        self.project_code = project_code
        self.name = name
        self.status = status
        self.customer = customer

def SetColumnsProjects(self):

    self.SetColumns([

        ColumnDefn("ID", "left", 80, "ID"),
        ColumnDefn("Project Code", "left", 150, "project_code"),
        ColumnDefn("Name", "left", 100, "name"),
        ColumnDefn("Status", "left", 150, "status"),
        ColumnDefn("Customer", "left", 200, "customer")
    ])

class ProjectsAdjustmentRowBuilder(object):
    def __init__(self, name, project_code):
        self.name = name
        self.project_code = project_code

def SetColumnsStockAdjustmentProjects(self):

    self.SetColumns([

        ColumnDefn("Project", "left", 220, "name"),
        ColumnDefn("Project Code", "left", 100, "project_code")

    ])

class ProductsRowBuilder(object):
    def __init__(self, ID, brand, supplier, model, company_code,
                 description, color, unit_of_measure, total_qty, project_qty, free_stock_qty, price_ex_vat):
        self.ID = ID
        self.brand = brand
        self.supplier = supplier
        self.model = model
        self.company_code = company_code
        self.description = description
        self.color = color
        self.unit_of_measure = unit_of_measure
        self.total_qty = total_qty
        self.project_qty = project_qty
        self.free_stock_qty = free_stock_qty
        self.price_ex_vat = price_ex_vat

def SetColumnsProducts(self):
    self.SetColumns([
        ColumnDefn("ID", "left", 80, "ID"),
        ColumnDefn("Brand", "left", 100, "brand"),
        ColumnDefn("Supplier", "left", 150, "supplier"),
        ColumnDefn("Model", "left", 150, "model"),
        ColumnDefn("Company Code", "left", 100, "company_code"),
        ColumnDefn("Description", "left", 100, "description"),
        ColumnDefn("Color", "left", 100, "color"),
        ColumnDefn("Unit Of Measure", "left", 100, "unit_of_measure"),
        ColumnDefn("Total Qty", "left", 100, "total_qty"),
        ColumnDefn("Project Qty", "left", 100, "project_qty"),
        ColumnDefn("Free Stock Qty", "left", 100, "free_stock_qty"),
        ColumnDefn("Price Ex VAT", "left", 100, "price_ex_vat")
    ])

class OrderMenuRowBuilder(object):
    def __init__(self, ID, status, order_raiser, project, supplier,
                 brand, model, company_code, description, unit_of_measure, qty, line_total_ex_vat, color,
                 date_to_order_by, order_comments, date_ordered, purchase_order, expected_delivery):
        self.ID = ID
        self.status = status
        self.order_raiser = order_raiser
        self.project = project
        self.supplier = supplier
        self.brand = brand
        self.model = model
        self.company_code = company_code
        self.description = description
        self.unit_of_measure = unit_of_measure
        self.qty = qty
        self.line_total_ex_vat = line_total_ex_vat
        self.color = color
        self.date_to_order_by = date_to_order_by
        self.order_comments = order_comments
        self.date_ordered = date_ordered
        self.purchase_order = purchase_order
        self.expected_delivery = expected_delivery

def SetColumnsOrderMenu(self):
    self.SetColumns([
        ColumnDefn("ID", "left", 80, "ID"),
        ColumnDefn("Status", "left", 220, "status"),
        ColumnDefn("Order Raiser", "left", 200, "order_raiser"),
        ColumnDefn("Project", "left", 150, "project"),
        ColumnDefn("Supplier", "left", 150, "supplier"),
        ColumnDefn("Brand", "left", 100, "brand"),
        ColumnDefn("Model", "left", 100, "model"),
        ColumnDefn("Company Code", "left", 100, "company_code"),
        ColumnDefn("Description", "left", 100, "description"),
        ColumnDefn("Unit Of Measure", "left", 100, "unit_of_measure"),
        ColumnDefn("Qty", "left", 100, "qty"),
        ColumnDefn("Line Total Ex-VAT", "left", 100, "line_total_ex_vat"),
        ColumnDefn("Color", "left", 100, "color"),
        ColumnDefn("Date To Order By", "left", 100, "date_to_order_by"),
        ColumnDefn("Order Comments", "left", 100, "order_comments"),
        ColumnDefn("Date Ordered", "left", 100, "date_ordered"),
        ColumnDefn("Purchase Order", "left", 100, "purchase_order"),
        ColumnDefn("Expected Delivery", "left", 100, "expected_delivery")
    ])

class UserLogRowBuilder(object):
    def __init__(self, ID, table, command, date, time):
        self.ID = ID
        self.table = table
        self.command = command
        self.date = date
        self.time = time

def SetColumnsUserLog(self):
    self.SetColumns([

        ColumnDefn("ID", "left", 100, "ID"),
        ColumnDefn("Table", "left", 200, "table"),
        ColumnDefn("Command", "left", 150, "command"),
        ColumnDefn("Date", "left", 150, "date"),
        ColumnDefn("Time", "left", 100, "time")
    ])

class ProjectStockRowBuilder(object):
    def __init__(self, ID, model, total_qty, internal_held_qty, site_held_qty, cost):
        self.ID = ID
        self.model = model
        self.total_qty = total_qty
        self.internal_held_qty = internal_held_qty
        self.site_held_qty = site_held_qty
        self.cost = cost

def SetColumnsProjectStock(self):
    self.SetColumns([

        ColumnDefn("ID", "left", 100, "ID"),
        ColumnDefn("Model", "left", 150, "model"),
        ColumnDefn("Total Qty", "left", 150, "total_qty"),
        ColumnDefn("Internal Held Qty", "left", 150, "internal_held_qty"),
        ColumnDefn("Site Held Qty", "left", 150, "site_held_qty"),
        ColumnDefn("Cost", "left", 100, "cost")
    ])


