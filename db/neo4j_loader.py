import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from neo4j import GraphDatabase
import pandas as pd
import config

driver = GraphDatabase.driver(
    config.NEO4J_URI,
    auth=(config.NEO4J_USER, config.NEO4J_PASSWORD)
)

df = pd.read_csv("data/sample_5yr_data.csv")

def load(tx, row):
    tx.run("""
    MERGE (s:Server {name:$server})
    MERGE (a:Application {name:$application})
    MERGE (p:BusinessProcess {name:$process})
    MERGE (sv:BusinessService {name:$service})

    MERGE (s)-[:HOSTS]->(a)
    MERGE (a)-[:SUPPORTS]->(p)
    MERGE (p)-[:ENABLES]->(sv)
    """, **row)

with driver.session() as session:
    for _, row in df.iterrows():
        session.execute_write(load, row.to_dict())

print("✅ Data loaded into Neo4j")
