########################################################################################################################
# Program - TuckPDF Split And Merge -- A pdf splitter and merger.
# Author - Mark Tucker

''' The following application is a PDF merger and splitter. The aim of this app is to be able to split and merge large
pdf files generated from CAD software for my own personal use.

The code used is property of the Author Mark Tucker but the classes used are the
property of there own individual developers. The following application is not for the goal of
gaining remuneration, but as a leaning experience.

In the following code you may see some redundancy's, mistakes and inefficient code. This as stated above because this
has been a leaning exercise, this is not to say that the app does not preform! But if you are viewing this please look
past this and enjoy

Happy Coding!
'''
########################################################################################################################

########################################################################################################################
# Import the library's
########################################################################################################################

# WXPython GUI
import wx
# Python Operating System module
import os
# import path from above
import os.path
import stat
import time
# Import PyPDF2 and it merger, writer and reader classes. For reading writing and merging pdf files!
from PyPDF2 import PdfFileMerger, PdfFileWriter, PdfFileReader
# Import the canvas class from reportLab this is used for creating blank reports
from reportlab.pdfgen.canvas import Canvas
# A visually appealing list
from ObjectListView import ObjectListView, ColumnDefn


########################################################################################################################
# This is the panel drop target - Note to self why did i call this Tuck main panel ?
########################################################################################################################

class PDFDropArea(wx.FileDropTarget):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, window):
        """Constructor"""
        wx.FileDropTarget.__init__(self)
        self.window = window

    # ----------------------------------------------------------------------
    def OnDropFiles(self, x, y, file_names):
        """
        When files are dropped, update the display
        """
        self.window.updateDisplay(file_names)


########################################################################################################################
# Class that creates the file_list object
########################################################################################################################

class FileInfo(object):
    """"""
    # ----------------------------------------------------------------------
    def __init__(self, path, directory, date_created, date_modified, size, index):
        """Constructor"""
        self.index = index
        self.name = os.path.basename(path)
        self.path = path
        self.file_path = directory
        self.date_created = date_created
        self.date_modified = date_modified
        self.size = size

########################################################################################################################
# The Main panel class ! This is the grew area inside of the windows "Python" program boarder
########################################################################################################################

