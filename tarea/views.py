from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Esto sirve para convertir strings a jsons y jsons a strings
from json import loads, dumps
import sqlite3
import requests

# Ruta para index
def index(request):
    return render(request, 'index.html')

# Post para retrivear datos
@csrf_exempt
def datos(request):
    body = request.body.decode('UTF-8')
    eljson = loads(body)
    # Datos del estudiante por ID
    id_estudiante1 = eljson['id1']
    id_estudiante2 = eljson['id2']

    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()

    # Sacar los números de lista y grupos
    estudiante1 = list(cur.execute
                       ("SELECT numero_lista FROM Estudiante WHERE id = ?", [(str(id_estudiante1))]))
    grupo1 = list(cur.execute
                       ("SELECT grupo FROM Estudiante WHERE id = ?", [(str(id_estudiante1))]))
    
    estudiante2 = list(cur.execute
                       ("SELECT numero_lista FROM Estudiante WHERE id = ?", [(str(id_estudiante2))]))

    grupo2 = list(cur.execute
                       ("SELECT grupo FROM Estudiante WHERE id = ?", [(str(id_estudiante2))]))

    # Minutos jugados de estudiante 1
    minutos_jugados1 = list(cur.execute
                           ("SELECT minutos_jugados FROM Partida WHERE estudiante = ?", [(str(id_estudiante1))]))
    # Minutos jugados de estudiante 2
    minutos_jugados2 = list(cur.execute
                           ("SELECT minutos_jugados FROM Partida WHERE estudiante = ?", [(str(id_estudiante2))]))
    
    # Niveles de estudiante 1
    niveles1 = list(cur.execute
                 ("SELECT nivel FROM Partida WHERE estudiante = ?", [(str(id_estudiante1))]))
    # Niveles de estudiante 2
    niveles2 = list(cur.execute
                 ("SELECT nivel FROM Partida WHERE estudiante = ?", [(str(id_estudiante2))]))
    
    # Puntajes de estudiante 1
    puntajes1 = list(cur.execute
                   ("SELECT puntaje FROM Partida WHERE estudiante = ?", [(str(id_estudiante1))]))
    # Puntajes de estudiante 2
    puntajes2 = list(cur.execute
                   ("SELECT puntaje FROM Partida WHERE estudiante = ?", [(str(id_estudiante2))]))
    
    return JsonResponse({"estudiante1" : estudiante1, "grupo1" : grupo1,
                         "minutos_jugados1" : minutos_jugados1, "niveles1" : niveles1, "puntajes1" : puntajes1,
                         "estudiante2" : estudiante2, "grupo2" : grupo2,
                         "minutos_jugados2" : minutos_jugados2, "niveles2" : niveles2,
                         "puntajes2" : puntajes2})

# Para graficar
@csrf_exempt
def bubblegraph(request):
    url = 'http://127.0.0.1:8000/datos'
    id_estudiantes = {"id1" : 1, "id2" : 2}
    resultado = requests.post(url, json = id_estudiantes)
    data_json = resultado.json()

    return render(request, 'bubblegraph.html', {'data_json' : data_json})