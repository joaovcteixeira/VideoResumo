import tkinter as tk

janela = tk.Tk()
janela.title('Teste Tkinter')
janela.geometry('300x200')

label =tk.Label(janela, text='Se você vê isso, Tkinter está funcionando!', font=('Arial',12))
label.pack(pady=20)

janela.mainloop()