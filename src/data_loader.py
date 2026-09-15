from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent / "data"

def load_data():
    shipments = pd.read_csv(DATA_DIR / "shipments.csv")
    fleet = pd.read_csv(DATA_DIR / "fleet.csv")
    routes = pd.read_csv(DATA_DIR / "routes.csv")
    disruptions = pd.read_csv(DATA_DIR / "disruptions.csv")
    cold_chain = pd.read_csv(DATA_DIR / "cold_chain.csv")
    return shipments, fleet, routes, disruptions, cold_chain
