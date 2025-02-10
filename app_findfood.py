import tkinter as tk
from tkinter import ttk
from busca_places import buscar_restaurantes
from ibge_api import obter_estados, obter_cidades

def atualizar_cidades(event):
    uf = estado_var.get()
    cidades = obter_cidades(uf)
    cidade_combobox['values'] = cidades
    cidade_combobox.set('')

def buscar():
    estado = estado_var.get()
    cidade = cidade_var.get()

    if not estado or not cidade:
        lista_restaurantes.delete(0, tk.END)
        lista_restaurantes.insert(tk.END, 'Selecione um estado e uma cidade.')
        return

    resultados = buscar_restaurantes(estado, cidade)

    lista_restaurantes.delete(0, tk.END)
    for restaurante in resultados:
        lista_restaurantes.insert(tk.END, restaurante)

root = tk.Tk()
root.title('Busca de Restaurantes')

estados = obter_estados()

ttk.Label(root, text='Estado').grid(row=0, column=0, padx=5, pady=5)
estado_var = tk.StringVar()
estado_combobox = ttk.Combobox(root, textvariable=estado_var, values=list(estados.keys()), state='readonly')
estado_combobox.grid(row=0, column=1, padx=5, pady=5)
estado_combobox.bind('<<ComboboxSelected>>', atualizar_cidades)

ttk.Label(root, text='Cidade').grid(row=1, column=0, padx=5, pady=5)
cidade_var = tk.StringVar()
cidade_combobox = ttk.Combobox(root, textvariable=cidade_var, state='readonly')
cidade_combobox.grid(row=1, column=1, padx=5, pady=5)

btn_buscar = ttk.Button(root, text='Buscar Restaurantes', command=buscar)
btn_buscar.grid(row=2, column=0, columnspan=2, pady=10)

lista_restaurantes = tk.Listbox(root, width=50, height=10)
lista_restaurantes.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()