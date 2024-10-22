import tkinter as tk
import serial
import pandas as pd
import time
from datetime import datetime
import os

# Configuração da porta serial
ser = serial.Serial('/dev/ttyACM0', 9600)  # Substitua 'COM3' pela sua porta
time.sleep(2)  # Aguarda a conexão ser estabelecida

# Lista para armazenar votos
votos = []

def confirmar_voto(voto):
    # Adiciona o voto à lista
    votos.append(voto)
    ser.write(voto.encode())
    atualizar_lista()

def atualizar_lista():
    # Atualiza a lista para mostrar todos os votos em uma única linha
    lista_votos.delete(0, tk.END)
    lista_votos.insert(tk.END, " ".join(votos))

def salvar_votos():
    # Adiciona data/hora aos votos antes de salvar
    agora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    voto_completo = " ".join(votos)  # Concatena todos os votos em uma única string
    dados = [{"Voto": voto_completo, "Horário": agora}]
    df = pd.DataFrame(dados)
    df.to_excel("votos.xlsx", index=False)
    status_label.config(text="Votos salvos em votos.xlsx")
    
    # Tocar som
    tocar_som()
    
    # Limpar votos
    votos.clear()
    atualizar_lista()

def tocar_som():
    # Substitua pelo caminho do seu arquivo de som .wav
    os.system('aplay ./som_confirma.mp4')  

# Interface gráfica
root = tk.Tk()
root.title("Urna Eletrônica")

tk.Label(root, text="Escolha seu voto:").pack()

# Gera os 10 botoes digitalmente
#for i in range(10):
#    tk.Button(root, text=str(i), command=lambda i=i: confirmar_voto(str(i))).pack()


# o botao de salvar digitalmente
# tk.Button(root, text="Salvar Votos", command=salvar_votos).pack()

lista_votos = tk.Listbox(root)
lista_votos.pack()

status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()
