import serial
import time

ser = serial.Serial('COM3', 9600)
time.sleep(2)

with open("output.txt", "a") as file:
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            print(f"Recebido: {data}")
            file.write(data + "\n")
