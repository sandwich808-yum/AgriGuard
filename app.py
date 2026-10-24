"""AgriGuard dashboard. Run with: streamlit run app.py"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from agriguard import data, i18n, risk, weather

st.set_page_config(page_title="AgriGuard Rwanda", page_icon="🌱", layout="wide")

LEVEL_COLORS = {"High": "#d64545", "Moderate": "#e8a33d", "Low": "#3f9d5c"}
RISK_SCALE = [(0.0, "#3f9d5c"), (0.25, "#a8c95a"), (0.5, "#e8a33d"), (1.0, "#b02a2a")]
LAYERS = {"Overall": "overall_index", "Drought": "drought_index",
          "Flood": "flood_index", "Storage": "storage_index"}

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


def badge(lvl: str, text: str) -> str:
    return f'<span class="badge" style="background:{LEVEL_COLORS[lvl]}">{text}</span>'


def season_key(month: int) -> str:
    """Rwanda's agricultural seasons: A Sep-Jan, B Feb-Jun, C Jul-Aug."""
    if month in (9, 10, 11, 12, 1):
        return "season_A"
    if month in (2, 3, 4, 5, 6):
        return "season_B"
    return "season_C"


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


@st.cache_data(ttl=3 * 3600, show_spinner=False)
def load_live(districts: pd.DataFrame):
    return weather.load_weather(districts)


# Language comes first so every label below can use it.
lang = st.sidebar.selectbox("🌐 Language · Langue · Ururimi", list(i18n.LANGUAGES),
                            format_func=i18n.LANGUAGES.get, key="lang")


def tr(key: str, **kwargs) -> str:
    return i18n.t(key, lang, **kwargs)


geojson, districts, crops, district_crops, sample_crops = load_static()
with st.spinner(tr("loading")):
    wx, wx_source, as_of = load_live(districts)
summary = risk.summarise_weather(wx)
crop_risk = risk.assess_crops(summary, district_crops, crops)
dist_risk = risk.assess_districts(summary, crop_risk).merge(districts, on="district")
dist_risk["province_label"] = dist_risk.province.map(lambda p: i18n.province_name(p, lang))
dist_risk["overall_label"] = dist_risk.overall_level.map(lambda v: i18n.level_name(v, lang))
dist_risk["main_risk_label"] = dist_risk.main_risk.map(lambda v: i18n.risk_name(v, lang))
all_alerts = risk.alerts(dist_risk, crop_risk, lang)

# ---------------------------------------------------------------- sidebar
with st.sidebar:
    st.title("🌱 AgriGuard")
    st.caption(tr("tagline"))
    layer = st.radio(tr("layer_label"), list(LAYERS), help=tr("layer_help"),
                     format_func=lambda r: i18n.risk_name(r, lang))
    provinces = st.multiselect(tr("provinces"), list(data.PROVINCES), placeholder=tr("all_provinces"),
                               format_func=lambda p: i18n.province_name(p, lang))
    if "district" not in st.session_state:
        st.session_state.district = dist_risk.sort_values("overall_index").iloc[-1]["district"]
    st.selectbox(tr("district"), sorted(districts["district"]), key="district")
    st.divider()
    st.caption(f"📅 {tr(season_key(as_of.month))}")
    st.caption(tr("weather_caption", source=tr("source_live" if wx_source == "live" else "source_snapshot"),
                  as_of=f"{as_of:%d/%m/%Y}", fc_end=f"{wx['date'].max():%d/%m}"))

view = dist_risk[dist_risk.province.isin(provinces)] if provinces else dist_risk
view_alerts = all_alerts[all_alerts.district.isin(view.district)]

# ---------------------------------------------------------------- header
st.title("AgriGuard Rwanda")
st.markdown(tr("intro"))
if wx_source != "live":
    st.warning(tr("api_down"), icon="📡")
if sample_crops:
    st.info(tr("sample_notice"), icon="ℹ️")

k1, k2, k3, k4 = st.columns(4)
k1.metric(tr("kpi_high"), int((view.overall_level == "High").sum()), help=tr("kpi_high_help"))
k2.metric(tr("kpi_moderate"), int((view.overall_level == "Moderate").sum()))
k3.metric(tr("kpi_alerts"), len(view_alerts))
k4.metric(tr("kpi_rain"), f"{view.rain_30d.mean():.0f} mm")

