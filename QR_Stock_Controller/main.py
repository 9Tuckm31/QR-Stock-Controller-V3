import wx
import GUI

def main():
    # Need to work out what wx.App does ??

    Tuck_QR_Stock_Controller = wx.App(False)
    # Call the main frame class, which calls the MainPanel which holds the widgets."Think of it like russian dolls"!
    frame = GUI.MainFrame()

    # Initialize the GUI loop!!
    Tuck_QR_Stock_Controller.MainLoop()

    # ------------------------------------------------------------------------
    # Ask user for a login details here
    # ------------------------------------------------------------------------

    # ------------------------------------------------------------------------
    # Need to test to see if a connection can be made to the server here !
    # ------------------------------------------------------------------------

    # ------------------------------------------------------------------------
    # Failing to connect to the server needs to (A) be if the user login
    # info is invalid and (B) to say if it cannot find the server
    # ------------------------------------------------------------------------

    # ------------------------------------------------------------------------
    # Need to see if the correctly named data base and all the tables are
    # present on the server. If this return true run as normal else,
    # The program needs to run a set up of the data base or the missing tables
    # ------------------------------------------------------------------------


if __name__ == "__main__":
    main()
