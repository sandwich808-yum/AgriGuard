"""Rule-based climate risk model.

Three risks are scored per district on a 0-100 index:

* Drought / irrigation need: rainfall over the last 30 days compared with the
  crop water demand (FAO-56: reference evapotranspiration x crop coefficient),
  weighted by each crop's share of the district's cultivated area.
* Heavy rain / flooding: forecast daily peak and total rainfall.
* Post-harvest storage: forecast humidity and temperature, which drive mould
  and aflatoxin in stored grain.

Index >= 50 is High, >= 25 is Moderate, otherwise Low. The rules are kept
simple on purpose so every alert can be explained to a farmer or extension
officer in one sentence.
"""

import pandas as pd

from agriguard import i18n

HIGH, MODERATE = 50, 25

# FAO rule of thumb: roughly 80% of rainfall is effective for crops; the rest
# is lost to runoff and deep percolation.
EFFECTIVE_RAIN = 0.8
# Drought-tolerant crops (cassava, sorghum, sweet potato) feel a deficit less.
TOLERANT_FACTOR = 0.7
# Extra drought points when the coming week is also forecast to be dry.
DRY_FORECAST_PENALTY = 15


def level(index: float) -> str:
    if index >= HIGH:
        return "High"
    if index >= MODERATE:
        return "Moderate"
    return "Low"


def clip(x: float) -> float:
    return max(0.0, min(100.0, x))


def water_ratio(rain_mm: float, et0_mm: float, kc: float) -> float:
    """Share of crop water demand met by effective rainfall (1.0 = fully met)."""
    demand = et0_mm * kc
    return EFFECTIVE_RAIN * rain_mm / demand if demand > 0 else 1.0


def crop_drought_index(ratio_past: float, ratio_forecast: float, tolerant: bool) -> float:
    """0 when rainfall meets demand, 100 when there was no rain at all."""
    index = 100 * (1 - ratio_past)
    if tolerant:
        index *= TOLERANT_FACTOR
    if ratio_forecast < 0.5:
        index += DRY_FORECAST_PENALTY
    return clip(index)


def flood_index(max_daily_mm: float, total_mm: float) -> float:
    """High at 40 mm in one day or 80 mm over the forecast week."""
    return clip(max(max_daily_mm * 1.25, total_mm * 0.625))


def storage_index(mean_rh: float, mean_temp_c: float) -> float:
    """Mould risk in stored grain. Daily mean humidity (night included) sits
    around 75-80% in Rwanda's rainy seasons, so alerts start above that
    baseline: Moderate from 80%, High from 85%. Warmth speeds mould growth,
    so lowland districts get a boost over the cool highlands."""
    index = (mean_rh - 75) * 5
    if mean_temp_c >= 22:
        index *= 1.2
    return clip(index)


def summarise_weather(weather: pd.DataFrame) -> pd.DataFrame:
    """Per-district totals for the observed period and the forecast."""
    past = weather[~weather["is_forecast"]].groupby("district").agg(
        rain_30d=("rain_mm", "sum"), et0_30d=("et0_mm", "sum"))
    fc = weather[weather["is_forecast"]].groupby("district").agg(
        rain_fc=("rain_mm", "sum"), rain_fc_max=("rain_mm", "max"),
        et0_fc=("et0_mm", "sum"), rh_fc=("rh_pct", "mean"), temp_fc=("tmean_c", "mean"))
    return past.join(fc).reset_index()


def assess_crops(summary: pd.DataFrame, district_crops: pd.DataFrame,
                 crops: pd.DataFrame) -> pd.DataFrame:
    """Drought risk for every district/crop pair."""
    df = district_crops.merge(crops, on="crop").merge(summary, on="district")
    df["water_met"] = [water_ratio(r, e, k) for r, e, k in zip(df.rain_30d, df.et0_30d, df.kc_mid)]
    fc_ratio = [water_ratio(r, e, k) for r, e, k in zip(df.rain_fc, df.et0_fc, df.kc_mid)]
    df["drought_index"] = [crop_drought_index(p, f, t)
                           for p, f, t in zip(df.water_met, fc_ratio, df.drought_tolerant)]
    df["drought_level"] = df["drought_index"].map(level)
    return df


