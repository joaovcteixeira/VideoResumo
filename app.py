from flask import Flask, request, jsonify
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

genai.configure(api_key='AIzaSyCDRcqRw2YmRbixhM_v-I8B3AIGniqf24Y')

def extrair_transcricao(video_url):
    video_id = video_url.split('v=')[-1]
    try:
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
    video_url = request.json.get('link','')
    if not video_url:
        return jsonify({'erro': 'Nenhuma URL fornecida'}), 400
    video_id = video_url.split('v=')[-1]

    transcricao = extrair_transcricao(video_id)
    if 'error' in transcricao.lower():
        return jsonify({'erro': 'Erro ao obter transcrição'}), 500

    resumo = resumir_texto(transcricao)
    return jsonify({'resumo': resumo})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)