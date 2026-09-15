import pandas as pd

def rank_routes(routes: pd.DataFrame, disruptions: pd.DataFrame, origin: str, destination: str) -> pd.DataFrame:
    candidates = routes[
        (routes["origin"].str.lower() == origin.lower())
        & (routes["destination"].str.lower() == destination.lower())
    ].copy()

    if candidates.empty:
        return candidates

    disruption_severity = {
        "Low": 0.20, "Medium": 0.50, "High": 0.80, "Critical": 1.00
    }
    affected = {}
    for _, row in disruptions.iterrows():
        affected[row["affected_route"]] = max(
            affected.get(row["affected_route"], 0),
            disruption_severity.get(row["severity"], 0.2),
        )

    candidates["disruption_penalty"] = candidates["route_id"].map(affected).fillna(0.0)
    candidates["effective_risk"] = (
        0.65 * candidates["route_risk"] + 0.35 * candidates["disruption_penalty"]
    ).clip(0, 1)

    max_time = max(candidates["estimated_hours"].max(), 1)
    max_cost = max(candidates["base_cost_inr"].max(), 1)
    candidates["time_score"] = candidates["estimated_hours"] / max_time
    candidates["cost_score"] = candidates["base_cost_inr"] / max_cost

    # Lower is better. Risk is deliberately weighted highest because the goal is disruption resilience.
    candidates["optimizer_score"] = (
        0.55 * candidates["effective_risk"]
        + 0.25 * candidates["time_score"]
        + 0.20 * candidates["cost_score"]
    )
    candidates["optimizer_score"] = candidates["optimizer_score"].round(3)
    candidates["recommendation"] = "Alternative"
    if not candidates.empty:
        candidates.loc[candidates["optimizer_score"].idxmin(), "recommendation"] = "Recommended"

    return candidates.sort_values("optimizer_score").reset_index(drop=True)
