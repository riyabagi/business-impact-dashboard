from neo4j import GraphDatabase
import config

driver = GraphDatabase.driver(
    config.NEO4J_URI,
    auth=(config.NEO4J_USER, config.NEO4J_PASSWORD)
)

print("=" * 50)
print("VERIFICATION: What's in Neo4j?")
print("=" * 50)

with driver.session() as session:
    # Check all node labels
    result = session.run("MATCH (n) RETURN DISTINCT labels(n) as labels")
    labels = set()
    for row in result:
        labels.update(row['labels'])
    print(f"\n📌 Node Labels Found: {labels}")
    
    # Count nodes by label
    for label in labels:
        result = session.run(f"MATCH (n:{label}) RETURN count(n) as count")
        count = result.single()['count']
        print(f"   - {label}: {count} nodes")
    
    # Check relationship types
    result = session.run("MATCH ()-[r]-() RETURN DISTINCT type(r) as type")
    rel_types = [row['type'] for row in result]
    print(f"\n📌 Relationship Types Found: {rel_types}")
    
    # Sample data
    result = session.run("MATCH (i:Impact) RETURN i LIMIT 3")
    print(f"\n📌 Sample Impact Nodes:")
    for row in result:
        print(f"   {row['i']}")

driver.close()
