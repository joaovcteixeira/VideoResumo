import google.generativeai as genai

genai.configure(api_key='AIzaSyCDRcqRw2YmRbixhM_v-I8B3AIGniqf24Y')

def disciplinas(curso):
    curso = str(curso)
    modelo = genai.GenerativeModel('gemini-pro')
    prompt = ('Ofereça detalhadamente, subdivido e com base em todos os dados possíveis,'
           'as disciplinas (e seus subtemas) necessários para seguinte curso:\n'+curso)
    resposta = modelo.generate_content(prompt)
    return resposta.text

estudante = str(input('Digite o nome do curso que você quer estudar: '))
assuntos = disciplinas(estudante)
print(f'\n\033[97;42m DISCIPLINAS -> {estudante} \033[m\n\n',assuntos)
