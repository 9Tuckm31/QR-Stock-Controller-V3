import wx
import GUI

from GUI import MainFrame
from GUI import MainPanel
from Modals import LoginDialog

def main():
    # Need to work out what wx.App does ??
    TuckDataBaseManager = wx.App(False)


    # Call the main frame class, which calls the MainPanel which holds the widgets."Think of it like russian dolls"!
    frame = MainFrame()

    # Initialize the GUI loop!!
    TuckDataBaseManager.MainLoop()

if __name__ == "__main__":
    main()