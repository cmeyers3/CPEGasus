import serial
import time

def main():
    ser = serial.Serial('/dev/ttyACM0')
    print("python: {}/n".format(ser.name))
    ser.write(b'A')
    print("python: wrote D") 
    print("from Arduino:{}/n".format(ser.readline())) 
    print("from Arduino: {}/n".format(ser.readline()))
    print("from Arduino: {}/n".format(ser.readline()))

if __name__ == '__main__':
    main()
