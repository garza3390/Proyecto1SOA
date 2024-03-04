from django.shortcuts import render
from django.http import HttpResponse
import json
import os

def default(request,type,value):

    value = value.lower()
    type = type.lower()

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
        return HttpResponse('No ofrecemos recomendaciones para esa solicitud', status=404)
    
    try:
        serviceRecommendation = str(data[type][value]["combination"])

        return HttpResponse(serviceRecommendation, content_type='application/json')
    
    except:
        return HttpResponse('Parece que estas combinando mal el tipo y el plato', status=404)
    
def defaultComplete(request,value1,value2):

    value1 = value1.lower()
    value2 = value2.lower()

    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/db/db.json')
    if not os.path.exists(file_path):
        return HttpResponse('El archivo no se encontró', status=404)
    
    with open(file_path) as jsonDb:
        data = json.load(jsonDb)

    type1 = None
    type2 = None

    mainDishes = data["maindishes"]
    drinks = data["drinks"]
    desserts = data["desserts"]

    mainDishesList = list(mainDishes.keys())
    drinksList = list(drinks.keys())
    dessertsList = list(desserts.keys())

    mainFoodKeys = mainDishesList + drinksList + dessertsList

    if value1 not in mainFoodKeys or value2 not in mainFoodKeys:
        return HttpResponse('No ofrecemos recomendaciones para esa solicitud', status=404)
    

    if value1 in mainDishesList:
        type1 = "maindishes"
    elif value1 in drinksList:
        type1 = "drinks"
    elif value1 in dessertsList:
        type1 = "desserts"

    if value2 in mainDishesList:
        type2 = "maindishes"
    elif value2 in drinksList:
        type2 = "drinks"
    elif value2 in dessertsList:
        type2 = "desserts"

    if type1 == None:
        return HttpResponse('No poseemos el primer platillo', status=404)
    if type2 == None:
        return HttpResponse('No poseemos el segundo platillo', status=404)


    try:
        servRec1 = str(data[type1][value1]["combination"])
        servRec2 = str(data[type2][value2]["combination"])
        serviceRecommendation = []
        canCombinate = False
        for r in servRec1:
            if r in servRec2:
                canCombinate = True
                serviceRecommendation = [value1,value2,r]
        if not canCombinate:
            return HttpResponse("No encontramos una recomendación de acuerdo a esas dos entradas",status=404)
        
        return HttpResponse(serviceRecommendation, content_type='application/json')
    
    except:
        return HttpResponse('No encontramos respuesta a esa solicitud', status=404)

def artificial(request,type,value):
    pass

def externalSystem(request,type,value):
    pass

def data(request):

    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/db/db.json')

    if not os.path.exists(file_path):
        return HttpResponse('El archivo no se encontró', status=404)
    
    with open(file_path) as f:
        data = f.read()
    return HttpResponse(data, content_type='application/json')
        

