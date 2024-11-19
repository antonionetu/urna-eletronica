import serial
import time

from main import limpar_arquivo, salvar_e_tocar

ser = serial.Serial('COM3', 9600)
time.sleep(2)

with open("../temp.txt", "a") as file:
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            
            if data not in ["LIMPAR", "CONFIRMAR"]:
                file.write(data)

            else:
                if data == "LIMPAR":
                    limpar_arquivo("../temp.txt")

                elif data == "CONFIRMAR":
                    salvar_e_tocar()
