import requests
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from openai import OpenAI
import json
import os

client = OpenAI()

def formaResponseList(type,list):

    if type == "maindishes":
            list[0] = "Bebida: " + list[0]
            list[1] = "Postre: " + list[1]
            list[2] = "Plato Principal: " + list[2]
    elif type == "drinks":
            list[0] = "Plato Principal: " + list[0]
            list[1] = "Postre: " + list[1]
            list[2] = "Bebida: " + list[2]
    elif type == "desserts":
            list[0] = "Plato Principal: " + list[0]
            list[1] = "Bebida: " + list[1]
            list[2] = "Postre: " + list[2]

    return list

def formaResponseList2(type1,type2,list):

    allValues = ["Plato Principal: ", "Bebida: ", "Postre: "]

    if type1 == "maindishes":
        type1 = "Plato Principal: "
    elif type1 == "drinks":
        type1 = "Bebida: "
    elif type1 == "desserts":
        type1 = "Postre: "

    if type2 == "maindishes":
        type2 = "Plato Principal: "
    elif type2 == "drinks":
        type2 = "Bebida: "
    elif type2 == "desserts":
        type2 = "Postre: "

    allValues.remove(type1)
    allValues.remove(type2)

    list = [type1+list[0],type2+list[1],allValues[0]+list[2]]

    return list

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
        serviceRecommendation = data[type][value]["combination"] + [value.capitalize()]
        serviceRecommendation = str(formaResponseList(type,serviceRecommendation))
        serviceRecommendation = serviceRecommendation.replace("[","{").replace("]","}")
        

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
        servRec1 = data[type1][value1]["combination"]
        servRec2 = data[type2][value2]["combination"]
        serviceRecommendation = []
        canCombinate = False
        for r in servRec1:
            if r in servRec2 and r.lower() != value1 and r.lower() != value2:
                canCombinate = True
                serviceRecommendation = [value1.capitalize(),value2.capitalize(),r]
                serviceRecommendation = str(formaResponseList2(type1,type2,serviceRecommendation))
                serviceRecommendation = serviceRecommendation.replace("[","{").replace("]","}")
                
                break
        if not canCombinate:
            return HttpResponse("No encontramos una recomendación de acuerdo a esas dos entradas",status=404)
        
        return HttpResponse(serviceRecommendation, content_type='application/json')
    
    except:
        return HttpResponse('No encontramos respuesta a esa solicitud', status=404)

def artificial(request,_type,value):

    if(_type == "maindishes"):
        _type = "Plato Principal"
    elif(_type == "drinks"):
        _type = "Bebida"
    elif(_type == "desserts"):
        _type = "Postre"
    else:
        _type = "Combinar"

    value = _type + ": " + value
    print("\n")
    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
		{"role": "system", 
        "content": """Eres un recomendador de platos completos, y debes completar la combinación Plato Principal, Bebida y Postre
        recomendando lo que mejor combine para el usuario. El usuario te provee uno de los elementos de la combinación
        y tú completas la combinación respondiendo con el siguiente formato: 
        {Plato Principal: "Tu respuesta", Bebida: "Tu respuesta", Postre: "Tu respuesta"}."""},
        {"role": "user", "content": value}
      ]
    )
    
    serviceRecommendation = completion.choices[0].message.content
    print(serviceRecommendation)

    return HttpResponse(serviceRecommendation, status=200)

def artificialComplete(request,value1,value2):

    value1 = "Primer valor: " + value1
    value2 = "Segundo valor: " + value2
    message = value1 + "\n" + value2

    print("\n")

    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
		{"role": "system", 
        "content": """Eres un recomendador de platos completos, y debes completar la combinación Plato Principal, Bebida y Postre
        recomendando lo que mejor combine para el usuario. El usuario te provee o dos de los elementos de la combinación
        y tú completas la combinación respondiendo con el siguiente formato: 
        {Plato Principal: "Tu respuesta", Bebida: "Tu respuesta", Postre: "Tu respuesta"}."""},
        {"role": "user", "content": message}
      ]
    )
    
    serviceRecommendation = completion.choices[0].message.content
    print(serviceRecommendation)

    return HttpResponse(serviceRecommendation, status=200)

