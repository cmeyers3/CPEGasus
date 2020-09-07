import serial

def main():
    
    print("hi") 
    ser = serial.Serial('/dev/ttyUSB0')
    print(ser.name)
    
    ser.write(b'Hello')
    ser.close()


if __name__ == '__main__':
    main()
