def get_impact(tx, server_name):
    result = tx.run("""
    MATCH (s:Server {name:$server})-[:HOSTS]->(a)
          -[:SUPPORTS]->(p)-[:ENABLES]->(sv)
    RETURN a.name AS application,
           p.name AS process,
           sv.name AS service
    """, server=server_name)

    return result.data()
