from flask import Flask, request, jsonify
import yt_dlp
import os
import google.generativeai as genai

# Configurar a chave da API Gemini
API_KEY = "SUA_CHAVE_GEMINI_AQUI"
genai.configure(api_key=API_KEY)

app = Flask(__name__)


def baixar_legendas(video_id):
    """Baixa legendas automáticas do YouTube usando yt_dlp"""
    ydl_opts = {
        'skip_download': True,  # Não baixa o vídeo, apenas as legendas
        'writesubtitles': True,  # Baixa legendas
        'subtitleslangs': ['pt', 'en'],  # Tenta primeiro PT, depois EN
        'outtmpl': f"{video_id}.vtt",  # Nome do arquivo de legendas
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([f"https://www.youtube.com/watch?v={video_id}"])
            return f"{video_id}.vtt"
        except Exception:
            return None


def ler_legendas(arquivo):
    """Lê legendas do arquivo .vtt"""
    if not os.path.exists(arquivo):
        return None

    with open(arquivo, 'r', encoding='utf-8') as f:
        linhas = f.readlines()

    texto_limpo = []
    for linha in linhas:
        if "-->" not in linha and linha.strip() and not linha.strip().isdigit():
            texto_limpo.append(linha.strip())

    return " ".join(texto_limpo)


def gerar_resumo(texto):
    """Usa a API Gemini para resumir as legendas"""
    try:
        modelo = genai.GenerativeModel("gemini-pro")
        resposta = modelo.generate_content(f"Resuma o seguinte texto detalhadamente em um formato bem estruturado, com parágrafos claros e separados (não precisa informar o número do parágrafo): \n\n{texto}")
        return resposta.text
    except Exception:
        return "Erro ao gerar resumo com IA."


@app.route('/resumir', methods=['POST'])
def resumir():
    """Recebe um link do usuário, extrai legendas e gera resumo"""
    try:
        data = request.get_json()
        video_url = data.get('link', '')

        if not video_url:
            return jsonify({'erro': 'Nenhuma URL fornecida'}), 400

        if 'youtube.com/watch?v=' in video_url:
            video_id = video_url.split('v=')[-1].split('&')[0]
        elif 'youtu.be/' in video_url:
            video_id = video_url.split('youtu.be/')[-1].split('?')[0]
        else:
            return jsonify({'erro': 'URL inválida'}), 400

        # Baixar legendas
        arquivo_legenda = baixar_legendas(video_id)
        if not arquivo_legenda:
            return jsonify({'erro': 'Este vídeo não possui legendas disponíveis'}), 500

        # Ler legendas
        transcricao = ler_legendas(arquivo_legenda)
        if not transcricao:
            return jsonify({'erro': 'Erro ao processar legendas'}), 500

        # Gerar resumo com IA
        resumo = gerar_resumo(transcricao)

        return jsonify({'resumo': resumo})

    except Exception as e:
        return jsonify({'erro': f'Erro interno: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
