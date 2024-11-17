import os
import time
from datetime import datetime

import tkinter as tk
import pandas as pd
import pygame as pg


def ler_arquivo_txt(caminho_arquivo):
    with open(caminho_arquivo, 'r') as file:
        conteudo = file.read().strip()
    return conteudo


def salva_voto(conteudo, caminho_excel):
    data_e_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df = pd.DataFrame([[conteudo, data_e_hora]], columns=["Número", "Horário"])

    with pd.ExcelWriter(caminho_excel, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
        df.to_excel(writer, index=False, header=False, startrow=writer.sheets['Sheet1'].max_row)


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

root.mainloop()
