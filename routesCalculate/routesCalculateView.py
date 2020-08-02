from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
import json
from routesCalculate.database import neoData

@csrf_exempt 
def createCity(request):
    request1 = json.loads(request.body)
    nome = request1['nome']
    neoData.createSimpleNode(nome, 'Cidade')
    return HttpResponse('Ola MUndo!')

@csrf_exempt 
def createRoad(request):
    de = json.loads(request.body)['de']
    para = json.loads(request.body)['para']
    roadKm = json.loads(request.body)['roadKm']

    print(de, para, roadKm)
    neoData.createRoad(de, para, roadKm)
    return HttpResponse('Ola MUndo!')


@csrf_exempt 
def getCity(request):
    request1 = json.loads(request.body)
    nome = request1['nome']
    result = neoData.getCity('Cidade', nome)
    resposta = json.dumps(result)

    return HttpResponse(resposta, content_type='application/json')

    

@csrf_exempt 
def getDistance(request):
    de = json.loads(request.body)['de']
    para = json.loads(request.body)['para']
    result = neoData.getDistance(de, para, 'km')
    print('RESULTO', result)
    resposta = json.dumps(result)
    return HttpResponse(resposta, content_type='application/json')


@csrf_exempt 
def calcularShortestRoute(request):
    de = json.loads(request.body)['de']
    para = json.loads(request.body)['para']
    result = neoData.calcularShortestRoute(de, para)
    
    resposta = json.dumps(result)
    return HttpResponse(resposta, content_type='application/json')

@csrf_exempt 
def getAllCitysWithRoads(request):
    result = neoData.getAllCitysWithRoads()
    resposta = json.dumps(result)
    return HttpResponse(resposta, content_type='application/json')