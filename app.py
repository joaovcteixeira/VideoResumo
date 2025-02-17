from flask import Flask, request, jsonify
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
import os

app = Flask(__name__)

genai.configure(api_key='AIzaSyCDRcqRw2YmRbixhM_v-I8B3AIGniqf24Y')

def extrair_transcricao(video_url):
    try:
        video_id = video_url.split('v=')[-1]
        transcricao = YouTubeTranscriptApi.get_transcript(video_id,languages=['pt'])
        texto = ' '.join([item['text']for item in transcricao])
        return texto
    except Exception as e:
        return str(e)

def resumir_texto(texto):
    try:
        modelo = genai.GenerativeModel('gemini-pro')
        prompt = ('Resuma o seguinte texto detalhadamente em um formato bem estruturado, '
        'com parágrafos claros e separados (não precisa informar o número do parágrafo): \n\n'+texto)
        resposta = modelo.generate_content(prompt)
        return resposta.text
    except Exception as e:
        return str(e)


@app.route('/resumir', methods=['POST'])
def gerar_resumo():
    try:
        video_url = request.json.get('link', '')

        if not video_url:
            return jsonify({'erro': 'Nenhuma URL fornecida'}), 400

        if 'youtube.com/watch?v=' in video_url:
            video_id = video_url.split('v=')[-1].split('&')[0]
        elif 'youtu.be/' in video_url:
            video_id = video_url.split('youtu.be/')[-1].split('?')[0]
        else:
            return jsonify({'erro': 'URL inválida'}), 400

        transcricao = extrair_transcricao(video_id)
        if not transcricao:
            return jsonify({'erro': 'Erro ao obter transcricao'}), 500

        resumo = resumir_texto(transcricao)
        if not resumo:
            return jsonify({'erro': 'Erro ao gerar resumo'}), 500

        return jsonify({'resumo': resumo})

    except Exception as e:
        return jsonify({'erro': f'Erro interno {str(e)}'}), 500

@app.route('/teste', methods=['GET'])
def teste_youtube():
    url = 'https://www.youtube.com/watch?v=FDVTxKRRENo'
    try:
        resposta = requests.get(erl)
        return jsonify({'status_code': resposta.status_code})
    except Exception as e:
        return jsonify({'erro': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)