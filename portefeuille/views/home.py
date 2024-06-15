from django.shortcuts import render
import datetime
import os.path
import time


def index(request):
    date_fichier = datetime.datetime.strptime(time.ctime(os.path.getmtime("data.json")), "%a %b %d %H:%M:%S %Y")
    return render(request, "portefeuille/home.html", locals())