class MainPanel(wx.Panel):
    # ----------------------------------------------------------------------

    # ----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)

        self.file_list = []
        self.current_selection = 0

        file_drop_target = PDFDropArea(self)
        lbl_drop_area = wx.StaticText(self, label="Drag some PDFs here:")
        lbl_file_out_txt = wx.StaticText(self, label="Merge Name:")
        lbl_file_path_txt = wx.StaticText(self, label="Merge Output Location:")
        self.file_name = wx.TextCtrl(self, -1, "", size=(175, -1))
        # Was this just used for testing ?
        main_file_name = self.file_name.GetValue()

        self.btn_up = wx.Button(self, -1, "Move Up")
        self.btn_up.Bind(wx.EVT_BUTTON, lambda event: self.OnMoveUp(event, self.file_list, self.current_selection))

        self.btn_out_root = wx.Button(self, -1, "Output Location")
        self.btn_out_root.Bind(wx.EVT_BUTTON, self.onDir)

        self.btn_dwn = wx.Button(self, -1, "Move Down")
        self.btn_dwn.Bind(wx.EVT_BUTTON, lambda event: self.OnMoveDown(event, self.file_list, self.current_selection))

        self.btn_del = wx.Button(self, -1, "Delete File")
        self.btn_del.Bind(wx.EVT_BUTTON, lambda event: self.OnDelete(event, self.file_list, self.current_selection))

        self.btn_merg = wx.Button(self, -1, "Merge Files")
        self.btn_merg.Bind(wx.EVT_BUTTON, lambda event: self.OnMerge(event, self.file_list, self.file_name.GetValue(),
                                                                     self.file_root_txt.GetLabel()))

        self.btn_split = wx.Button(self, -1, "Split Files")
        self.btn_split.Bind(wx.EVT_BUTTON, lambda event: self.OnSplit(event, self.file_list, self.current_selection))

        self.file_root_txt = wx.StaticText(self, -1, label="", size=(175, -1))

        self.olv = ObjectListView(self, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.olv.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnClick)
        self.olv.SetDropTarget(file_drop_target)


        self.setFiles()

        ########################################################################

        top_bar_sizer = wx.BoxSizer(wx.HORIZONTAL)
        top_bar_sizer.Add(self.btn_up, 0, wx.ALIGN_CENTER, 10)
        top_bar_sizer.Add(self.btn_dwn, 0, wx.ALIGN_CENTER, 10)
        top_bar_sizer.Add(self.btn_del, 0, wx.ALIGN_CENTER, 10)
        top_bar_sizer.Add(self.btn_merg, 0, wx.ALIGN_CENTER, 10)
        top_bar_sizer.Add(self.btn_split, 0, wx.ALIGN_CENTER, 10)
        top_bar_sizer.AddSpacer(20)
        top_bar_sizer.Add(lbl_file_out_txt, 0, wx.ALIGN_CENTER, 5)
        top_bar_sizer.AddSpacer(5)
        top_bar_sizer.Add(self.file_name, 0, wx.ALIGN_CENTER, 5)

        ########################################################################

        bot_bar_sizer = wx.BoxSizer(wx.HORIZONTAL)
        bot_bar_sizer.Add(self.btn_out_root, 0, wx.ALIGN_CENTER, 10)
        bot_bar_sizer.AddSpacer(10)
        bot_bar_sizer.Add(lbl_file_path_txt, 0, wx.ALIGN_CENTER, 10)
        bot_bar_sizer.AddSpacer(5)
        bot_bar_sizer.Add(self.file_root_txt, 0, wx.ALIGN_CENTER, 10)
        bot_bar_sizer.AddSpacer(20)

        ########################################################################

        panel_wrapper_sizer = wx.BoxSizer(wx.VERTICAL)
        panel_wrapper_sizer.Add(top_bar_sizer, 0, wx.ALL, 5)
        panel_wrapper_sizer.Add(lbl_drop_area, 0, wx.ALL, 5)
        panel_wrapper_sizer.Add(self.olv, 1, wx.EXPAND)
        panel_wrapper_sizer.Add(bot_bar_sizer, 0, wx.ALL, 5)

        self.SetSizer(panel_wrapper_sizer)

    ########################################################################
    # Write what updateDisplay is here
    # ----------------------------------------------------------------------
    def updateDisplay(self, file_list):
        """"""

        object_index = 0
        for path in file_list:

            file_stats = os.stat(path)
            file_path = os.path.abspath(path)
            file_type = os.path.splitext(file_path)[1]
            if file_type == ".pdf":

                creation_time = time.strftime("%m/%d/%Y %I:%M %p",
                                              time.localtime(file_stats[stat.ST_CTIME]))
                modified_time = time.strftime("%m/%d/%Y %I:%M %p",
                                              time.localtime(file_stats[stat.ST_MTIME]))
                file_size = file_stats[stat.ST_SIZE]
                if file_size > 1024:
                    file_size = file_size / 1024.0
                    file_size = "%.2f KB" % file_size

                self.file_list.append(FileInfo(path,
                                               file_path,
                                               creation_time,
                                               modified_time,
                                               file_size,
                                               str(object_index)))

                object_index = object_index + 1
            else:
                self.showMessageDlg("This is not a PDF file", "Unknown File Type", wx.OK | wx.CANCEL | wx.ICON_QUESTION)

        self.olv.SetObjects(self.file_list)

    ########################################################################
    # Write what OnClick is here
    # ----------------------------------------------------------------------
    def OnClick(self, event):

        getID = self.olv.GetSelectedObject()
        current_selection = getID.name
        self.current_selection = str(current_selection)
        #self.debugOneTxt.SetLabel(str(current_selection))

    ########################################################################
    # Write what setFiles is here
    # ----------------------------------------------------------------------
    def setFiles(self):
        """"""
        self.olv.SetColumns([

            ColumnDefn("Name", "left", 220, "name"),
            ColumnDefn("File Path", "left", 200, "file_path"),
            ColumnDefn("Date created", "left", 150, "date_created"),
            ColumnDefn("Date modified", "left", 150, "date_modified"),
            ColumnDefn("Size", "left", 100, "size")
        ])

        self.olv.SetObjects(self.file_list)


    ########################################################################
    # Write what onDir is here
    # ----------------------------------------------------------------------
    def onDir(self, event):

        dlg = wx.DirDialog(self, "Choose a directory:",
                           style=wx.DD_DEFAULT_STYLE
                            #| wx.DD_DIR_MUST_EXIST
                            | wx.DD_CHANGE_DIR
                           )
        if dlg.ShowModal() == wx.ID_OK:
            outputlocation = dlg.GetPath()
            self.file_root_txt.SetLabel(outputlocation)
            return outputlocation

        dlg.Destroy()

    ########################################################################
    # Write what showMessageDlg is here
    # ----------------------------------------------------------------------
    def showMessageDlg(self, msg, title, style):
        """"""
        dlg = wx.MessageDialog(parent=None, message=msg,
                               caption=title, style=style)
        dlg.ShowModal()
        dlg.Destroy()

    ########################################################################
    # Write what OnMoveUp is here
    # ----------------------------------------------------------------------
    def OnMoveUp(self, event, file_list, current_selection):

        # for loop counters
        x = 0
        y = 0
        list_length = len(file_list)

        if list_length >= 1:

            for x in range(len(file_list)):

                if file_list[x].name == current_selection:

                    list_hold = file_list[x]

                    for y in range(len(file_list)):
                        if y == (x - 1):
                            indexPre = y
                            list_hold_pre = file_list[y]
                            file_list[y] = list_hold
                            file_list[x] = list_hold_pre


        else:
            pass
        # Update the list of files in the array
        self.file_list = file_list

        #self.debugOneTxt.SetLabel((file_list[y].name))

        # The following updates the list !
        self.olv.SetObjects(self.file_list)
        # Need to work out why the item at x is not reselected !
        self.olv.SetItemState(self.file_list[x], wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)

    ########################################################################
    # Write what OnMoveDown is here
    # ----------------------------------------------------------------------
    def OnMoveDown(self, event, file_list, current_selection):
        x = 0
        y = 0
        toggle = False
        list_length = len(file_list)

        if list_length >= 1:

            for x in range(len(file_list)):

                if file_list[x].name == current_selection:

                    list_hold = file_list[x]
                    if toggle == False:
                        for y in range(len(file_list)):
                            if y == (x + 1):
                                toggle = True
                                list_hold_pre = file_list[y]
                                file_list[y] = list_hold
                                file_list[x] = list_hold_pre





        else:
            pass
        # Update the list of files in the array
        self.file_list = file_list

        #self.debugOneTxt.SetLabel((file_list[y].name))

        # The following updates the list !
        self.olv.SetObjects(self.file_list)

    ########################################################################
    # Write what OnDelete is here
    # ----------------------------------------------------------------------
    def OnDelete(self, event, file_list, current_selection):
        x = 0
        for x in range(len(file_list)):
            if file_list[x].name == current_selection:
                del (file_list[x])
                self.file_list = file_list
                self.olv.SetObjects(self.file_list)

    ########################################################################
    # Write what OnMerge is here
    # ----------------------------------------------------------------------
    def OnMerge(self, event, file_list, output_name, out_location):

        # Creates a instance of the merger
        merger = PdfFileMerger()
        # Length of the file list
        list_length = len(file_list)

        # for loop counters
        x = 0

        # if check to see if there is more than one document in the list
        if list_length >= 1:
            # loop through all the documents in the file list and add them to the merger target
            for x in range(len(file_list)):
                doc_path_hold = open(file_list[x].path, "rb")
                merger.append(doc_path_hold)
        # if checks that there is a name and a location give for the document
        if not output_name == "" and not out_location == "" and list_length >= 1:
            # Concatonate the output path with the file name
            target = str(out_location) + '\\' + str(output_name + ".pdf")
            # Creates a blank PDF canvas at the location and with the name of the target VAR
            canvas = Canvas(target)
            canvas.showPage()
            canvas.save()
            # Loads the traget into the PDF writer
            output = file(target, "wb")
            # Over writes the bank PDF with a new one !
            merger.write(output)

        else:
            # need to open a message box that tells the user that they need to check if they have more than
            # one document, have set a file name and a out output path
            self.showMessageDlg("Please make sure you have given a file name, and a location to merge too!", "Error",
                                wx.OK | wx.CANCEL | wx.ICON_QUESTION)

    ########################################################################
    # Write what OnSplit is here
    # ----------------------------------------------------------------------
    def OnSplit(self, event, file_list, current_selection):
        # split_options is a instance of the SplitDialog class " That is a pop up modal "
        split_options = SplitDialog(self, "Split Pages", file_list, current_selection).ShowModal()

