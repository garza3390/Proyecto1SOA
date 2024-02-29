from django.shortcuts import render
from django.http import HttpResponse
import json
import os

def recommendation(request,type,value):

    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/db/db.json')
    if not os.path.exists(file_path):
        return HttpResponse('El archivo no se encontró', status=404)
    if type not in ["maindishes","drinks","desserts"]:
        return HttpResponse('Ese tipo de entrada no existe', status=404)
    
    with open(file_path) as jsonDb:
        data = json.load(jsonDb)

    mainDishes = data["maindishes"]
    drinks = data["drinks"]
    desserts = data["desserts"]

    mainFoodKeys = list(mainDishes.keys()) + list(drinks.keys()) + list(desserts.keys())

    if value not in mainFoodKeys:
        return HttpResponse('No ofrecemos recomendaciones para ese platillo', status=404)
    
    try:
        serviceRecommendation = str(data[type][value]["combination"])

        return HttpResponse(serviceRecommendation, content_type='application/json')
    
    except:
        return HttpResponse('Parece que estas combinando mal el tipo y el plato', status=404)


def data(request):

    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/db/db.json')

    if not os.path.exists(file_path):
        return HttpResponse('El archivo no se encontró', status=404)
    
    with open(file_path) as f:
        data = f.read()
    return HttpResponse(data, content_type='application/json')
        

