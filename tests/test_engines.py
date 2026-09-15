import sys
from pathlib import Path
import pandas as pd

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from services.risk_engine import score_shipments
from services.route_optimizer import rank_routes
from services.fleet_optimizer import idle_assets
from services.cold_chain import classify_excursions

def test_risk_score_orders_high_risk_first():
    shipments = pd.DataFrame([{
        "shipment_id":"A","route_id":"R1","priority":"Critical","current_delay_hours":10,
        "weather_risk":0.9,"traffic_level":"High","disruption_active":True,
        "origin":"A","destination":"B","distance_km":100,"scheduled_hours":5,"cold_chain":False
    },{
        "shipment_id":"B","route_id":"R2","priority":"Standard","current_delay_hours":0,
        "weather_risk":0.1,"traffic_level":"Low","disruption_active":False,
        "origin":"A","destination":"B","distance_km":100,"scheduled_hours":5,"cold_chain":False
    }])
    disruptions = pd.DataFrame([{
        "disruption_id":"D1","type":"Storm","location":"A","severity":"Critical",
        "duration_hours":10,"affected_route":"R1"
    }])
    scored = score_shipments(shipments, disruptions)
    assert scored.iloc[0]["shipment_id"] == "A"
    assert scored.iloc[0]["risk_score"] > scored.iloc[1]["risk_score"]

def test_route_optimizer_returns_recommendation():
    routes = pd.DataFrame([
        {"route_id":"R1","origin":"A","destination":"B","distance_km":100,"estimated_hours":5,
         "base_cost_inr":1000,"route_risk":0.9,"traffic_level":"High"},
        {"route_id":"R1-B","origin":"A","destination":"B","distance_km":120,"estimated_hours":6,
         "base_cost_inr":1200,"route_risk":0.2,"traffic_level":"Low"},
    ])
    disruptions = pd.DataFrame([{
        "disruption_id":"D1","type":"Closure","location":"A","severity":"Critical",
        "duration_hours":12,"affected_route":"R1"
    }])
    ranked = rank_routes(routes, disruptions, "A", "B")
    assert ranked.iloc[0]["recommendation"] == "Recommended"
    assert ranked.iloc[0]["route_id"] == "R1-B"

def test_idle_assets_filters_available_low_utilisation():
    fleet = pd.DataFrame([
        {"vehicle_id":"V1","vehicle_type":"Truck","capacity_tons":10,"current_location":"A",
         "status":"Available","utilization":0.2,"fuel_efficiency_kmpl":4},
        {"vehicle_id":"V2","vehicle_type":"Truck","capacity_tons":10,"current_location":"A",
         "status":"In Transit","utilization":0.1,"fuel_efficiency_kmpl":4},
    ])
    result = idle_assets(fleet)
    assert list(result["vehicle_id"]) == ["V1"]

def test_cold_chain_severity():
    sensors = pd.DataFrame([
        {"sensor_id":"S1","shipment_id":"SH1","timestamp":"2026-09-14 10:00",
         "temperature_c":5,"humidity_pct":50,"allowed_min_c":2,"allowed_max_c":8},
        {"sensor_id":"S2","shipment_id":"SH1","timestamp":"2026-09-14 11:00",
         "temperature_c":14,"humidity_pct":50,"allowed_min_c":2,"allowed_max_c":8},
    ])
    result = classify_excursions(sensors)
    assert result.iloc[0]["severity"] == "Critical"
