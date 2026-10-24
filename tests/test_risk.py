"""Unit tests for the risk rules and data loading. Run with: python -m pytest"""

from datetime import date, timedelta

import pandas as pd

from agriguard import data, risk


def test_levels():
    assert risk.level(80) == "High"
    assert risk.level(50) == "High"
    assert risk.level(30) == "Moderate"
    assert risk.level(10) == "Low"


def test_water_ratio_full_and_dry():
    # 150 mm rain, 100 mm ET0, Kc 1.2 -> 0.8*150 / 120 = 1.0
    assert risk.water_ratio(150, 100, 1.2) == 1.0
    assert risk.water_ratio(0, 100, 1.2) == 0.0


def test_drought_index():
    assert risk.crop_drought_index(1.0, 1.0, tolerant=False) == 0
    assert risk.crop_drought_index(0.4, 1.0, tolerant=False) == 60
    # Tolerant crops feel the same deficit less.
    assert risk.crop_drought_index(0.4, 1.0, tolerant=True) < 60
    # A dry forecast adds the penalty.
    assert risk.crop_drought_index(0.4, 0.2, tolerant=False) == 60 + risk.DRY_FORECAST_PENALTY


def test_flood_and_storage_thresholds():
    assert risk.level(risk.flood_index(40, 40)) == "High"
    assert risk.level(risk.flood_index(5, 80)) == "High"
    assert risk.level(risk.flood_index(5, 20)) == "Low"
    assert risk.level(risk.storage_index(86, 18)) == "High"
    assert risk.level(risk.storage_index(81, 18)) == "Moderate"
    assert risk.level(risk.storage_index(70, 25)) == "Low"


def test_districts_load_all_30_inside_rwanda():
    df = data.load_districts()
    assert len(df) == 30
    assert set(df.province) == set(data.PROVINCES)
    assert df.lat.between(-2.9, -1.0).all() and df.lon.between(28.8, 31.0).all()


def test_crop_shares_sum_to_one_and_crops_known():
    dc = data.load_district_crops()
    assert dc.groupby("district").share.sum().round(6).eq(1).all()
    assert set(dc.crop) <= set(data.load_crops().crop)
    assert set(dc.district) == set(data.load_districts().district)


def _weather(district: str, rain: float, rh: float) -> pd.DataFrame:
    start = date(2026, 1, 1)
    return pd.DataFrame([{
        "district": district, "date": start + timedelta(days=i), "rain_mm": rain,
        "tmax_c": 27, "tmean_c": 21, "rh_pct": rh, "et0_mm": 4.0, "is_forecast": i > 30,
    } for i in range(37)])  # 30 past days, today, 6 forecast days


def test_end_to_end_dry_district_raises_drought_alert():
    wx = pd.concat([_weather("Kirehe", rain=0.5, rh=60), _weather("Musanze", rain=6, rh=60)])
    summary = risk.summarise_weather(wx)
    crop_risk = risk.assess_crops(summary, data.load_district_crops(), data.load_crops())
    districts = risk.assess_districts(summary, crop_risk).set_index("district")
    assert districts.loc["Kirehe", "drought_level"] == "High"
    assert districts.loc["Musanze", "drought_level"] == "Low"

    alerts = risk.alerts(districts.reset_index(), crop_risk)
    assert ((alerts.district == "Kirehe") & (alerts.risk == "Drought")).any()
    assert not (alerts.district == "Musanze").any()
