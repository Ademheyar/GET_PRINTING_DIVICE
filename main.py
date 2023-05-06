import usb.core
import json
from escpos.printer import Usb

# File path to store the USB device data
saved_data_file = 'usb_devices.json'

# Specify the Vendor ID and Product ID of your USB device
vendor_id = 0x04b8
product_id = 0x0e02

# Load the previously saved USB device data
try:
    with open(saved_data_file, 'r') as file:
        saved_devices = json.load(file)
except FileNotFoundError:
    saved_devices = []

# Find all connected USB devices
devices = usb.core.find(find_all=True)

# Set to store new USB devices
new_devices = []

# Iterate over the connected devices
for device in devices:
    # Get the device information
    current_vendor_id = device.idVendor
    current_product_id = device.idProduct

    # Check if the device is new and accessible
    if {'vendor_id': current_vendor_id, 'product_id': current_product_id} not in saved_devices:
        try:
            # Try to connect to the printer
            printer = Usb(current_vendor_id, current_product_id)

            # Print the new device information
            print("New USB device found:")
            print("Vendor ID: 0x{:04x}".format(current_vendor_id))
            print("Product ID: 0x{:04x}".format(current_product_id))
            print()
            vendor_id = current_vendor_id
            product_id = current_product_id
            # Disconnect from the printer
            printer.close()

                        
            # Find the USB device with the specified Vendor ID and Product ID
            device = usb.core.find(idVendor=vendor_id, idProduct=product_id)

            # Check if the device is found
            if device is None:
                print("USB device not found.")
            else:
                
                print("USB device found.")
                # Connect to the printer
                printer = Usb(vendor_id, product_id)

                # Set text size to 2x
                printer.text("\x1d\x21\x11")

                # Set text alignment to center
                printer.text("\x1b\x61\x01")

                # Print your desired text
                printer.text("Hello, world!")

                # Cut the paper
                printer.cut()

                # Disconnect from the printer
                printer.close()
            
        except:
            # If successful, add it to the new devices list
            new_devices.append({'vendor_id': current_vendor_id, 'product_id': current_product_id})

            print("Ignore devices that are not accessible.")
            # Ignore devices that are not accessible
            pass

# Update the saved device data
saved_devices.extend(new_devices)

# Save the updated device data
with open(saved_data_file, 'w') as file:
    json.dump(saved_devices, file, indent=4)
