from py2neo import Graph, Node, Relationship, NodeMatcher
from py2neo.matching import *
from routesCalculate.database import config
import json

def getConnection():
    return Graph(password = config.PASSWORD)

def createSimpleNode(prop, labelName):
    db    = getConnection().begin()
    city = Node(labelName, nome=prop)
    db.create(city)
    db.commit()

def createRel(de, para, rel, distance):
    db    = getConnection().begin()
    node1 = Node('Cidade', nome=de)
    node2 = Node('Cidade', nome=para)
    KM  = Relationship(node1, rel, node2, distancia=distance)

    # db.create(node1)
    # db.create(node2)
    db.create(KM)
    db.commit()


def getDistance(de, para, rel):
    db = getConnection()
    node1 = getCity('Cidade', de)
    node2 = getCity('Cidade', para)
    print(de)
    print(para)
    distance = list(db.relationships.match((node1, node2), rel).limit(1))
    return distance


def getCity(labels, nameCity):
    db = getConnection()
    vertice = db.nodes.match(labels, nome = nameCity).first()
    return vertice
    

def buildQuery(template, de, para):
    template = template.replace('@cityFrom@', de)
    template = template.replace('@cityTo@', para)
    # if km is not None:
    #     template = template.replace('@km@', km)

    return template

def calcularShortestRoute (de, para):
    template = "MATCH (start:Cidade{nome:'@cityFrom@'}), (end:Cidade{nome:'@cityTo@'}) \
                CALL algo.shortestPath.stream(start, end, 'distancia') YIELD nodeId, cost \
                MATCH (other:Cidade) WHERE id(other) = nodeId \
                RETURN other.nome AS nome, cost "
    template = buildQuery(template, de, para)
    db = getConnection()
    result = db.run(template).data()
    return result

def createRoad (de, para, km):
    template = "MATCH(a:Cidade), (b:Cidade) WHERE a.nome= '@cityFrom@' and b.nome = '@cityTo@' CREATE(a)-[:km {distancia: {km}}]->(b)"
    template = buildQuery(template, de, para)
    db = getConnection()
    result = db.run(template, km=km).data()
    return result

def getAllCitysWithRoads():
    db = getConnection()
    templateRotas = "MATCH (n:Cidade) MATCH (n)-[r]->(m:Cidade) RETURN r.distancia as id, ID(n) as source, ID(m) as target, 'distancia' as label"
    templateCities = "MATCH (n:Cidade) RETURN n.nome as label, ID(n) as id"
    
    routes = db.run(templateRotas).data()
    cities = db.run(templateCities).data()
    result = {
        'nodes': cities,
        'edges': routes
    }
    return result