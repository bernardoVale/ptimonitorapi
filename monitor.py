#!/usr/bin/python
# coding=utf-8
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

def estimate():
    total_tables = 2200
    total_size = 85

    so_far = how_long()

    print "Estimativa"
    print "-" * 60
    print "Tempo de Importação(Minutos):%s" % so_far[0]
    print "Total de tabelas no PostgreSQL:%s" % total_tables
    print "Tamanho no banco no PostgreSQL(GB):%s" % total_size

    profile = define_system_profile('OracleLinux')

    size_query = "%s SELECT trunc((sum(bytes)/1024/1024/1024),2) AS SIZE_GB FROM user_segments;" % sqlplus_header()

    table_query = "%s SELECT count(*) FROM user_tables;" % sqlplus_header()

    stdout = run_sqlplus(size_query, profile)
    tables_so_far = run_sqlplus(table_query, profile).strip()

    size = stdout.strip().replace(",", ".")

    percent_complete = float(size) * 100 / float(total_size)
    table_percent_complete = int(tables_so_far) * 100 / int(total_tables)

    print u"Estimativa por Size(Porcentagem):%.2f" % percent_complete
    print u"Estimativa por Tabelas Completas(Porcentagem):%s" % table_percent_complete
    print "-" * 60

    print "Tempo Final Estimado"
    print "-" * 60

    if percent_complete < 1:
        tempo_estimado_size = int(so_far[0]) * 100 / int(1)
        print u"Estimativa de tempo por Size(Horas):%s" % int(tempo_estimado_size/60)
    else:
        tempo_estimado_size = int(so_far[0]) * 100 / int(percent_complete)
        print u"Estimativa de tempo por Size(Horas):%s" % int(tempo_estimado_size/60)

    if table_percent_complete < 1:
        tempo_estimado = int(so_far[0]) * 100 / int(1)
        print u"Estimativa de tempo por Tabelas Completas(Horas):%s" % int(tempo_estimado/60)
    else:
        tempo_estimado = int(so_far[0]) * 100 / int(table_percent_complete)
        print u"Estimativa de tempo por Tabelas Completas(Horas):%s" % int(tempo_estimado/60)

    print "-" * 60



def how_long():
    data_inicio = datetime.strptime('30/06/2016 12:18:00', "%d/%m/%Y %H:%M:%S")
    now = datetime.now()

    diff = now - data_inicio
    return divmod(diff.days * 86400 + diff.seconds, 60)


def print_query(query, msg):
    profile = define_system_profile('OracleLinux')

    query = "%s %s" % (sqlplus_header(), query)

    stdout = run_sqlplus(query, profile)

    print "%s%s" % (msg, stdout.strip())


table_query = "SELECT count(*) FROM user_tables;"
size_query = "SELECT trunc((sum(bytes)/1024/1024/1024),2) AS SIZE_GB FROM user_segments;"
last_table = "select * from (select table_name from user_tables where table_name not like 'TOP_%' order by 1 desc) where rownum <=1;"

print "Monitor"
print "-"*60
print_query(table_query, "Total de Tabelas:")
print_query(size_query, "Tamanho Atual(GB):")
print_query(last_table, u"Última tabela importada:")
print "-"*60
estimate()