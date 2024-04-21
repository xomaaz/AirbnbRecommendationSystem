from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable, AuthError

uri = "bolt://localhost:7687"  
username = "neo4j"
password = "Prettyflacko1"

try:
    # Connect to Neo4j
    driver = GraphDatabase.driver(uri, auth=(username, password))
    print("Connected to database")  # Confirm successful connection

    # Function to run a Cypher query and return results
    def run_query(query):
        with driver.session() as session:
            result = session.run(query)
            return [record for record in result]

    # Example query: Total number of nodes
    query = "MATCH (n) RETURN count(n) AS total_nodes"
    total_nodes = run_query(query)[0]['total_nodes']

    print("Total nodes in the graph:", total_nodes)

except ServiceUnavailable:
    print("Failed to connect to Neo4j. Is the database running?")
except AuthError:
    print("Authentication error. Please check your username and password.")
except Exception as e:
    print("An error occurred:", str(e))
finally:
    # Ensure the connection is closed
    if 'driver' in locals() and driver:
        driver.close()
