import pandas as pd

def classify_excursions(sensor_df: pd.DataFrame) -> pd.DataFrame:
    df = sensor_df.copy()
    df["outside_range"] = (
        (df["temperature_c"] < df["allowed_min_c"])
        | (df["temperature_c"] > df["allowed_max_c"])
    )

    deviation = pd.concat([
        (df["temperature_c"] - df["allowed_max_c"]).clip(lower=0),
        (df["allowed_min_c"] - df["temperature_c"]).clip(lower=0),
    ], axis=1).max(axis=1)

    df["deviation_c"] = deviation.round(1)

    def severity(row):
        if not row["outside_range"]:
            return "Normal"
        d = row["deviation_c"]
        if d <= 2:
            return "Minor"
        if d <= 5:
            return "Major"
        return "Critical"

    df["severity"] = df.apply(severity, axis=1)
    return df.sort_values("deviation_c", ascending=False).reset_index(drop=True)

def cold_chain_summary(sensor_df: pd.DataFrame):
    checked = classify_excursions(sensor_df)
    excursions = checked[checked["outside_range"]]
    return {
        "sensor_readings": len(checked),
        "excursions": len(excursions),
        "minor": int((checked["severity"] == "Minor").sum()),
        "major": int((checked["severity"] == "Major").sum()),
        "critical": int((checked["severity"] == "Critical").sum()),
    }, checked
