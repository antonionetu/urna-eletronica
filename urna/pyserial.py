import serial
import time

# import main

ser = serial.Serial('COM11', 9600)
time.sleep(2)

with open("../temp.txt", "a") as file:
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            print(data, data in ["LIMPAR", "CONFIRMAR"])
            
            if data not in ["LIMPAR", "CONFIRMAR"]:
                file.write(data)
                file.close()
                file = open("../temp.txt", "a")           

            else:
                if data == "LIMPAR":
                    #limpar_arquivo("../temp.txt")
                    ...

                elif data == "CONFIRMAR":
                    #salvar_e_tocar()
                    ...
