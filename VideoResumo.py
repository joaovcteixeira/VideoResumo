import tkinter as tk
from tkinter import scrolledtext, messagebox
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
import os
os.environ['GRPC_ENABLE_FORK_SUPORT'] = 'O'

genai.configure(api_key='AIzaSyCDRcqRw2YmRbixhM_v-I8B3AIGniqf24Y')

def extrair_transcricao(video_url):
    video_id = video_url.split('v=')[-1]
    try:
        transcricao = YouTubeTranscriptApi.get_transcript(video_id,languages=['pt'])
        texto = ' '.join([item['text']for item in transcricao])
        return texto
    except Exception as e:
        messagebox.showerror(f'Erro ao obter transcrição: {e}')
        return None

def resumir_texto(texto):
    try:
        modelo = genai.GenerativeModel('gemini-pro')
        prompt = ('Resuma o seguinte texto detalhadamente em um formato bem estruturado, '
        'com parágrafos claros e separados (não precisa informar o número do parágrafo): \n\n'+texto)
        resposta = modelo.generate_content(prompt)
        return resposta.text
    except Exception as e:
        messagebox.showerror('Erro',f'Erro ao gerar resumo: {e}')
        return None

def gerar_resumo():
    video_id = entrada_video.get().strip()
    if not video_id:
        messagebox.showwarning('Atenção','Digite um ID de vídeo válido!')
        return
    resumo_texto.config(state=tk.NORMAL)
    resumo_texto.delete(1.0, tk.END)

    transcricao = extrair_transcricao(video_id)
    if transcricao:
        resumo = resumir_texto(transcricao)
        if resumo:
            resumo_texto.insert(tk.END, resumo)

    resumo_texto.config(state=tk.DISABLED)

janela = tk.Tk()
janela.title('Resumo de Vídeos do Youtube')
janela.geometry('600x400')

tk.Label(janela, text='ID do Vídeo do Youtube: ').pack(pady=5)
entrada_video = tk.Entry(janela, width=50)
entrada_video.pack(pady=5)

botao_resumir = tk.Button(janela, text='Gerar Resumo', command=gerar_resumo)
botao_resumir.pack(pady=10)

resumo_texto = scrolledtext.ScrolledText(janela, width=70, height=70, wrap=tk.WORD)
resumo_texto.pack(pady=10)
resumo_texto.config(state=tk.DISABLED)

janela.mainloop()