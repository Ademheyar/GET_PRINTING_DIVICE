import tkinter as tk
import win32print
import time
import ctypes

# Create the main window
root = tk.Tk()
root.title("Printer Selection")

# Initialize printer variable
printer_name = None

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
  
def wait_for_printer_ready(printer_name, timeout=30, max_attempts=10):
    attempts = 0
    while attempts < max_attempts:
        printer_handle = win32print.OpenPrinter(printer_name)
        printer_info = win32print.GetPrinter(printer_handle, 2)
        win32print.ClosePrinter(printer_handle)
        print("printer status : " + str(printer_info))
        print("printer status : " + str(win32print.PRINTER_STATUS_PAUSED))
        print("printer status : " + str(win32print.PRINTER_STATUS_OFFLINE))
        print("printer status : " + str(win32print.PRINTER_ATTRIBUTE_WORK_OFFLINE))
        if printer_info['Status'] == win32print.PRINTER_STATUS_PAUSED or printer_info['Status'] == 0:
            return True
        if printer_info['Status'] == win32print.PRINTER_STATUS_OFFLINE:
            win32print.SetPrinter(printer_name, None, {'Attributes': printer_info.Attributes & ~win32print.PRINTER_ATTRIBUTE_WORK_OFFLINE})
        time.sleep(1)
        attempts += 1
    # Printer is still offline after maximum number of attempts
    print(f"Error: Printer '{printer_name}' is offline and could not be brought online.")
    return False

# Function to print the entry value using the selected printer driver
def print_entry():
    # Load the saved printer driver choice
    with open('printer.txt', 'r') as f:
        printer_name = f.read().strip()
    wait_for_printer_ready(printer_name)
    print("printer_name|" + str(printer_name) + "|")
    # Print the entry value using the saved printer driver
    printer_handle = win32print.OpenPrinter(printer_name)
    data = entry.get()
    job_id = win32print.StartDocPrinter(printer_handle, 1, ('print', None, 'RAW'))
    job_info = win32print.JOB_INFO_1
    
    win32print.WritePrinter(printer_handle, data.encode())
    win32print.FlushPrinter(printer_handle, b"", 1)
    win32print.EndPagePrinter(printer_handle)
    win32print.EndDocPrinter(printer_handle)
    win32print.ClosePrinter(printer_handle)
    print("printer job_info : " + str(job_info))
    print("printer status : " + str(win32print.JOB_STATUS_COMPLETE))
    # Wait for the printer to become ready again
    '''while True:
        win32print.GetJob(printer_handle, job_id, 1, ctypes.byref(job_info))
        if job_info.Status == win32print.JOB_STATUS_COMPLETE:
            break
        time.sleep(1)'''
      

# Create the entry widget
entry = tk.Entry(root, width=50)
entry.pack(pady=10)


# Create the first button to choose a printer driver
printer_name = tk.StringVar()
choose_printer_button = tk.Button(root, text="Choose Printer", command=choose_printer)
choose_printer_button.pack()

# Create the second button to print the entry value using the selected printer driver
print_button = tk.Button(root, text="Print Entry", command=print_entry)
print_button.pack(pady=10)

# Start the main loop
root.mainloop()
