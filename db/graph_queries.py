from neo4j import GraphDatabase
import config

driver = GraphDatabase.driver(
    config.NEO4J_URI,
    auth=(config.NEO4J_USER, config.NEO4J_PASSWORD)
)

def get_servers():
    """Get all unique servers from the database"""
    with driver.session() as session:
        result = session.run("""
        MATCH (s:Server)
        RETURN s.name AS server
        ORDER BY s.name
        """)
        return [r["server"] for r in result]    # returns list of server names

def get_impact(server_name):
    """Get all impacts for a specific server"""
    with driver.session() as session:
        result = session.run("""
        MATCH (s:Server {name: $server})-[:HAS_IMPACT]->(i:Impact)
        RETURN DISTINCT
               i.application AS application,
               i.process AS process,
               i.service AS service
        """, server=server_name)

        return result.data()    # returns list of dicts with keys: application, process, service

def get_all_impacts():
    """Get all impacts in the database"""
    with driver.session() as session:
        result = session.run("""
        MATCH (i:Impact)
        RETURN i.server AS server,
               i.application AS application,
               i.process AS process,
               i.service AS service,
               i.impact_year AS year
        ORDER BY i.impact_year DESC
        """)
        return result.data()


