# coding=utf-8
from flask import Blueprint, render_template, jsonify, request
from flask_api import status
from app.models import db, Result
from app.utils import estimate
main = Blueprint('main', __name__)

TOTAL_TABELAS = 2200
TOTAL_SIZE = 85

@main.route('/')
def hello_world():

    resultado = Result.query.all()[-1]

    so_far = estimate.how_long()

    estimate_tables = estimate.percent_completo(resultado.total_tabelas, TOTAL_TABELAS)
    estimate_size = estimate.percent_completo(resultado.tamanho_atual, TOTAL_SIZE)


    estimate_time_tables = estimate.time_to_go(so_far, estimate_tables)
    estimate_time_size = estimate.time_to_go(so_far, estimate_size)

    return render_template("monitor.html", title="PTI Monitor", result=resultado,
                           estimate_tables= "%.2f" % estimate_tables, estimate_size="%.2f" % estimate_size,
                           time_tables=estimate_time_tables, time_size=estimate_time_size)


@main.route("/pushresult/<string:tamanho_atual>/<string:tempo_importacao>/<string:total_tabelas>/"
            "<string:ultima_tabela>", methods=["POST"])
def post_result(tamanho_atual, tempo_importacao, total_tabelas, ultima_tabela):

    r = Result(tamanho_atual=tamanho_atual, tempo_importacao=tempo_importacao,
               total_tabelas=total_tabelas, ultima_tabela=ultima_tabela)
    db.session.add(r)
    db.session.commit()

    return jsonify(
        {}
    ),status.HTTP_200_OK

@main.route("/sendresult", methods=["POST"])
def send_result():
    result = request.get_json()

    try:
        r = Result()
        r.tamanho_atual = result["tamanho_atual"]
        r.tempo_importacao = result["tempo_importacao"]
        r.total_tabelas = result["total_tabelas"]
        r.ultima_tabela = result["ultima_tabela"]
        db.session.add(r)
        db.session.commit()
    except:
        return jsonify(
            {'detail': u"Argumentos inválidos"}
        ), status.HTTP_400_BAD_REQUEST

    return jsonify({}), status.HTTP_201_CREATED