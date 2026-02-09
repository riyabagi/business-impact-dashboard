import pandas as pd
import random

# ---------- MEDIUM SERVER SET ----------
servers = [
    "Core Banking Cluster",
    "Payments Gateway Node",
    "Customer Data Platform",
    "Risk Management Server"
]

# ---------- WORD POOLS ----------
app_words = [
    "Transaction", "Account", "Security",
    "Customer", "Digital", "Analytics"
]

process_words = [
    "Processing", "Validation",
    "Management", "Authorization"
]

service_words = [
    "Platform", "Service",
    "System", "Engine"
]

# 🔥 Medium size settings
years = range(2022, 2025)   # 3 years
apps_per_server = 3         # 3 apps each

rows = []

for year in years:
    for server in servers:

        for _ in range(apps_per_server):

            app = f"{random.choice(app_words)} {random.choice(['System','Engine'])}"
            process = f"{random.choice(app_words)} {random.choice(process_words)}"
            service = f"{random.choice(['Secure','Enterprise'])} {random.choice(service_words)}"

            rows.append({
                "year": year,
                "server": server,
                "application": app,
                "process": process,
                "service": service,
                "resolution_time_minutes": random.randint(5, 120)
            })

df = pd.DataFrame(rows)

df.to_csv("data/sample_5yr_data.csv", index=False)

print("✅ Medium dataset generated!")
print("Rows:", len(df))
