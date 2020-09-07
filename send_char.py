import serial
import time

def main():
    ser = serial.Serial('/dev/ttyUSB0')
    print(ser.name)
    
    while True:
        time.sleep(1)
        ser.write(b'Hello')
        ser.close()


if __name__ == '__main__':
    main()
