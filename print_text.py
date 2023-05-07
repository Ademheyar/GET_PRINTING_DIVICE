import win32print
import tkinter as tk

# Create a hidden Tkinter root window
root = tk.Tk()
root.withdraw()

printer_name = ""

# Function to choose a printer driver and save the choice
def choose_printer():
    # Get a list of available printer drivers
    printer_list = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None, 1)
    printer_names = [printer[2] for printer in printer_list]
    # Create a dropdown list to choose a printer driver
    printer_var = tk.StringVar(value=printer_names[0])
    printer_menu = tk.OptionMenu(root, printer_var, *printer_names)
    printer_menu.pack(pady=10)
    # Save the printer driver choice
    def save_printer():
        printer_name = printer_var.get()
        with open('printer.txt', 'w') as f:
            f.write(printer_name)
        printer_menu.destroy()
    ok_button = tk.Button(root, text="OK", command=save_printer)
    ok_button.pack(pady=10)

    
def print_text_with_dialog(text):
    choose_printer()
    # Load the saved printer driver choice
    with open('printer.txt', 'r') as f:
        printer_name = f.read().strip()
    # Get the default printer name
    #printer_name = win32print.GetDefaultPrinter()

    # Prepare the printer properties
    printer_props = {
        "DesiredAccess": win32print.PRINTER_ALL_ACCESS,
        "PrinterName": printer_name,
        "Attributes": win32print.PRINTER_ATTRIBUTE_DIRECT,
    }

    # Open the printer and get a handle to it
    print("Open the printer and get a handle to it\n")
    printer_handle = win32print.OpenPrinter(printer_name)
    try:
        print("Prepare the document info\n")
        # Prepare the document info
        doc_info = ('print', None, 'RAW')
        
        print("Start the print job\n")
        # Start the print job
        job_handle = win32print.StartDocPrinter(printer_handle, 1, doc_info)

        try:
            print("Start a new page\n")
            # Start a new page
            win32print.StartPagePrinter(printer_handle)
            
            print("Send the text to the printer\n")
            # Send the text to the printer
            twiths = (text + ".\n.\n")
            win32print.WritePrinter(printer_handle, twiths.encode("utf-8"))


 
            # Send a paper-cut command to the printer
            # You may need to adjust the command based on the printer model
            print("Send a paper-cut command to the printere\n")
            print("You may need to adjust the command based on the printer model\n")
            paper_cut_command = b'\x1D\x56\x01'
            win32print.WritePrinter(printer_handle, paper_cut_command)

            # Send a command to open the cash drawer
            # Adjust the command based on the printer and cash drawer model
            print("Send a command to open the cash drawer\n")
            print("You may need to adjust the command based on the printer model\n")
            cash_drawer_command = b'\x1B\x70\x00\x19\xFA'
            win32print.WritePrinter(printer_handle, cash_drawer_command)

        finally:
            print("End the print job\n")
            # End the print job
            win32print.EndDocPrinter(printer_handle)

    finally:
        print("Close the printer handle\n")
        # Close the printer handle
        win32print.ClosePrinter(printer_handle)

# Example usage
text_to_print = \
              "     Company name\n" + \
              "----------------------\n"\
              "Receipt No. : ??????\n" + \
              "YEAR-MONTH-DAY TIME PM\AM\n" + \
              "USER: \n" + \
              "CUSTEMER: \n" + \
              "-----------------------\n" + \
              "Items       QTY        PRICE\n" + \
              "Item0       2          0\n" + \
              "Item1       1          1\n" + \
              "Item2       1          1\n" + \
              "-----------------------\n" + \
              "TOTAL Items            3\n" + \
              "TOTAL price            2\n" + \
              "-----------------------\n" + \
              "paid amount:           2\n" + \
              "amount due:            2\n" + \
              "-----------------------\n" + \
              "thank you for shoping with us\n"

# Call the function to print the text with the printer driver dialog
print_text_with_dialog(text_to_print)


# Start the main loop
root.mainloop()
