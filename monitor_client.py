import requests
from datetime import datetime
endpoint = "http://127.0.0.1:5000/sendresult"

coleta = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
result = {
  "tamanho_atual": "50",
  "tempo_importacao": "120",
  "total_tabelas": "1940",
  "ultima_tabela": "ZYS010",
  "data_coleta": coleta,
}
r = requests.post(endpoint, json = result)

if r.status_code != 201:
    print "Erro ao enviar coleta de dados"
    exit(1)