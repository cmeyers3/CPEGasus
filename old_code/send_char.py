import os
import re
import time

import serial
import serial.tools.list_ports
from serial import SerialException


linux_port_dir = "/dev/"

baud_rate = 57600


# Get port name
def get_port_name():
    # If Linux: /dev/ttyUSB* or /dev/ttyACM*
    if os.name == 'posix':
        serial_ports = os.listdir(linux_port_dir)
        print("Ports: {}".format(serial_ports))
        for port in serial_ports:
            if re.match("(ttyUSB[0-9]+|ttyACM[0-9]+)", port):
                return port
            
    # If Windows: COM*
    elif os.name == 'nt':
        serial_ports = [p.device for p in serial.tools.list_ports.comports()]
        if len(serial_ports) > 1:
            raise SystemExit("Found multiple serial ports: {}. Exiting.".format(serial_ports))
        elif len(serial_ports) < 1:
            raise SystemExit("Found no valid serial ports. Exiting.")
        return serial_ports[0]

    # If fall through, no port found. Exit with error.
    raise SystemExit("Could not find port. Exiting.")
    

def main():
    port = get_port_name()
    try:
        ser = serial.Serial(port, baud_rate)
        print("Opening port {}".format(port))
    except SerialException:
        print("Port {} already open".format(port))
        raise SystemExit
    
    string = b'D'
    for i in range(10):
        time.sleep(1)
        ser.write(string)
        print(ser.readline())
        

if __name__ == '__main__':
    main()
