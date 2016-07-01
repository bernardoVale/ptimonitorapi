import requests

endpoint = "http://127.0.0.1:5000/sendresult"

result = {
  "tamanho_atual": "45",
  "tempo_importacao": "730",
  "total_tabelas": "1340",
  "ultima_tabela": "SX1010"
}
r = requests.post(endpoint, json = result)

if r.status_code != 201:
    print "Erro ao enviar coleta de dados"
    exit(1)