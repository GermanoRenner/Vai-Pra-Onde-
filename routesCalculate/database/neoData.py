from neo4jrestclient.client import GraphDatabase
from neo4jrestclient import client
from routesCalculate.database import config

def getConnection():
    return GraphDatabase(config.HOST, config.USERNAME, config.PASSWORD)

def createSimpleNode(prop, labelName):
    db    = getConnection()
    label = db.labels.create(labelName)
    node  = db.nodes.create(name = prop)
    label.add(node)

def createNodeWithRel(prop1, prop2, labelName, rel, cost, directional):

    db    = getConnection()
    label = db.labels.create(labelName)
    node1  = db.nodes.create(name = prop1)
    node2  = db.nodes.create(name = prop2)
    label.add(node1, node2)

    node1.relationships.create(rel, node2, cost=cost) if directional is True else db.relationships.create(node1, rel, node2, cost=cost)
    


def simpleSelect(labels, rel):
    db    = getConnection()
    template = 'MATCH(@label:label@)' + 'OPTIONAL MATCH(label)-[@r:rel@]-() RETURN label, r'
                        
    query = buildQuery(template, labels, rel)

    results = db.query(query, returns=(client.Node, str, client.Node))
    return results
    

def buildQuery(template, label, rel):
    template = template.replace('@label:label@', 'label:'+label) if label is not None else template.replace('@label:label@', 'label')
    template = template.replace('@r:rel@', 'r:'+rel) if rel is not None else template.replace('@r:rel@', 'r')

    return template