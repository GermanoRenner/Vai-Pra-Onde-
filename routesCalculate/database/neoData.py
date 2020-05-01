from py2neo import Graph, Node, Relationship, NodeMatcher
from routesCalculate.database import config

def getConnection():
    return Graph(password = config.PASSWORD)

def createSimpleNode(prop, labelName):
    db    = getConnection().begin()
    city = Node(labelName, nome=prop)
    db.create(city)
    db.commit()

def createRel(de, para, rel, distance):
    db    = getConnection()
    node1 = getCity('Cidade', de)
    node2 = getCity('Cidade', para)
    KM  = Relationship(node1, rel, node2, distancia=distance)
    KM2 = Relationship(node2, rel, node1, distancia=distance)
    db.merge(KM)
    db.merge(KM2)


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
