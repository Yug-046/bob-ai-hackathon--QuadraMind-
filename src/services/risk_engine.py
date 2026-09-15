import pandas as pd

TRAFFIC_SCORE = {"Low": 0.15, "Medium": 0.50, "High": 0.90}
PRIORITY_SCORE = {"Standard": 0.25, "Priority": 0.65, "Critical": 1.00}
SEVERITY_SCORE = {"Low": 0.20, "Medium": 0.50, "High": 0.80, "Critical": 1.00}

def _clamp(value, low=0.0, high=1.0):
    return max(low, min(high, float(value)))

def score_shipments(shipments: pd.DataFrame, disruptions: pd.DataFrame) -> pd.DataFrame:
    df = shipments.copy()

    active_routes = set(disruptions["affected_route"].astype(str))
    severity_by_route = (
        disruptions.groupby("affected_route")["severity"]
        .agg(lambda s: max((SEVERITY_SCORE.get(x, 0.2) for x in s), default=0.0))
        .to_dict()
    )

    df["traffic_score"] = df["traffic_level"].map(TRAFFIC_SCORE).fillna(0.5)
    df["delay_score"] = (df["current_delay_hours"] / 12).clip(0, 1)
    df["route_disruption_score"] = df["route_id"].astype(str).map(severity_by_route).fillna(0.0)
    df["priority_score"] = df["priority"].map(PRIORITY_SCORE).fillna(0.25)

    df["risk_score"] = (
        0.25 * df["weather_risk"]
        + 0.20 * df["traffic_score"]
        + 0.20 * df["delay_score"]
        + 0.20 * df["route_disruption_score"]
        + 0.10 * df["priority_score"]
        + 0.05 * df["disruption_active"].astype(float)
    ) * 100

    df["risk_score"] = df["risk_score"].round(1)
    df["risk_level"] = pd.cut(
        df["risk_score"],
        bins=[-1, 30, 60, 80, 101],
        labels=["Low", "Medium", "High", "Critical"],
    ).astype(str)

    def reason(row):
        reasons = []
        if row["weather_risk"] >= 0.65:
            reasons.append("weather")
        if row["traffic_score"] >= 0.75:
            reasons.append("traffic")
        if row["current_delay_hours"] >= 5:
            reasons.append("current delay")
        if row["route_disruption_score"] >= 0.75:
            reasons.append("active disruption")
        if row["priority"] == "Critical":
            reasons.append("critical priority")
        return ", ".join(reasons) if reasons else "combined operational factors"

    df["risk_reason"] = df.apply(reason, axis=1)
    df["affected_by_disruption"] = df["route_id"].astype(str).isin(active_routes)
    return df.sort_values("risk_score", ascending=False).reset_index(drop=True)

def dashboard_metrics(scored):
    return {
        "shipments": len(scored),
        "high_risk": int((scored["risk_score"] >= 60).sum()),
        "critical": int((scored["risk_score"] >= 80).sum()),
        "affected": int(scored["affected_by_disruption"].sum()),
    }
