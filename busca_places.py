import requests

url = 'https://overpass-api.de/api/interpreter'

def buscar_restaurantes(estado,cidade):
    query = f"""
    [out:json];
    area['ISO3166-2'='BR-{estado}']->.estado;
    area['name'='{cidade}']['admin_level'='8'](area.estado)->.cidade;
    (
        node['amenity'='restaurant'](area.cidade);
        way['amenity'='restaurant'](area.cidade);
        relation['amenity'='restaurant'](area.cidade);
    );
    out center;
    """
    try:
        resposta = requests.get(url, params={'data':query})
        resposta.raise_for_status()
        dados = resposta.json()

        restaurantes = []

        for elemento in dados.get('elements',[]):
            nome = elemento.get('elements', [])
            nome = elemento.get('tags',{}).get('name','Nome desconhecido')
            restaurantes.append(nome)

        return restaurantes if restaurantes else ['Nenhum restaurante encontrado']

    except requests.exceptions.RequestException as e:
        print(f'Erro ao buscar dados: {e}')
        return ['Erro ao buscar dados.']