def externalSystem(request,type,value):
    # Inicializamos el JSON con valores predeterminados
    response_data = {
        "meal": {
            "dessert": "",
            "drink": "",
            "main_dish": ""
        },
        "recommendation_of": [],
        "src": "localdb"
    }

    # Verificamos el valor de 'type' y actualizamos el JSON
    if type == "maindishes":
        response_data["meal"]["main_dish"] = value
        response_data["recommendation_of"] = ["drink", "dessert"]
    elif type == "drinks":
        response_data["meal"]["drink"] = value
        response_data["recommendation_of"] = ["main_dish", "dessert"]
    elif type == "desserts":
        response_data["meal"]["dessert"] = value
        response_data["recommendation_of"] = ["main_dish", "drink"]
    else:
        # Si 'type' no es uno de los valores esperados
        return JsonResponse({"error": "Tipo no válido"}, status=400)

    return getExternalResponse(response_data)

def externalSystemComplete(request,type1,value1,type2,value2):
    # Inicializamos el JSON con valores predeterminados
    response_data = {
        "meal": {
            "dessert": "",
            "drink": "",
            "main_dish": ""
        },
        "recommendation_of": [],
        "src": "localdb"
    }

    # Verificamos los valores de type1, value1, type2, y value2 y actualizamos el JSON
    if type1 == "drinks":
        response_data["meal"]["drink"] = value1
    elif type1 == "maindishes":
        response_data["meal"]["main_dish"] = value1
    elif type1 == "desserts":
        response_data["meal"]["dessert"] = value1
    else:
        # Si type1 no es uno de los valores esperados
        return JsonResponse({"error": "Tipo no válido"}, status=400)

    if type2 == "drinks":
        response_data["meal"]["drink"] = value2
    elif type2 == "maindishes":
        response_data["meal"]["main_dish"] = value2
    elif type2 == "desserts":
        response_data["meal"]["dessert"] = value2
    else:
        # Si type2 no es uno de los valores esperados
        return JsonResponse({"error": "Tipo no válido"}, status=400)

    if type1 != "drinks" and type2 != "drinks":
        response_data["recommendation_of"] = ["dessert"]
    elif type1 != "maindishes" and type2 != "maindishes":
        response_data["recommendation_of"] = ["main_dish"]
    elif type1 != "desserts" and type2 != "desserts":
        response_data["recommendation_of"] = ["dessert"]

    return getExternalResponse(response_data)

def getExternalResponse(response_data):
    # URL de destino
    post_url = "http://34.208.253.148/gen-recommendation/"

    try:
        # Realizamos la solicitud POST con el JSON construido
        response = requests.post(post_url, json=response_data)

        # Verificamos el código de estado de la respuesta
        if response.status_code == 200:
            # La solicitud fue exitosa, procesamos la respuesta JSON
            recommendation_data = response.json()

           # Transformamos la respuesta al formato deseado
            formatted_response = {
                "Plato Principal": recommendation_data.get("main_dish", "").capitalize(),
                "Bebida": recommendation_data.get("drink", "").capitalize(),
                "Postre": recommendation_data.get("dessert", "").capitalize()
            }

            # Devolvemos la respuesta procesada
            return JsonResponse(formatted_response)
        else:
            # La solicitud no fue exitosa, puedes manejarlo según tus necesidades
            return JsonResponse({"error": f"Solicitud fallida con código de estado {response.status_code}"}, status=500)
    except requests.exceptions.RequestException as e:
        # Manejamos las excepciones de la solicitud
        return JsonResponse({"error": f"Error en la solicitud: {str(e)}"}, status=500)

def data(request):

    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/db/db.json')

    if not os.path.exists(file_path):
        return HttpResponse('El archivo no se encontró', status=404)
    
    with open(file_path) as f:
        data = f.read()
    return HttpResponse(data, content_type='application/json')
        

