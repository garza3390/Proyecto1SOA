from django.shortcuts import render
from django.http import HttpResponse
from openai import OpenAI
import json
import os

client = OpenAI()

def default(request,type,value):

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

def artificial(request,_type,value):

    value = _type + ": " + value
    print("\n")
    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", 
        "content": """Eres un recomendador de platos completos, y debes completar la combinación plato, bebida y postre
        recomendando lo que mejor combine para el usuario. El usuario te provee uno, o dos, de los elementos de la combinación
        y tú completas la combinación respondiendo con el siguiente formato: 
        {Plato Principal: "Tu respuesta", Bebida: "Tu respuesta", Postre: "Tu respuesta"}."""},
        {"role": "user", "content": value}
      ]
    )
    
    serviceRecommendation = completion.choices[0].message.content
    print(serviceRecommendation)

    return HttpResponse(serviceRecommendation, status=200)

def externalSystem(request,type,value):
    pass

def data(request):

    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/db/db.json')

    if not os.path.exists(file_path):
        return HttpResponse('El archivo no se encontró', status=404)
    
    with open(file_path) as f:
        data = f.read()
    return HttpResponse(data, content_type='application/json')
        

