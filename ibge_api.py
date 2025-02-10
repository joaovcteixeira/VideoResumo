import requests

url_estados = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados'
url_cidades = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados/{}/municipios'

def obter_estados():
    resposta = requests.get(url_estados)
    if resposta.status_code == 200:
        estados = resposta.json()
        return {estado['sigla']: estado['nome'] for estado in estados}
    return {}

def obter_cidades(uf):
    resposta = requests.get(url_cidades.format(uf))
    if resposta.status_code == 200:
        cidades = resposta.json()
        return [cidade['nome'] for cidade in cidades]
    return []