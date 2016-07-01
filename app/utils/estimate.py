import os
from os.path import expanduser
import subprocess
import re
from datetime import datetime


def how_long():
    data_inicio = datetime.strptime('30/06/2016 12:18:00', "%d/%m/%Y %H:%M:%S")
    now = datetime.now()

    diff = now - data_inicio
    return divmod(diff.days * 86400 + diff.seconds, 60)


def percent_completo(sofar, total):

    return (float(sofar) * 100 / float(total))


def time_to_go(so_far, percent_complete):

    if percent_complete < 1:
        total = float(so_far) * 100 / float(1)
    else:
        total = float(so_far) * 100 / float(percent_complete)

    to_go = float((total - so_far)/60)
    return "%.2f horas" % to_go