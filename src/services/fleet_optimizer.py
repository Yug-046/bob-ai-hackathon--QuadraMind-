import pandas as pd

def idle_assets(fleet: pd.DataFrame, threshold: float = 0.35) -> pd.DataFrame:
    df = fleet.copy()
    return df[
        (df["status"] == "Available") & (df["utilization"] <= threshold)
    ].sort_values(["utilization", "capacity_tons"]).reset_index(drop=True)

def recommend_redeployment(fleet: pd.DataFrame, shipments: pd.DataFrame) -> pd.DataFrame:
    idle = idle_assets(fleet).copy()
    if idle.empty:
        return idle

    high_need = shipments[
        shipments["risk_score"] >= 60
    ].copy()

    if high_need.empty:
        idle["recommended_for"] = "No urgent shipment"
        return idle

    high_need = high_need.sort_values("risk_score", ascending=False)
    recommendations = []
    for idx, (_, asset) in enumerate(idle.iterrows()):
        target = high_need.iloc[idx % len(high_need)]
        recommendations.append({
            **asset.to_dict(),
            "recommended_for": target["shipment_id"],
            "shipment_risk": target["risk_score"],
            "origin": target["origin"],
            "destination": target["destination"],
        })
    return pd.DataFrame(recommendations)
