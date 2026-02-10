import pandas as pd
import random

servers = [
    "Core Banking Cluster",
    "Payments Gateway Node",
    "Customer Data Platform",
    "Risk Management Server"
]

years = range(2022, 2025)

rows = []

for year in years:
    for server in servers:
        for _ in range(3):
            rows.append({
                "year": year,
                "server": server,
                "application": random.choice([
                    "Transaction System",
                    "Security Engine",
                    "Analytics Platform"
                ]),
                "process": random.choice([
                    "Processing",
                    "Validation",
                    "Authorization"
                ]),
                "service": random.choice([
                    "Secure Platform",
                    "Enterprise Service",
                    "Core System"
                ])
            })

df = pd.DataFrame(rows)
df.to_csv("data/sample_5yr_data.csv", index=False)

print("✅ CSV created")