tab_map, tab_alerts, tab_method = st.tabs([tr("tab_map"), tr("tab_alerts"), tr("tab_method")])

# ---------------------------------------------------------------- map tab
with tab_map:
    col_map, col_list = st.columns([3, 2], gap="large")
    col = LAYERS[layer]
    with col_map:
        st.subheader(tr("map_title", layer=i18n.risk_name(layer, lang)))
        st.caption(f"{tr('desc_' + layer)}. {tr('map_click')}")
        # A geo choropleth (no tile basemap) is used because Streamlit reports
        # clicks on it, which tile maps don't.
        fig = px.choropleth(
            view, geojson=geojson, locations="district", featureidkey="properties.shapeName",
            color=col, range_color=(0, 100), color_continuous_scale=RISK_SCALE,
            height=500,
            custom_data=["district", "province_label", "overall_label", "main_risk_label",
                         "rain_30d", "rain_fc"],
            labels={col: tr("risk_index")},
        )
        fig.update_traces(marker_line_color="white", marker_line_width=1, hovertemplate=(
            f"<b>%{{customdata[0]}}</b> (%{{customdata[1]}})<br>{tr('risk_index')}: %{{z:.0f}}<br>"
            f"{tr('hover_overall')}: %{{customdata[2]}} (%{{customdata[3]}})<br>"
            f"{tr('hover_rain30')}: %{{customdata[4]:.0f}} mm<br>"
            f"{tr('hover_fc')}: %{{customdata[5]:.0f}} mm<extra></extra>"))
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
                          coloraxis_colorbar=dict(title=tr("colorbar"), orientation="h", y=-0.02,
                                                  len=0.8, thickness=12, tickvals=[0, 25, 50, 100],
                                                  ticktext=["0", i18n.level_name("Moderate", lang),
                                                            i18n.level_name("High", lang), "100"]))
        st.plotly_chart(fig, width="stretch", on_select=select_from_map,
                        selection_mode="points", key="map")

    with col_list:
        st.subheader(tr("top_alerts"))
        top = view_alerts[view_alerts.risk == layer] if layer != "Overall" else view_alerts
        if top.empty:
            st.success(tr("no_alerts_selection"), icon="✅")
        for a in top.head(6).itertuples():
            st.markdown(
                f'<div class="alert-card" style="border-color:{LEVEL_COLORS[a.level]}">'
                f'{badge(a.level, a.level_label)} <b>{a.district}</b> · {a.risk_label}'
                f'<br><small>{a.detail}</small></div>',
                unsafe_allow_html=True)

    # ------------------------------------------------------------ district detail
    st.divider()
    name = st.session_state.district
    d = dist_risk.set_index("district").loc[name]
    st.subheader("📍 " + tr("district_heading", name=name, province=d.province_label))
    st.markdown(" ".join(
        badge(d[f"{r.lower()}_level"],
              f"{i18n.risk_name(r, lang)}: {i18n.level_name(d[f'{r.lower()}_level'], lang)}")
        for r in ("Drought", "Flood", "Storage")), unsafe_allow_html=True)

    c1, c2 = st.columns([3, 2], gap="large")
    with c1:
        dw = wx[wx.district == name]
        bars = go.Figure()
        bars.add_bar(x=dw.date, y=dw.rain_mm, name=tr("rain_legend"),
                     marker_color=["#9cc3e6" if f else "#2f6fab" for f in dw.is_forecast])
        bars.add_scatter(x=dw.date, y=dw.et0_mm, name=tr("demand_legend"),
                         mode="lines", line=dict(color="#e8a33d", width=2))
        bars.add_vline(x=pd.Timestamp(as_of).timestamp() * 1000, line_dash="dot", line_color="gray",
                       annotation_text=tr("today"), annotation_position="top")
        bars.update_layout(height=320, margin=dict(l=0, r=0, t=28, b=0), hovermode="x unified",
                           legend=dict(orientation="h", y=-0.15), yaxis_title=tr("mm_day"))
        st.markdown(tr("rain_title"))
        st.plotly_chart(bars, width="stretch")

    with c2:
        st.markdown(tr("crops_here"))
        table = crop_risk[crop_risk.district == name][
            ["crop", "share", "water_met", "drought_level"]].sort_values("share", ascending=False)
        table["crop"] = table.crop.map(lambda c: i18n.crop_name(c, lang))
        table["drought_level"] = table.drought_level.map(lambda v: i18n.level_name(v, lang))
        # Surplus rain doesn't help a crop beyond its need, so show at most 100%.
        table["water_met"] = table["water_met"].clip(upper=1)
        st.dataframe(
            table, hide_index=True, width="stretch",
            column_config={
                "crop": st.column_config.TextColumn(tr("col_crop"), width="small"),
                "share": st.column_config.NumberColumn(tr("col_area"), format="percent", width="small"),
                "water_met": st.column_config.ProgressColumn(tr("col_water"), format="percent",
                                                             min_value=0, max_value=1),
                "drought_level": st.column_config.TextColumn(i18n.risk_name("Drought", lang),
                                                             width="small"),
            })
        st.caption(tr("crop_caption", rain=f"{d.rain_30d:.0f}", et0=f"{d.et0_30d:.0f}",
                      fc=f"{d.rain_fc:.0f}", rh=f"{d.rh_fc:.0f}"))

    local = all_alerts[all_alerts.district == name]
    if local.empty:
        st.success(tr("no_alerts_district", name=name), icon="✅")
    else:
        st.markdown(tr("actions_heading"))
        for a in local.itertuples():
            ca, cb = st.columns([3, 2], gap="large")
            ca.markdown(f"{badge(a.level, a.level_label)} **{a.risk_label}**: {a.action}",
                        unsafe_allow_html=True)
            cb.markdown(f'<div class="sms">📱 {a.sms}</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------- alerts tab
with tab_alerts:
    st.subheader(tr("all_alerts"))
    f1, f2 = st.columns(2)
    risks = f1.multiselect(tr("risk_type"), ["Drought", "Flood", "Storage"],
                           default=["Drought", "Flood", "Storage"],
                           format_func=lambda r: i18n.risk_name(r, lang))
    levels = f2.multiselect(tr("level"), ["High", "Moderate"], default=["High", "Moderate"],
                            format_func=lambda v: i18n.level_name(v, lang))
    shown = view_alerts[view_alerts.risk.isin(risks) & view_alerts.level.isin(levels)]
    shown = shown[["district", "risk_label", "level_label", "index", "detail", "action"]]
    st.dataframe(shown, hide_index=True, width="stretch", height=420,
                 column_config={
                     "district": tr("district"), "risk_label": tr("col_risk"),
                     "level_label": tr("level"),
                     "index": st.column_config.ProgressColumn(tr("col_index"), min_value=0,
                                                              max_value=100, format="%d"),
                     "detail": st.column_config.TextColumn(tr("col_why"), width="large"),
                     "action": st.column_config.TextColumn(tr("col_action"), width="large")})
    st.download_button(tr("download"), shown.to_csv(index=False).encode("utf-8-sig"),
                       file_name=f"agriguard_alerts_{lang}_{as_of}.csv", mime="text/csv")

    st.subheader(tr("overview"))
    chart_df = view.melt(id_vars="district", value_vars=["drought_index", "flood_index", "storage_index"],
                         var_name="risk", value_name="index")
    chart_df["risk"] = chart_df.risk.map(
        lambda c: i18n.risk_name(c.replace("_index", "").capitalize(), lang))
    heat = px.density_heatmap(chart_df, x="district", y="risk", z="index", histfunc="avg",
                              color_continuous_scale=RISK_SCALE, range_color=(0, 100), height=280)
    heat.update_layout(margin=dict(l=0, r=0, t=10, b=0), xaxis_title=None, yaxis_title=None,
                       coloraxis_colorbar_title=tr("col_index"))
    st.plotly_chart(heat, width="stretch")

# ---------------------------------------------------------------- method tab
with tab_method:
    st.subheader(tr("method_title"))
    st.markdown(tr("method_body", penalty=risk.DRY_FORECAST_PENALTY))
    st.subheader(tr("sources_title"))
    st.markdown("""
- **NISR**: Seasonal Agricultural Survey: [statistics.gov.rw](https://www.statistics.gov.rw)
- **Open-Meteo**: weather forecast and history API (CC BY 4.0)
- **geoBoundaries**: Rwanda district boundaries, ADM2 (CC BY 4.0)
- **FAO Irrigation & Drainage Paper 56**: crop coefficients (Kc)
""")
    st.markdown(tr("crop_params"))
    st.dataframe(crops, hide_index=True, width="stretch")
