from neo4j import GraphDatabase

uri = "neo4j+s://9513c9ad.databases.neo4j.io"
username= "9513c9ad"
password= "rHZJ1U1LwZhbQdPItq2UfEoYzTScVv241N_85ZarT2E"
driver = GraphDatabase.driver(uri, auth=(username, password))

query= ''' MATCH (n), ()-[r]->()
           RETURN count(n) AS numNodos, count(r) AS numRelaciones'''

with driver.session() as session:
    result = session.run(query)
    print(result.data())

class Neo4jConnection:

    def __init__(self, uri, user, pwd):

        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None

        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))
        except Exception as e:
            print("Failed to create the driver:", e)

    def close(self):

        if self.__driver is not None:
            self.__driver.close()

    def query(self, query, parameters=None, db=None):

        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None

        try:
            session = self.__driver.session(database=db) if db is not None else self.__driver.session()
            response = list(session.run(query, parameters))
        except Exception as e:
            print("Query failed:", e)
        finally:
            if session is not None:
                session.close()
        return response
    

conn = Neo4jConnection(uri=uri, user=username, pwd=password)
query = """ MATCH (n:Product)
            RETURN n
            LIMIT 4 """

result = conn.query(query)
result

type(result[0])
type(result[0]["n"])
for record in result:
    print('Id:', record["n"].element_id)
    print('Etiquetas:', record["n"].labels)
    print('Propiedades:', dict(record["n"]))
    print('')

query = """ MATCH (n:Product)<-[r:SUPPLIES]-(s:Supplier)
            RETURN n,r,s
            LIMIT 1 """

result = conn.query(query)
result

query = """ MATCH path=(c:Customer)-[:PURCHASED]->()-[:ORDERS]->(:Product)<-[:SUPPLIES]-(:Supplier)
            WHERE c.companyName = 'Blauer See Delikatessen'
            RETURN path
            LIMIT 1 """

result = conn.query(query)
result