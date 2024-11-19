import serial
import time
import threading
import tkinter as tk
from datetime import datetime
import pygame as pg
import pandas as pd

ultimo_dado = None

def ler_serial():
    global ultimo_dado
    ser = serial.Serial('COM11', 9600)
    time.sleep(2)

    with open("../temp.txt", "a") as file:
        while True:
            if ser.in_waiting > 0:
                data = ser.readline().decode('utf-8').strip()
                print(data, ultimo_dado)

                if data not in ["LIMPAR", "CONFIRMAR"]:
                    file.write(data)
                    file.close()
                    file = open("../temp.txt", "a")
                    ultimo_dado = None

                else:
                    if data != ultimo_dado:
                        if data == "LIMPAR":
                            limpar_arquivo_txt("../temp.txt")
                        elif data == "CONFIRMAR":
                            salvar_e_tocar()
                        ultimo_dado = data

def tocar_som(caminho_som):
    pg.mixer.init()
    pg.mixer.music.load(caminho_som)
    pg.mixer.music.play()
    while pg.mixer.music.get_busy():
        time.sleep(1)

def atualizar_interface():
    numero = ler_arquivo_txt("../temp.txt")
    label_numero.config(text=numero)
    root.after(1000, atualizar_interface)

def salvar_e_tocar():
    numero = ler_arquivo_txt("../temp.txt")
    salva_voto(numero, "../votos.xlsx")
    tocar_som("../som-de-urna.mp3")
    limpar_arquivo_txt("../temp.txt")

def limpar_arquivo_txt(caminho_arquivo):
    with open(caminho_arquivo, 'w') as file:
        file.write("")

def ler_arquivo_txt(caminho_arquivo):
    with open(caminho_arquivo, 'r') as file:
        conteudo = file.read().strip()
    return conteudo

def salva_voto(conteudo, caminho_excel):
    data_e_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df = pd.DataFrame([[conteudo, data_e_hora]], columns=["Número", "Horário"])

    with pd.ExcelWriter(caminho_excel, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
        df.to_excel(writer, index=False, header=False, startrow=writer.sheets['Sheet1'].max_row)

root = tk.Tk()
root.title("Urna Eletrônica")
root.geometry("400x300")

label_titulo = tk.Label(root, text="Urna Eletrônica", font=("Helvetica", 16))
label_titulo.pack(pady=20)

label_numero = tk.Label(root, text="Número: ", font=("Helvetica", 24))
label_numero.pack(pady=20)

label_status = tk.Label(root, text="", font=("Helvetica", 12))
label_status.pack(pady=10)

atualizar_interface()

serial_thread = threading.Thread(target=ler_serial, daemon=True)
serial_thread.start()

root.mainloop()
