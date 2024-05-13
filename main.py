from neo4j import GraphDatabase, basic_auth
from neo4j.exceptions import ServiceUnavailable, AuthError
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import random

# Constants for Neo4j database connection
NEO4J_URI = "bolt://localhost:7687"  # Update with your Neo4j URI
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "12345678"

# Class to interact with Neo4j
class Neo4jManager:

    def __init__(self, uri, username, password):
        self.uri = uri
        self.username = username
        self.password = password
        self.driver = self.connect_to_neo4j()

    # Function to create and return a Neo4j driver
    def connect_to_neo4j(self):
        try:
            driver = GraphDatabase.driver(
                self.uri, auth=(self.username, self.password))
            print("Connected to Neo4j database")
            return driver
        except ServiceUnavailable:
            print("Failed to connect to Neo4j. Is the database running?")
            return None
        except AuthError:
            print("Authentication error. Please check your credentials.")
            return None
        except Exception as e:
            print("An error occurred:", str(e))
            return None

    # Function to run a Cypher query and return results
    def run_query(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.run(query, parameters)
            return [record for record in result]

    # Fetch basic graph statistics including additional queries
    def fetch_graph_statistics(self):
        # Queries for various statistics
        total_nodes_query = "MATCH (n) RETURN count(n) AS total_nodes"
        total_relationships_query = "MATCH ()-[r]-() RETURN count(r) AS total_relationships"
        isolated_nodes_query = "MATCH (n) WHERE NOT (n)--() RETURN count(n) AS isolated_nodes"
        nodes_by_label_query = "MATCH (n) UNWIND labels(n) AS label RETURN label, count(n) AS count"
        relationships_by_type_query = "MATCH ()-[r]-() RETURN type(r) AS relationship_type, count(r) AS count"

        # Additional queries for statistics
        most_common_amenities_query = """
        MATCH (a:Amenity)<-[:HAS]-(l:Listing)
        RETURN a.name AS amenity, COUNT(l) AS num_listings
        ORDER BY num_listings DESC
        LIMIT 5
        """

        average_price_by_property_type_query = """
        MATCH (l:Listing)
        RETURN l.property_type AS property_type, AVG(l.price) AS avg_price
        ORDER BY avg_price DESC
        """

        top_hosts_by_num_listings_query = """
        MATCH (h:Host)-[:HOSTS]->(l:Listing)
        RETURN h.host_name AS host_name, COUNT(l) AS num_listings
        ORDER BY num_listings DESC
        LIMIT 10
        """

        geospatial_analysis_query = """
        MATCH (l:Listing)
        WHERE point.distance(point({latitude: l.latitude, longitude: l.longitude}), point({latitude: 30.2672, longitude: -97.7431})) < 5000
        RETURN l.name AS listing_name, l.latitude AS latitude, l.longitude AS longitude
        """

        host_similarity_analysis_query = """
        MATCH (h1:Host)-[:HOSTS]->(l:Listing)-[:HAS]->(a:Amenity)
        WITH h1, COLLECT(DISTINCT a.name) AS amenities
        MATCH (h2:Host)-[:HOSTS]->(l2:Listing)-[:HAS]->(a2:Amenity)
        WHERE h1 <> h2
        WITH h1, h2, COUNT(DISTINCT a2) AS common_amenities, SIZE(amenities) AS total_amenities
        RETURN h1.host_id AS host_id1, h2.host_id AS host_id2, common_amenities / toFloat(total_amenities) AS similarity
        ORDER BY similarity DESC
        LIMIT 10
        """

        # Get statistics
        total_nodes = self.run_query(total_nodes_query)[0]["total_nodes"]
        total_relationships = self.run_query(total_relationships_query)[0]["total_relationships"]
        isolated_nodes = self.run_query(isolated_nodes_query)[0]["isolated_nodes"]
        nodes_by_label = self.run_query(nodes_by_label_query)
        relationships_by_type = self.run_query(relationships_by_type_query)

        # Additional statistics
        most_common_amenities = self.run_query(most_common_amenities_query)
        average_price_by_property_type = self.run_query(average_price_by_property_type_query)
        top_hosts_by_num_listings = self.run_query(top_hosts_by_num_listings_query)
        geospatial_analysis = self.run_query(geospatial_analysis_query)
        host_similarity_analysis = self.run_query(host_similarity_analysis_query)

        # Return collected statistics
        return {
            "total_nodes": total_nodes,
            "total_relationships": total_relationships,
            "isolated_nodes": isolated_nodes,
            "nodes_by_label": nodes_by_label,
            "relationships_by_type": relationships_by_type,
            "most_common_amenities": most_common_amenities,
            "average_price_by_property_type": average_price_by_property_type,
            "top_hosts_by_num_listings": top_hosts_by_num_listings,
            "geospatial_analysis": geospatial_analysis,
            "host_similarity_analysis": host_similarity_analysis,
        }

    def close(self):
        self.driver.close()

# Initialize the Neo4j manager with connection details
neo4j_manager = Neo4jManager(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD)

if neo4j_manager.driver:
    # Fetch basic graph statistics including additional statistics
    graph_statistics = neo4j_manager.fetch_graph_statistics()

    # Print basic graph statistics
    print("Graph Statistics:")
    print("Total nodes:", graph_statistics["total_nodes"])
    print("Total relationships:", graph_statistics["total_relationships"])
    print("Isolated nodes:", graph_statistics["isolated_nodes"])

    print("Node Distribution by Label:")
    for record in graph_statistics["nodes_by_label"]:
        print(f" - {record['label']}: {record['count']} nodes")

    print("Relationships by Type:")
    for record in graph_statistics["relationships_by_type"]:
        print(f" - {record['relationship_type']}: {record['count']} relationships")

    # Print additional statistics
    print("\nAdditional Statistics:")
    print("Most Common Amenities:")
    for record in graph_statistics["most_common_amenities"]:
        print(f" - Amenity: {record['amenity']}, Number of Listings: {record['num_listings']}")

    print("\nAverage Listing Price by Property Type:")
    for record in graph_statistics["average_price_by_property_type"]:
        print(f" - Property Type: {record['property_type']}, Average Price: {record['avg_price']}")

    print("\nTop Hosts by Number of Listings:")
    for record in graph_statistics["top_hosts_by_num_listings"]:
        print(f" - Host: {record['host_name']}, Number of Listings: {record['num_listings']}")

    print("\nGeospatial Analysis for Location-Based Recommendations:")
    for record in graph_statistics["geospatial_analysis"]:
        print(f" - Listing Name: {record['listing_name']}, Latitude: {record['latitude']}, Longitude: {record['longitude']}")

    print("\nHost Similarity Analysis:")
    for record in graph_statistics["host_similarity_analysis"]:
        print(f" - Host ID 1: {record['host_id1']}, Host ID 2: {record['host_id2']}, Similarity: {record['similarity']}")

    neo4j_manager.close()
