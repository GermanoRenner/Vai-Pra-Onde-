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
def createCityWithRoad(request):
    de = json.loads(request.body)['de']
    para = json.loads(request.body)['para']
    roadKm = json.loads(request.body)['roadKm']

    print(de, para, roadKm)
    neoData.createNodeWithRel(de, para, 'Cidade', 'km', roadKm, False)
    return HttpResponse('Ola MUndo!')


@csrf_exempt 
def getCity(request):
    result = neoData.simpleSelect('Cidade', None)
    response = []
    for r in result:
        print('nome: ', r[0]['name'])
        response.append({'nome': r[0]['name']})
    return HttpResponse(response)