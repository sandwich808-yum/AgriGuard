"""AgriGuard dashboard. Run with: streamlit run app.py"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from agriguard import data, risk, weather

st.set_page_config(page_title="AgriGuard Rwanda", page_icon="🌱", layout="wide")

LEVEL_COLORS = {"High": "#d64545", "Moderate": "#e8a33d", "Low": "#3f9d5c"}
RISK_SCALE = [(0.0, "#3f9d5c"), (0.25, "#a8c95a"), (0.5, "#e8a33d"), (1.0, "#b02a2a")]
LAYERS = {
    "Overall": ("overall_index", "Highest of the three risks"),
    "Drought": ("drought_index", "Rainfall vs crop water demand, last 30 days"),
    "Flood": ("flood_index", "Heavy rain forecast for the coming week"),
    "Storage": ("storage_index", "Mould risk for stored grain from forecast humidity"),
}

st.markdown("""
<style>
  .block-container {padding-top: 1.6rem;}
  .badge {display:inline-block; padding:2px 10px; border-radius:999px; color:#fff;
          font-size:0.8rem; font-weight:600; margin-right:4px;}
  .alert-card {border-left:5px solid; padding:8px 12px; margin-bottom:8px;
               background:rgba(127,127,127,0.07); border-radius:6px;}
  .alert-card small {opacity:0.8;}
  .sms {font-family:ui-monospace,monospace; font-size:0.85rem; padding:10px 12px;
        border-radius:10px; background:rgba(63,157,92,0.12);}
</style>
""", unsafe_allow_html=True)


def badge(lvl: str, text: str | None = None) -> str:
    return f'<span class="badge" style="background:{LEVEL_COLORS[lvl]}">{text or lvl}</span>'


def season_of(month: int) -> str:
    """Rwanda's agricultural seasons."""
    if month in (9, 10, 11, 12, 1):
        return "Season A (Sep-Jan): planting and growing on the short rains"
    if month in (2, 3, 4, 5, 6):
        return "Season B (Feb-Jun): long rains; Season A harvest in storage"
    return "Season C (Jul-Aug): dry season, irrigated marshland and valley crops"


def select_from_map():
    """Map click callback. Runs before the rerun, so it may still set the
    district selectbox's value."""
    points = st.session_state.map.selection.points
    if points and points[0].get("location"):
        st.session_state.district = points[0]["location"]


@st.cache_data(show_spinner=False)
def load_static():
    return (data.load_geojson(), data.load_districts(), data.load_crops(),
            data.load_district_crops(), data.uses_sample_crop_data())


@st.cache_data(ttl=3 * 3600, show_spinner="Fetching live weather for 30 districts...")
def load_live(districts: pd.DataFrame):
    return weather.load_weather(districts)


geojson, districts, crops, district_crops, sample_crops = load_static()
wx, wx_source, as_of = load_live(districts)
summary = risk.summarise_weather(wx)
crop_risk = risk.assess_crops(summary, district_crops, crops)
dist_risk = risk.assess_districts(summary, crop_risk).merge(districts, on="district")
all_alerts = risk.alerts(dist_risk, crop_risk)

# ---------------------------------------------------------------- sidebar
with st.sidebar:
    st.title("🌱 AgriGuard")
    st.caption("Climate risk alerts for Rwandan farmers")
    layer = st.radio("Risk layer", list(LAYERS), help="Which risk to colour the map by.")
    provinces = st.multiselect("Provinces", list(data.PROVINCES), placeholder="All provinces")
    if "district" not in st.session_state:
        st.session_state.district = dist_risk.sort_values("overall_index").iloc[-1]["district"]
    st.selectbox("District", sorted(districts["district"]), key="district")
    st.divider()
    st.caption(f"📅 {season_of(as_of.month)}")
    st.caption(f"Weather: Open-Meteo, {'live' if wx_source == 'live' else 'offline snapshot'}, "
               f"observed to {as_of:%d %b %Y}, forecast to {wx['date'].max():%d %b}.")

view = dist_risk[dist_risk.province.isin(provinces)] if provinces else dist_risk
view_alerts = all_alerts[all_alerts.district.isin(view.district)]

# ---------------------------------------------------------------- header
st.title("AgriGuard Rwanda")
st.markdown("Early warnings for **drought**, **heavy rain** and **post-harvest storage** risk "
            "in every district, from live weather and national crop statistics.")
if wx_source != "live":
    st.warning("The live weather API is unreachable, so this shows the saved snapshot.", icon="📡")
if sample_crops:
    st.info("District crop mix uses sample shares. Replace data/district_crops.csv with the "
            "NISR Seasonal Agricultural Survey figures to make alerts official.", icon="ℹ️")

k1, k2, k3, k4 = st.columns(4)
k1.metric("Districts at high risk", int((view.overall_level == "High").sum()), help="Any risk at High")
k2.metric("Districts at moderate risk", int((view.overall_level == "Moderate").sum()))
k3.metric("Active alerts", len(view_alerts))
k4.metric("Avg rain, last 30 days", f"{view.rain_30d.mean():.0f} mm")

