import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from db.graph_queries import get_servers, get_impact

print("=" * 60)
print("TEST: Query Results")
print("=" * 60)

print("\n🖥️ Available Servers:")
servers = get_servers()
for server in servers:
    print(f"  • {server}")

print(f"\n✓ Total servers loaded: {len(servers)}")

if servers:
    print(f"\n📊 Testing impact query for: {servers[0]}")
    impacts = get_impact(servers[0])
    print(f"✓ Impacts found: {len(impacts)}")
    for impact in impacts[:3]:
        print(f"  • {impact}")
else:
    print("❌ ERROR: No servers found!")
