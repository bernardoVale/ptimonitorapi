import requests

endpoint = "http://10.200.0.126:86/sendresult"

result = {
  "tamanho_atual": "45",
  "tempo_importacao": "780",
  "total_tabelas": "1340",
  "ultima_tabela": "ZYS010"
}
r = requests.post(endpoint, json = result)

if r.status_code != 201:
    print "Erro ao enviar coleta de dados"
    exit(1)