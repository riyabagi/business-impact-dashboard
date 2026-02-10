from neo4j import GraphDatabase
import pandas as pd
import config

driver = GraphDatabase.driver(
    config.NEO4J_URI,
    auth=(config.NEO4J_USER, config.NEO4J_PASSWORD)
)

# Clear existing data
with driver.session() as session:
    session.run("MATCH (n) DETACH DELETE n")
    print("🗑️ Cleared existing database")

df = pd.read_csv("data/sample_5yr_data.csv")

def load_data(tx, row):
    query = """
    MERGE (s:Server {name: $server})
    MERGE (a:Application {name: $application})
    MERGE (p:Process {name: $process})
    MERGE (sv:Service {name: $service})
    MERGE (y:Year {year: $year})
    
    MERGE (i:Impact {
        id: $id
    })
    SET i.impact_year = $year,
        i.server = $server,
        i.application = $application,
        i.process = $process,
        i.service = $service
    
    MERGE (s)-[:HAS_IMPACT]->(i)
    MERGE (a)-[:INVOLVED_IN]->(i)
    MERGE (p)-[:EXECUTED_IN]->(i)
    MERGE (sv)-[:PROVIDED_BY]->(i)
    MERGE (y)-[:CONTAINS]->(i)
    """
    
    row_dict = row.to_dict()
    row_dict['id'] = f"{row['server']}_{row['application']}_{row['process']}_{row['service']}_{row['year']}"
    
    tx.run(query, **row_dict)

with driver.session() as session:
    for idx, row in df.iterrows():
        session.execute_write(load_data, row)

print("✅ Database loaded successfully!")
print(f"📊 Total rows processed: {len(df)}")

# Verify
with driver.session() as session:
    servers = session.run("MATCH (s:Server) RETURN count(s) as count").single()['count']
    impacts = session.run("MATCH (i:Impact) RETURN count(i) as count").single()['count']
    print(f"✓ Servers: {servers}")
    print(f"✓ Impacts: {impacts}")