########################################################################################################################
# Class for the pop up window that gives the user all the possible ways I have made to split a PDF file !
########################################################################################################################

class SplitDialog(wx.Dialog):
    def __init__(self, parent, title, file_list, current_selection):
        super(SplitDialog, self).__init__(parent, title=title, size=(600, 300))
        # Create a new panel
        panel = wx.Panel(self)
        # Create a Var call page nums and set it to the lowest possible number of pages!
        Page_Num = 1
        # Create a var that holds the file path the split files will go to !
        self.spt_out_txt = ""
        if current_selection == 0:
            current_selection = file_list[current_selection].name
        # Declare the pdf reader that will load the pdf into python

        # For scans through the file list and finds the file that matches the currently selections this check is done
        # by the if !
        for x in range(len(file_list)):
            if file_list[x].name == current_selection:
                # The PDFFileReader class is called form the library and reads the file into the in_pdf "In PDF" var it
                # gets the file form the file list at the position of where the loop finished
                in_pdf = PdfFileReader(file(file_list[x].path, "rb"))
                # We call the getNumPages function from the read pdf and save that number to a Var
                Page_Num = in_pdf.getNumPages()

        # ----------------------------------------------------------------------

        # The bellow section defines the widget "buttons and stuff" layout for the dialog box.
        # Just the same as above the buttons positions floats on individual bars "rows of widgets"

        # ----------------------------------------------------------------------

        # Title bar with a heading showing the currently selected file, which is the one that will be edited
        siz_title_bar = wx.BoxSizer(wx.HORIZONTAL)

        # Create the label and concatonate the currently selected file. This has already been selected as the name from
        # previous code above in the main panel class
        spt_dia_sel_target = wx.StaticText(self, label="The file you are splitting is: %s" % current_selection)

        # Add label to bar
        siz_title_bar.Add(spt_dia_sel_target, 0, wx.ALL, 10)

        # ----------------------------------------------------------------------

        # create next bar
        siz_spt_all_bar = wx.BoxSizer(wx.HORIZONTAL)
        # Layout Spacer
        siz_spt_all_bar.AddSpacer(20)
        # Create text label
        self.spt_dia_all_txt = wx.StaticText(self, label="Split the file into individual pages!")
        # Add label to bar
        siz_spt_all_bar.Add(self.spt_dia_all_txt, 0, wx.ALIGN_CENTER, 10)

        # Layout Spacer
        siz_spt_all_bar.AddSpacer(20)
        # Create button to split
        self.spt_dia_split_all_btn = wx.Button(self, 0, "Split")
        # Binds a event to the above button
        self.spt_dia_split_all_btn.Bind(wx.EVT_BUTTON,
                                        lambda event: self.IndFileSplit(event, file_list, current_selection,
                                                                        self.spt_dia_out_txt.GetLabel()))
        # Add Button to bar
        siz_spt_all_bar.Add(self.spt_dia_split_all_btn, 0, wx.ALIGN_CENTER, 10)

        # ----------------------------------------------------------------------

        siz_spt_single_bar = wx.BoxSizer(wx.HORIZONTAL)
        # Layout Spacer
        siz_spt_single_bar.AddSpacer(20)
        # Create text label
        self.SptDia_SingTxt = wx.StaticText(self, label="Split a single page from the file!")
        siz_spt_single_bar.Add(self.SptDia_SingTxt, 0, wx.ALIGN_CENTER, 10)
        self.spt_dia_sing_spin = wx.SpinCtrl(self, -1, '1', min=1, max=int(Page_Num))
        # Layout Spacer
        siz_spt_single_bar.AddSpacer(32)
        siz_spt_single_bar.Add(self.spt_dia_sing_spin, 0, wx.ALIGN_CENTER, 10)
        # Layout Spacer
        siz_spt_single_bar.AddSpacer(10)
        self.spt_dia_split_sing_btn = wx.Button(self, 0, "Split")
        self.spt_dia_split_sing_btn.Bind(wx.EVT_BUTTON,
                                         lambda event: self.SinFileSplit(event, file_list, current_selection,
                                                                         self.spt_dia_out_txt.GetLabel(),
                                                                         self.spt_dia_sing_spin.GetValue()))

        siz_spt_single_bar.Add(self.spt_dia_split_sing_btn, 0, wx.ALIGN_CENTER, 10)

        # ----------------------------------------------------------------------

        siz_spt_inc_bar = wx.BoxSizer(wx.HORIZONTAL)
        # Layout Spacer
        siz_spt_inc_bar.AddSpacer(20)
        # Create text label
        self.SptDia_IncTxt = wx.StaticText(self, label="Split range of pages from the file!")
        siz_spt_inc_bar.Add(self.SptDia_IncTxt, 0, wx.ALIGN_CENTER, 10)
        # Layout Spacer
        siz_spt_inc_bar.AddSpacer(23)
        self.spt_dia_inc_min_spin = wx.SpinCtrl(self, -1, '1', min=1, max=int(Page_Num - 1))
        siz_spt_inc_bar.Add(self.spt_dia_inc_min_spin, 0, wx.ALIGN_CENTER, 10)
        self.spt_dia__inc_max_spin = wx.SpinCtrl(self, -1, '1', min=1, max=int(Page_Num))
        siz_spt_inc_bar.Add(self.spt_dia__inc_max_spin, 0, wx.ALIGN_CENTER, 10)
        self.spt_dia_inc_max_btn = wx.Button(self, 0, label="Split")
        self.spt_dia_inc_max_btn.Bind(wx.EVT_BUTTON,
                                      lambda event: self.BetFileSplit(event, file_list, current_selection,
                                                                      self.spt_dia_out_txt.GetLabel(),
                                                                      self.spt_dia_inc_min_spin.GetValue(),
                                                                      self.spt_dia__inc_max_spin.GetValue()))
        # Layout Spacer
        siz_spt_inc_bar.AddSpacer(10)
        siz_spt_inc_bar.Add(self.spt_dia_inc_max_btn, 0, wx.ALIGN_CENTER, 10)

        # ----------------------------------------------------------------------

        siz_out_put_bar = wx.BoxSizer(wx.HORIZONTAL)

        self.out_put_location_btn = wx.Button(self, -1, label="Output Location %s" % self.spt_out_txt)
        siz_out_put_bar.Add(self.out_put_location_btn, 0, wx.ALIGN_CENTER, 10)
        self.out_put_location_btn.Bind(wx.EVT_BUTTON, self.FileOutRoot)
        # Layout Spacer
        siz_out_put_bar.AddSpacer(10)
        # Need to bind a event to this button to call the folder structure finder class from above ! and pass that back
        # to the label bellow !
        self.spt_dia_out_txt = wx.StaticText(self, label="File output location! ")
        siz_out_put_bar.Add(self.spt_dia_out_txt, 0, wx.ALIGN_CENTER, 10)

        # ----------------------------------------------------------------------
        # Create bar wrapper
        wrapper_sizer = wx.BoxSizer(wx.VERTICAL)
        # Add each of the Bars "which are horizontal sizer to one wrapping vertical wrapper_sizer
        wrapper_sizer.Add(siz_title_bar, 0, wx.ALL, 5)
        wrapper_sizer.Add(siz_spt_all_bar, 0, wx.ALL, 5)
        wrapper_sizer.Add(siz_spt_single_bar, 0, wx.ALL, 5)
        wrapper_sizer.Add(siz_spt_inc_bar, 0, wx.ALL, 5)
        wrapper_sizer.Add(siz_out_put_bar, 0, wx.ALL, 5)
        # ----------------------------------------------------------------------

        # Set main wrapper_sizer of the dialog this ends the GUI layout bit of the dialog construction
        self.SetSizer(wrapper_sizer)

    # ----------------------------------------------------------------------
    # Need to build the events DEF's for the buttons bellow!
    # ----------------------------------------------------------------------


    def FileOutRoot(self, event):

        dlg = wx.DirDialog(self, "Choose a directory:",
                           style=wx.DD_DEFAULT_STYLE
                           # | wx.DD_DIR_MUST_EXIST
                           # | wx.DD_CHANGE_DIR
                           )
        if dlg.ShowModal() == wx.ID_OK:
            outputlocation = dlg.GetPath()
            self.spt_dia_out_txt.SetLabel(outputlocation)
            return outputlocation

        dlg.Destroy()

    def IndFileSplit(self, event, file_list, current_selection, out_location):
        # x is a loop counter to find the file in the file list
        x = 0
        # y is a loop counter to work through the number of pages
        y = 0
        # j augments y by 1 so that the split prefix starts at 1
        j = 1

        for x in range(len(file_list)):
            if file_list[x].name == current_selection:

                doc_path_hold = PdfFileReader(open(file_list[x].path, "rb"))
                if not out_location == "File output location! " or out_location == "":
                    NumPages = doc_path_hold.getNumPages()
                    for y in range((NumPages)):
                        Spliter = PdfFileWriter()
                        # outCheck = out_location.GetLabel()
                        target = str(out_location) + '\\' + str("(%s) " + (file_list[x].name)) % j
                        canvas = Canvas(target)
                        canvas.showPage()
                        canvas.save()
                        Spliter.addPage(doc_path_hold.getPage(y))
                        # Loads the traget into the PDF writer
                        output = file(target, "wb")
                        # Over writes the bank PDF with a new one !
                        Spliter.write(output)
                        j = j + 1
                        event.Skip()
        else:
            # event.Skip()
            pass

    def SinFileSplit(self, event, file_list, current_selection, out_location, page_to_split):

        # x is a loop counter to find the file in the file list
        x = 0
        # y is a loop counter to work through the number of pages
        y = 0
        # j augments y by 1 so that the split prefix starts at 1
        j = 1

        for x in range(len(file_list)):
            if file_list[x].name == current_selection:

                doc_path_hold = PdfFileReader(open(file_list[x].path, "rb"))
                if not out_location == "File output location! " or out_location == "":
                    Spliter = PdfFileWriter()
                    target = str(out_location) + '\\' + str("(%s) " + (file_list[x].name)) % j
                    canvas = Canvas(target)
                    canvas.showPage()
                    canvas.save()
                    Spliter.addPage(doc_path_hold.getPage(page_to_split - 1))
                    output = file(target, "wb")
                    # Over writes the bank PDF with a new one !
                    Spliter.write(output)

                    event.Skip()

    def BetFileSplit(self, event, file_list, current_selection, out_location, page_to_split_min, page_to_split_max):
        # x is a loop counter to find the file in the file list
        x = 0
        # y is a loop counter to work through the number of pages
        y = 0
        # j augments y by 1 so that the split prefix starts at 1
        j = 1

        for x in range(len(file_list)):
            if file_list[x].name == current_selection:

                doc_path_hold = PdfFileReader(open(file_list[x].path, "rb"))
                if not out_location == "File output location! " or out_location == "":
                    num_pages = doc_path_hold.getNumPages()
                    spliter = PdfFileWriter()
                    for y in range(num_pages):
                        if y >= page_to_split_min and y <= page_to_split_max:
                            spliter.addPage(doc_path_hold.getPage(y))

                    target = str(out_location) + '\\' + str("(%s) " + (file_list[x].name)) % j
                    canvas = Canvas(target)
                    canvas.showPage()
                    canvas.save()

                    # Loads the target into the PDF writer
                    output = file(target, "wb")
                    # Over writes the bank PDF with a new one !
                    spliter.write(output)
                    j = j + 1
                    event.Skip()
        else:

            pass