def assess_districts(summary: pd.DataFrame, crop_risk: pd.DataFrame) -> pd.DataFrame:
    """One row per district with the three risk indices and an overall level."""
    weighted = crop_risk.assign(w=crop_risk.drought_index * crop_risk.share)
    drought = weighted.groupby("district")["w"].sum().rename("drought_index")
    storage_share = (crop_risk[crop_risk.storage_sensitive].groupby("district")["share"]
                     .sum().rename("storage_crop_share"))

    df = summary.set_index("district").join(drought).join(storage_share).reset_index()
    df["storage_crop_share"] = df["storage_crop_share"].fillna(0)
    df["drought_index"] = df["drought_index"].fillna(0)
    df["flood_index"] = [flood_index(m, t) for m, t in zip(df.rain_fc_max, df.rain_fc)]
    # Storage risk only matters where grain or pulses are stored.
    df["storage_index"] = [storage_index(h, t) if s > 0 else 0.0
                           for h, t, s in zip(df.rh_fc, df.temp_fc, df.storage_crop_share)]
    indices = ["drought_index", "flood_index", "storage_index"]
    df["overall_index"] = df[indices].max(axis=1)
    df["main_risk"] = df[indices].idxmax(axis=1).str.replace("_index", "").str.capitalize()
    for col in indices + ["overall_index"]:
        df[col.replace("_index", "_level")] = df[col].map(level)
    return df


def alerts(districts: pd.DataFrame, crop_risk: pd.DataFrame, lang: str = "en") -> pd.DataFrame:
    """Plain-language alerts for every Moderate or High risk, most severe first.

    `risk` and `level` stay as English codes for filtering and colours; the
    `*_label`, `detail`, `action` and `sms` columns are in `lang`."""
    rows = []
    for d in districts.itertuples():
        for risk in ("Drought", "Flood", "Storage"):
            idx = getattr(d, f"{risk.lower()}_index")
            lvl = level(idx)
            if lvl == "Low":
                continue
            if risk == "Drought":
                hit = crop_risk[(crop_risk.district == d.district) & (crop_risk.drought_level != "Low")]
                crops = ", ".join(i18n.crop_name(c, lang) for c in
                                  hit.sort_values("drought_index", ascending=False).crop)
                detail = i18n.t("detail_Drought", lang, rain=f"{d.rain_30d:.0f}", fc=f"{d.rain_fc:.0f}",
                                crops=crops or i18n.t("main_crops", lang))
            elif risk == "Flood":
                detail = i18n.t("detail_Flood", lang, max=f"{d.rain_fc_max:.0f}", fc=f"{d.rain_fc:.0f}")
            else:
                detail = i18n.t("detail_Storage", lang, rh=f"{d.rh_fc:.0f}", temp=f"{d.temp_fc:.0f}")
            action = i18n.action(risk, lvl, lang)
            rows.append({
                "district": d.district, "risk": risk, "level": lvl, "index": round(idx),
                "risk_label": i18n.risk_name(risk, lang), "level_label": i18n.level_name(lvl, lang),
                "detail": detail, "action": action,
                # The SMS carries only the first, most important action.
                "sms": i18n.t("sms", lang, level=i18n.level_name(lvl, lang).upper(),
                              risk=i18n.risk_name(risk, lang).upper(), district=d.district,
                              detail=detail, action=action.split(";")[0].strip()),
            })
    df = pd.DataFrame(rows, columns=["district", "risk", "level", "index", "risk_label",
                                     "level_label", "detail", "action", "sms"])
    return df.sort_values("index", ascending=False).reset_index(drop=True)