tab_map, tab_alerts, tab_method = st.tabs(["🗺️ Risk map", "🚨 All alerts", "📘 Method & data"])

# ---------------------------------------------------------------- map tab
with tab_map:
    col_map, col_list = st.columns([3, 2], gap="large")
    col, layer_help = LAYERS[layer]
    with col_map:
        st.subheader(f"{layer} risk by district")
        st.caption(f"{layer_help}. Click a district for details.")
        # A geo choropleth (no tile basemap) is used because Streamlit reports
        # clicks on it, which tile maps don't.
        fig = px.choropleth(
            view, geojson=geojson, locations="district", featureidkey="properties.shapeName",
            color=col, range_color=(0, 100), color_continuous_scale=RISK_SCALE,
            height=500,
            custom_data=["district", "province", "overall_level", "main_risk", "rain_30d", "rain_fc"],
            labels={col: "Risk index"},
        )
        fig.update_traces(marker_line_color="white", marker_line_width=1, hovertemplate=(
            "<b>%{customdata[0]}</b> (%{customdata[1]})<br>Risk index: %{z:.0f}<br>"
            "Overall: %{customdata[2]} (%{customdata[3]})<br>"
            "Rain last 30 days: %{customdata[4]:.0f} mm<br>Forecast this week: %{customdata[5]:.0f} mm"
            "<extra></extra>"))
        # Outline the selected district, then label every district at its centroid.
        fig.add_choropleth(geojson=geojson, featureidkey="properties.shapeName",
                           locations=[st.session_state.district], z=[0], showscale=False,
                           colorscale=[[0, "rgba(0,0,0,0)"], [1, "rgba(0,0,0,0)"]],
                           marker_line_color="#111", marker_line_width=3, hoverinfo="skip")
        fig.add_scattergeo(lat=view.lat, lon=view.lon, text=view.district, mode="text",
                           textfont=dict(size=10, color="#1f2933"), hoverinfo="skip")
        fig.update_geos(visible=False, bgcolor="rgba(0,0,0,0)", projection_type="mercator",
                        fitbounds=False, lonaxis_range=[28.85, 30.9], lataxis_range=[-2.85, -1.05])
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor="rgba(0,0,0,0)",
                          showlegend=False,
                          coloraxis_colorbar=dict(title="Risk", orientation="h", y=-0.02, len=0.8,
                                                  thickness=12, tickvals=[0, 25, 50, 100],
                                                  ticktext=["0", "Moderate", "High", "100"]))
        st.plotly_chart(fig, width="stretch", on_select=select_from_map,
                        selection_mode="points", key="map")

    with col_list:
        st.subheader("Top alerts")
        top = view_alerts[view_alerts.risk == layer] if layer != "Overall" else view_alerts
        if top.empty:
            st.success("No moderate or high alerts for this selection.", icon="✅")
        for a in top.head(6).itertuples():
            st.markdown(
                f'<div class="alert-card" style="border-color:{LEVEL_COLORS[a.level]}">'
                f'{badge(a.level)} <b>{a.district}</b> · {a.risk}<br><small>{a.detail}</small></div>',
                unsafe_allow_html=True)

    # ------------------------------------------------------------ district detail
    st.divider()
    name = st.session_state.district
    d = dist_risk.set_index("district").loc[name]
    st.subheader(f"📍 {name} district, {d.province} Province")
    st.markdown(" ".join(badge(d[f"{r}_level"], f"{r.capitalize()}: {d[f'{r}_level']}")
                         for r in ("drought", "flood", "storage")), unsafe_allow_html=True)

    c1, c2 = st.columns([3, 2], gap="large")
    with c1:
        dw = wx[wx.district == name]
        bars = go.Figure()
        bars.add_bar(x=dw.date, y=dw.rain_mm, name="Rainfall (mm)",
                     marker_color=["#9cc3e6" if f else "#2f6fab" for f in dw.is_forecast])
        bars.add_scatter(x=dw.date, y=dw.et0_mm, name="Crop water demand (ET₀, mm)",
                         mode="lines", line=dict(color="#e8a33d", width=2))
        bars.add_vline(x=pd.Timestamp(as_of).timestamp() * 1000, line_dash="dot", line_color="gray",
                       annotation_text="today", annotation_position="top")
        bars.update_layout(height=320, margin=dict(l=0, r=0, t=28, b=0), hovermode="x unified",
                           legend=dict(orientation="h", y=-0.15), yaxis_title="mm/day")
        st.markdown("**Daily rainfall**: observed (dark blue) and 6-day forecast (light blue)")
        st.plotly_chart(bars, width="stretch")

    with c2:
        st.markdown("**Crops in this district**")
        table = crop_risk[crop_risk.district == name][
            ["crop", "share", "water_met", "drought_level"]].sort_values("share", ascending=False)
        # Surplus rain doesn't help a crop beyond its need, so show at most 100%.
        table["water_met"] = table["water_met"].clip(upper=1)
        st.dataframe(
            table, hide_index=True, width="stretch",
            column_config={
                "crop": st.column_config.TextColumn("Crop", width="small"),
                "share": st.column_config.NumberColumn("Area", format="percent", width="small"),
                "water_met": st.column_config.ProgressColumn("Water need met", format="percent",
                                                             min_value=0, max_value=1),
                "drought_level": st.column_config.TextColumn("Drought", width="small"),
            })
        st.caption(f"Last 30 days: {d.rain_30d:.0f} mm rain vs {d.et0_30d:.0f} mm reference "
                   f"evapotranspiration. Forecast: {d.rain_fc:.0f} mm, humidity {d.rh_fc:.0f}%.")

    local = all_alerts[all_alerts.district == name]
    if local.empty:
        st.success(f"No alerts for {name} this week. Conditions are within normal range.", icon="✅")
    else:
        st.markdown("**Recommended actions and SMS alert preview**")
        for a in local.itertuples():
            ca, cb = st.columns([3, 2], gap="large")
            ca.markdown(f"{badge(a.level)} **{a.risk}**: {a.action}", unsafe_allow_html=True)
            cb.markdown(f'<div class="sms">📱 {a.sms}</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------- alerts tab
with tab_alerts:
    st.subheader("All active alerts")
    f1, f2 = st.columns(2)
    risks = f1.multiselect("Risk type", ["Drought", "Flood", "Storage"],
                           default=["Drought", "Flood", "Storage"])
    levels = f2.multiselect("Level", ["High", "Moderate"], default=["High", "Moderate"])
    shown = view_alerts[view_alerts.risk.isin(risks) & view_alerts.level.isin(levels)]
    st.dataframe(shown[["district", "risk", "level", "index", "detail", "action"]],
                 hide_index=True, width="stretch", height=420,
                 column_config={
                     "district": "District", "risk": "Risk", "level": "Level",
                     "index": st.column_config.ProgressColumn("Index", min_value=0, max_value=100,
                                                              format="%d"),
                     "detail": st.column_config.TextColumn("Why", width="large"),
                     "action": st.column_config.TextColumn("Recommended action", width="large")})
    st.download_button("⬇️ Download alerts (CSV)", shown.to_csv(index=False).encode(),
                       file_name=f"agriguard_alerts_{as_of}.csv", mime="text/csv")

    st.subheader("Risk overview")
    chart_df = view.melt(id_vars="district", value_vars=["drought_index", "flood_index", "storage_index"],
                         var_name="risk", value_name="index")
    chart_df["risk"] = chart_df.risk.str.replace("_index", "").str.capitalize()
    heat = px.density_heatmap(chart_df, x="district", y="risk", z="index", histfunc="avg",
                              color_continuous_scale=RISK_SCALE, range_color=(0, 100), height=280)
    heat.update_layout(margin=dict(l=0, r=0, t=10, b=0), xaxis_title=None, yaxis_title=None,
                       coloraxis_colorbar_title="Index")
    st.plotly_chart(heat, width="stretch")

# ---------------------------------------------------------------- method tab
with tab_method:
    st.subheader("How AgriGuard works")
    st.markdown(f"""
1. **Weather**: every 3 hours the app pulls the last 30 days and a 6-day forecast of rainfall,
   temperature, humidity and FAO-56 reference evapotranspiration (ET₀) from
   [Open-Meteo](https://open-meteo.com) for the centre of each of Rwanda's 30 districts.
2. **Crop mix**: each district's cultivated area by crop comes from `data/district_crops.csv`
   (NISR Seasonal Agricultural Survey format).
3. **Drought risk**: for each crop, crop water demand = ET₀ × FAO crop coefficient (Kc).
   We compare it with effective rainfall (80% of rain). Below 75% of demand met is Moderate,
   below 50% is High. Drought-tolerant crops (cassava, sorghum, sweet potato) are scaled down, and a dry
   forecast adds {risk.DRY_FORECAST_PENALTY} points. District drought risk is the area-weighted average.
4. **Flood risk**: High when the forecast has 40 mm in one day or 80 mm in the week.
5. **Storage risk**: for districts that store grain or pulses, forecast mean humidity above
   80% is Moderate and above 85% is High, increased in warm (22°C or more) lowland districts.
6. **Alerts**: every Moderate or High risk becomes a plain-language alert with a recommended
   action and a 1-SMS-style message for farmers and extension officers.
""")
    st.subheader("Data sources")
    st.markdown("""
- **NISR**: Seasonal Agricultural Survey, crop area by district: [statistics.gov.rw](https://www.statistics.gov.rw)
- **Open-Meteo**: weather forecast and history API (CC BY 4.0)
- **geoBoundaries**: Rwanda district boundaries, ADM2 (CC BY 4.0)
- **FAO Irrigation & Drainage Paper 56**: crop coefficients (Kc)
""")
    st.markdown("**Crop parameters used**")
    st.dataframe(crops, hide_index=True, width="stretch")