class AboutDialog(wx.Dialog):
    def __init__(self, parent, title):
        super(AboutDialog, self).__init__(parent, title=title, size=(600, 300))
        # Create a new panel
        panel = wx.Panel(self)
        wrapper_sizer = wx.BoxSizer(wx.VERTICAL)
        self.abt_dia_txt_one = wx.StaticText(self, label="  TuckPDF is written by Mark Tucker and is not for commercial "
                                                       "release and should not be resold for any other individuals "
                                                       "remuneration other than that of the author Mark Tucker.")

        self.abt_dia_txt_two = wx.StaticText(self, label="     By using this program you agree to the following terms:")

        self.abt_dia_txt_three = wx.StaticText(self, label="     1- You will not redistribute the program without the authors permission ")
        self.abt_dia_txt_four = wx.StaticText(self, label="     2- You will not use the program to make monetary gains without the authors permission")
        self.abt_dia_txt_five = wx.StaticText(self, label="     3- The author is not responsible for any loss of data from using this program")
        self.abt_dia_txt_six = wx.StaticText(self, label="     4- The author is not responsible for any damages caused from using this program")
        self.abt_dia_txt_seven = wx.StaticText(self, label="     5- The author is under no responsibility to maintain or update the program")
        #self.abt_dia_txt_eight = wx.StaticText(self, label="")



        wrapper_sizer.Add(self.abt_dia_txt_one, 0, wx.ALIGN_CENTER, 10)
        wrapper_sizer.AddSpacer(10)
        wrapper_sizer.Add(self.abt_dia_txt_two, 0, wx.ALIGN_LEFT, 10)
        wrapper_sizer.AddSpacer(10)
        wrapper_sizer.Add(self.abt_dia_txt_three, 0, wx.ALIGN_LEFT, 10)
        wrapper_sizer.Add(self.abt_dia_txt_four, 0, wx.ALIGN_LEFT, 10)
        wrapper_sizer.Add(self.abt_dia_txt_five, 0, wx.ALIGN_LEFT, 10)
        wrapper_sizer.Add(self.abt_dia_txt_six, 0, wx.ALIGN_LEFT, 10)
        wrapper_sizer.Add(self.abt_dia_txt_seven, 0, wx.ALIGN_LEFT, 10)

        self.SetSizer(wrapper_sizer)
