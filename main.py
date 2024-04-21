from neo4j import GraphDatabase, basic_auth
from neo4j.exceptions import ServiceUnavailable, AuthError

# Function to create and return a Neo4j driver
def connect_to_neo4j(uri, username, password):
    try:
        driver = GraphDatabase.driver(uri, auth=(username, password))
        print("Connected to database")  # Confirm successful connection
        return driver
    except ServiceUnavailable:
        print("Failed to connect to Neo4j. Is the database running?")
        return None
    except AuthError:
        print("Authentication error. Please check your username and password.")
        return None
    except Exception as e:
        print("An error occurred:", str(e))
        return None

# Function to run a Cypher query and return results
def run_query(driver, query):
    with driver.session() as session:
        result = session.run(query)
        return [record for record in result]

# Function to fetch basic graph statistics
def fetch_graph_statistics(driver):
    # Get total number of nodes
    total_nodes_query = "MATCH (n) RETURN count(n) AS total_nodes"
    total_nodes = run_query(driver, total_nodes_query)[0]['total_nodes']

    # Get total number of relationships/edges
    total_relationships_query = "MATCH ()-[r]-() RETURN count(r) AS total_relationships"
    total_relationships = run_query(driver, total_relationships_query)[0]['total_relationships']

    # Get number of isolated nodes
    isolated_nodes_query = "MATCH (n) WHERE NOT (n)--() RETURN count(n) AS isolated_nodes"
    isolated_nodes = run_query(driver, isolated_nodes_query)[0]['isolated_nodes']

    # Get number of nodes by type
    nodes_by_type_query = "MATCH (n) RETURN labels(n)[0] AS node_type, count(n) AS count"
    nodes_by_type = run_query(driver, nodes_by_type_query)

    # Get total hosts
    total_hosts_query = "MATCH (h:Host) RETURN count(h) AS total_hosts"
    total_hosts = run_query(driver, total_hosts_query)[0]['total_hosts']

    # Get total listings
    total_listings_query = "MATCH (l:Listing) RETURN count(l) AS total_listings"
    total_listings = run_query(driver, total_listings_query)[0]['total_listings']

    # Get superhost count
    superhosts_count_query = "MATCH (h:Host) WHERE h.host_is_superhost = true RETURN count(h) AS superhosts_count"
    superhosts_count = run_query(driver, superhosts_count_query)[0]['superhosts_count']

    # Get max listings per host
    max_listings_per_host_query = "MATCH (h:Host)-[:HOSTS]->(l:Listing) RETURN count(l) AS count ORDER BY count DESC LIMIT 1"
    max_listings_per_host = run_query(driver, max_listings_per_host_query)[0]['count']

    # Return collected statistics
    return {
        "total_nodes": total_nodes,
        "total_relationships": total_relationships,
        "isolated_nodes": isolated_nodes,
        "nodes_by_type": nodes_by_type,
        "total_hosts": total_hosts,
        "total_listings": total_listings,
        "superhosts_count": superhosts_count,
        "max_listings_per_host": max_listings_per_host,
    }

# Main script
uri = "bolt://localhost:7687"  # Update with your Neo4j URI
username = "neo4j"
password = "Prettyflacko1"

driver = connect_to_neo4j(uri, username, password)

if driver:  # Only proceed if the connection was successful
    graph_statistics = fetch_graph_statistics(driver)

    print("Total nodes in the graph:", graph_statistics["total_nodes"])
    print("Total relationships in the graph:", graph_statistics["total_relationships"])
    print("Total isolated nodes in the graph:", graph_statistics["isolated_nodes"])

    print("Nodes by type:")
    for record in graph_statistics["nodes_by_type"]:
        print(f" - {record['node_type']}: {record['count']}")

    print("Total hosts in the graph:", graph_statistics["total_hosts"])
    print("Total listings in the graph:", graph_statistics["total_listings"])
    print("Total superhosts in the graph:", graph_statistics["superhosts_count"])

    print("Max listings by a single host:", graph_statistics["max_listings_per_host"])

    driver.close()  # Close the database connection
