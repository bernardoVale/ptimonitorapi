from flask.ext.sqlalchemy import SQLAlchemy
import datetime
db = SQLAlchemy()


class Result(db.Model):

    __tablename__ = 'result'

    id = db.Column(db.Integer, primary_key=True)
    total_tabelas = db.Column(db.String, nullable=False)
    tamanho_atual = db.Column(db.String, nullable=False)
    ultima_tabela = db.Column(db.String, nullable=False)
    tempo_importacao = db.Column(db.Integer, nullable=False)
    data_coleta = db.Column(db.DateTime)

    def __init__(self, total_tabelas=None, tamanho_atual=None, ultima_tabela=None,
                 tempo_importacao=None, data_coleta=None):
        self.total_tabelas = total_tabelas
        self.tamanho_atual = tamanho_atual
        self.ultima_tabela = ultima_tabela
        self.tempo_importacao = tempo_importacao
        self.data_coleta = self.data_coleta