########################################################################################################################
# Class for the "Windows Fame" that we then add our panel and menu bar to
########################################################################################################################

class MainFrame(wx.Frame):

    ########################################################################
    # creates a instance of the panel "that's what the __init__ means".
    # because of this, it means that the code in this function is only
    # called when the program is started and the GUI loads for the first time
    # means it cannot be used for any calculations i believe!
    # ----------------------------------------------------------------------
    def __init__(self):

        wx.Frame.__init__(self, None, title="TuckPDF Splitter And Merger, Time To Tuck In!", size=(800, 600))

        panel = MainPanel(self)

        # create a menu bar that sits inside of the frame. I believe this is part of the windows widget and cannot be
        # moved to the panel instead
        menu_bar = wx.MenuBar()
        #menu_bar.SetBackgroundColour((230,240,30,255))
        # Menu buttons created here!
        file_menu_button = wx.Menu()
        edit_menu_button = wx.Menu()
        help_menu_button = wx.Menu()
        # self.Bind(wx.EVT_MENU, lambda event: self.OnAbout(event), about_menu_button)
        # Menu sub button items
        # List buttons for file sub menu
        # Open button for the adding of PDF's to the file list, this will operate via modal
        open_sub_btn = file_menu_button.Append(wx.ID_OPEN, 'Open', 'Add a file to the list')
        # Bind event to button
        self.Bind(wx.EVT_MENU, lambda event: self.OnOpen(event, panel), open_sub_btn)

        # Exit button that close the program
        exit_sub_btn = file_menu_button.Append(wx.ID_EXIT, 'Exit', 'Exit Program')
        # bind event to button
        self.Bind(wx.EVT_MENU, self.OnExit, exit_sub_btn)

        # List buttons for edit sub menu
        # merge button that will call the OnMerge function in the main panel class
        merge_sub_btn = edit_menu_button.Append(wx.ID_ANY, 'Merge', 'Merge Files')
        self.Bind(wx.EVT_MENU, lambda event: self.OnMergeMenu(event, panel), merge_sub_btn)
        # merge button that will call the OnSplit function in the main panel class
        split_sub_btn = edit_menu_button.Append(wx.ID_ANY, 'Split', 'Split Files')
        # Bind event to button
        self.Bind(wx.EVT_MENU, lambda event: self.OnSplitMenu(event, panel), split_sub_btn)

        about_sub_btn = help_menu_button.Append(wx.ID_ANY, 'About', 'About the program')
        # Bind event to button
        self.Bind(wx.EVT_MENU, lambda event: self.OnAbout(event, panel), about_sub_btn)



        # Add the menu buttons to the menu bar!
        menu_bar.Append(file_menu_button, 'File')
        menu_bar.Append(edit_menu_button, 'Edit')
        menu_bar.Append(help_menu_button, 'Help')
        self.SetMenuBar(menu_bar)
        #menu_bar.SetBackgroundColour("blue")
        # The the frame that when it is loaded it should appear in the centre of the screen!
        self.Centre(True)

        self.Show()

    def OnMergeMenu(self, e, panel):
        '''Passed in the MainPanel class as panel into this function, this then allows us to extract all the variables
        generated inside the main panel. We then call the MainPanel OnMerge function from the menu button and pass in
        the extracted variables.'''
        file_list = panel.file_list
        file_name = panel.file_name.GetValue()
        file_root_txt = panel.file_root_txt.GetLabel()
        panel.OnMerge(self, file_list, file_name, file_root_txt)

    def OnSplitMenu(self, e, panel):
        '''Passed in the MainPanel class as panel into this function, this then allows us to extract all the variables
        generated inside the main panel. We then call the MainPanel OnSplit function from the menu button and pass in
        the extracted variables.'''
        file_list = panel.file_list
        file_current_selection = panel.current_selection
        panel.OnSplit(self, file_list, file_current_selection)

    def OnOpen(self, e, panel):
        open_file_dialog = wx.FileDialog(self, "Open PDF file", "", "",
                                       "Pdf files (*.pdf)|*.pdf", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)



        if open_file_dialog.ShowModal() == wx.ID_CANCEL:
            return  # the user changed idea...
        object_index = 0
        file_to_add = open_file_dialog
        file_path = file_to_add.GetPath()
        #PDFDropArea.OnDropFiles(panel.file_drop_target , 0, 0, file_path)
        #panel.updateDisplay(str(file_path))
        x = 11

        file_stats = os.stat(file_path)
        file_path = os.path.abspath(file_path)
        file_type = os.path.splitext(file_path)[1]
        if file_type == ".pdf":

            creation_time = time.strftime("%m/%d/%Y %I:%M %p",
                                      time.localtime(file_stats[stat.ST_CTIME]))
            modified_time = time.strftime("%m/%d/%Y %I:%M %p",
                                      time.localtime(file_stats[stat.ST_MTIME]))

            file_size = file_stats[stat.ST_SIZE]

            if file_size > 1024:
                file_size = file_size / 1024.0
                file_size = "%.2f KB" % file_size

            panel.file_list.append(FileInfo(file_path,
                                            file_path,
                                            creation_time,
                                            modified_time,
                                            file_size,
                                            str(object_index)))

        else:

            panel.showMessageDlg("This is not a PDF file", "Unknown File Type", wx.OK | wx.CANCEL | wx.ICON_QUESTION)

        panel.olv.SetObjects(panel.file_list)

    def OnExit(self, e):
        # Closes the program !
        self.Close(True)

    def OnAbout(self, e, panel):
        a = AboutDialog
        about_modal = AboutDialog(self, "About TuckPDF").ShowModal()



# ----------------------------------------------------------------------
def main():
    # Need to work out what wx.App does ??
    TuckPDFApp = wx.App(False)
    # Call the main frame class, which calls the MainPanel which holds the widgets."Think of it like russian dolls"!
    frame = MainFrame()

    # Initialize the GUI loop!!
    TuckPDFApp.MainLoop()


if __name__ == "__main__":
    main()
