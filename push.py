#!/usr/bin/python
# coding=utf-8
import requests
import os
from os.path import expanduser
import subprocess
import re
from datetime import datetime

def find_oracle_home_hard():

    f = open('/etc/passwd', 'r')
    try:
        passwd = f.read()
        for line in passwd.split('\n'):
            if re.match(r"^oracle:", line, flags=re.MULTILINE):
                return line.split(":")[5]
    finally:
        f.close()

    return u"Usuário Oracle não encontrado no /etc/passwd"

def define_system_profile(system):
    user_home = find_oracle_home_hard()
    if system == 'SLES' or system == 'Solaris' or system == 'AIX':
        return os.path.join(user_home, ".profile")
    else:
        return os.path.join(user_home, ".bash_profile")


def sqlplus_header():
    return "SET NEWPAGE 0 \n \
SET SPACE 0 \n \
SET LINESIZE 80 \n \
SET PAGESIZE 0 \n \
SET ECHO OFF \n \
SET FEEDBACK OFF \n \
SET VERIFY OFF \n \
SET HEADING OFF \n \
SET MARKUP HTML OFF SPOOL OFF \n \
SET COLSEP ',' \n \
        "


def run_sqlplus(query, profile):
    username = 'totvs'
    password = 'totvs'
    sid = 'totvsdev'
    #Standard sqlplus command
    sqlplus = "sqlplus -S %s/%s" % (username, password)

    #Setting the sid
    set_sid = "export ORACLE_SID=%s" % sid

    #Parsing the command
    cmd = "source %s;%s && %s" % (profile, set_sid, sqlplus)

    # Execute as a bash command to make `source` command works
    command = ['bash', '-c', cmd]

    session = subprocess.Popen(command, stdin=subprocess.PIPE,
                               env=dict(os.environ, ORACLE_SID=sid),
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    session.stdin.write(query)
    stdout, stderr = session.communicate()
    if stderr != '' or session.returncode != 0 or 'ORA-' in stdout:
        print "Falha ao executar consulta"
        print stderr
        exit(1)
    else:
        return stdout


def get_query_output(query):
    profile = define_system_profile('OracleLinux')

    query = "%s %s" % (sqlplus_header(), query)

    stdout = run_sqlplus(query, profile)

    return "%s" % stdout.strip().replace(',','.')

def how_long():
    data_inicio = datetime.strptime('30/06/2016 12:18:00', "%d/%m/%Y %H:%M:%S")
    now = datetime.now()

    diff = now - data_inicio
    return divmod(diff.days * 86400 + diff.seconds, 60)

table_query = "SELECT count(*) FROM user_tables;"
size_query = "SELECT trunc((sum(bytes)/1024/1024/1024),2) AS SIZE_GB FROM user_segments;"
last_table = "select * from (select table_name from user_tables where table_name not like 'TOP_%' order by 1 desc) where rownum <=1;"

total_tabelas = get_query_output(table_query)
tamanho_atual = get_query_output(size_query)
ultima_tabela = get_query_output(last_table)
tempo_importacao = how_long()[0]

result = {
  "tamanho_atual": tamanho_atual,
  "tempo_importacao": tempo_importacao,
  "total_tabelas": total_tabelas,
  "ultima_tabela": ultima_tabela
}
endpoint = "http://ptimonitor.lb2.com.br/sendresult"
r = requests.post(endpoint, json = result)
if r.status_code != 201:
    print "Erro ao enviar coleta de dados"
    exit(1)