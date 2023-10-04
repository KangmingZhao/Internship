from py2neo import Graph

graph = Graph("bolt://localhost:7687", auth=("neo4j", "030316zc"))

def query_neo4j(query, **params):
    result = graph.run(query, **params)
    return result

