from pathlib import Path
import random
import pandas as pd

SEED = 42
random.seed(SEED)

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)

CITIES = [
    ("Mumbai", "Ahmedabad"), ("Ahmedabad", "Delhi"), ("Delhi", "Jaipur"),
    ("Pune", "Mumbai"), ("Bengaluru", "Hyderabad"), ("Hyderabad", "Chennai"),
    ("Chennai", "Bengaluru"), ("Kolkata", "Bhubaneswar"), ("Delhi", "Lucknow"),
    ("Pune", "Nagpur"), ("Ahmedabad", "Jaipur"), ("Mumbai", "Pune"),
]

ROUTES = []
for i, (origin, destination) in enumerate(CITIES, 1):
    base_distance = random.randint(250, 1450)
    base_hours = round(base_distance / random.uniform(48, 62), 1)
    ROUTES.append({
        "route_id": f"R-{i:03d}",
        "origin": origin,
        "destination": destination,
        "distance_km": base_distance,
        "estimated_hours": base_hours,
        "base_cost_inr": int(base_distance * random.uniform(24, 34)),
        "route_risk": round(random.uniform(0.08, 0.48), 2),
        "traffic_level": random.choice(["Low", "Medium", "High"]),
    })

route_rows = []
for r in ROUTES:
    route_rows.append(r)
    # Alternate route with different time/cost/risk profile.
    alt = r.copy()
    alt["route_id"] = r["route_id"] + "-B"
    alt["distance_km"] = int(r["distance_km"] * random.uniform(1.05, 1.25))
    alt["estimated_hours"] = round(r["estimated_hours"] * random.uniform(0.82, 1.08), 1)
    alt["base_cost_inr"] = int(r["base_cost_inr"] * random.uniform(1.03, 1.22))
    alt["route_risk"] = round(max(0.03, r["route_risk"] * random.uniform(0.45, 0.9)), 2)
    alt["traffic_level"] = random.choice(["Low", "Medium"])
    route_rows.append(alt)

pd.DataFrame(route_rows).to_csv(DATA / "routes.csv", index=False)

fleet = []
for i in range(1, 31):
    util = round(random.uniform(0.12, 0.96), 2)
    fleet.append({
        "vehicle_id": f"VH-{i:03d}",
        "vehicle_type": random.choice(["Truck", "Reefer Truck", "Container Chassis", "Vessel"]),
        "capacity_tons": random.choice([8, 12, 18, 24, 30]),
        "current_location": random.choice(sorted({c for pair in CITIES for c in pair})),
        "status": random.choice(["Available", "Available", "In Transit", "Maintenance"]),
        "utilization": util,
        "fuel_efficiency_kmpl": round(random.uniform(2.5, 5.2), 2),
    })
pd.DataFrame(fleet).to_csv(DATA / "fleet.csv", index=False)

disruptions = [
    {"disruption_id":"D-001","type":"Heavy Rain","location":"Mumbai","severity":"High","duration_hours":18,"affected_route":"R-001"},
    {"disruption_id":"D-002","type":"Port Strike","location":"Mumbai","severity":"Critical","duration_hours":30,"affected_route":"R-012"},
    {"disruption_id":"D-003","type":"Road Closure","location":"Ahmedabad","severity":"High","duration_hours":12,"affected_route":"R-002"},
    {"disruption_id":"D-004","type":"Heat Wave","location":"Delhi","severity":"Medium","duration_hours":20,"affected_route":"R-003"},
    {"disruption_id":"D-005","type":"Geopolitical Delay","location":"Delhi","severity":"Critical","duration_hours":36,"affected_route":"R-009"},
]
pd.DataFrame(disruptions).to_csv(DATA / "disruptions.csv", index=False)

shipment_rows = []
route_df = pd.DataFrame(route_rows)
fleet_df = pd.DataFrame(fleet)
for i in range(1, 121):
    r = route_df.sample(1, random_state=SEED + i).iloc[0]
    cold = random.random() < 0.28
    shipment_rows.append({
        "shipment_id": f"SH-{1000+i}",
        "origin": r["origin"],
        "destination": r["destination"],
        "route_id": r["route_id"],
        "vehicle_id": random.choice(fleet_df["vehicle_id"].tolist()),
        "priority": random.choice(["Standard", "Priority", "Critical"]),
        "distance_km": int(r["distance_km"]),
        "scheduled_hours": float(r["estimated_hours"]),
        "current_delay_hours": round(max(0, random.gauss(2.4, 2.2)), 1),
        "weather_risk": round(random.uniform(0.05, 0.95), 2),
        "traffic_level": random.choice(["Low", "Medium", "High"]),
        "disruption_active": random.random() < 0.30,
        "cold_chain": cold,
    })
pd.DataFrame(shipment_rows).to_csv(DATA / "shipments.csv", index=False)

temp_rows = []
for i in range(1, 241):
    shipment_id = random.choice(pd.DataFrame(shipment_rows)["shipment_id"].tolist())
    cold = pd.DataFrame(shipment_rows).set_index("shipment_id").loc[shipment_id, "cold_chain"]
    if not cold:
        continue
    target = random.choice([2.0, 5.0, 8.0])
    temp = round(random.gauss(target, 1.8), 1)
    if random.random() < 0.10:
        temp += random.choice([7, 10, 15])
    temp_rows.append({
        "sensor_id": f"S-{i:04d}",
        "shipment_id": shipment_id,
        "timestamp": f"2026-09-{random.randint(1,14):02d} {random.randint(0,23):02d}:00",
        "temperature_c": temp,
        "humidity_pct": round(random.uniform(35, 85), 1),
        "allowed_min_c": 2.0,
        "allowed_max_c": 8.0,
    })
pd.DataFrame(temp_rows).to_csv(DATA / "cold_chain.csv", index=False)

print(f"Generated synthetic data in {DATA}")
