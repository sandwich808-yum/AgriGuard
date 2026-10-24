"""Interface and alert text in English, French and Kinyarwanda.

Data and risk logic always use the English codes ("High", "Drought", "Maize");
only what is shown to people goes through these tables."""

LANGUAGES = {"en": "English", "fr": "Français", "rw": "Kinyarwanda"}

TEXT = {
    # ---------------------------------------------------------------- sidebar
    "tagline": {
        "en": "Climate risk alerts for Rwandan farmers",
        "fr": "Alertes climatiques pour les agriculteurs rwandais",
        "rw": "Imiburo y'ibyago by'ikirere ku bahinzi bo mu Rwanda",
    },
    "layer_label": {"en": "Risk layer", "fr": "Couche de risque", "rw": "Ubwoko bw'ibyago"},
    "layer_help": {
        "en": "Which risk to colour the map by.",
        "fr": "Le risque affiché en couleur sur la carte.",
        "rw": "Ibyago bigaragazwa n'amabara ku ikarita.",
    },
    "provinces": {"en": "Provinces", "fr": "Provinces", "rw": "Intara"},
    "all_provinces": {"en": "All provinces", "fr": "Toutes les provinces", "rw": "Intara zose"},
    "district": {"en": "District", "fr": "District", "rw": "Akarere"},
    "season_A": {
        "en": "Season A (Sep-Jan): planting and growing on the short rains",
        "fr": "Saison A (sept.-janv.) : semis et croissance pendant les petites pluies",
        "rw": "Igihembwe A (Nzeri-Mutarama): gutera no gukura kw'imyaka mu mvura y'umuhindo",
    },
    "season_B": {
        "en": "Season B (Feb-Jun): long rains; Season A harvest in storage",
        "fr": "Saison B (févr.-juin) : grandes pluies ; récolte de la saison A en stock",
        "rw": "Igihembwe B (Gashyantare-Kamena): imvura y'itumba; umusaruro w'igihembwe A uri mu bubiko",
    },
    "season_C": {
        "en": "Season C (Jul-Aug): dry season, irrigated marshland and valley crops",
        "fr": "Saison C (juil.-août) : saison sèche, cultures irriguées de marais et de vallées",
        "rw": "Igihembwe C (Nyakanga-Kanama): impeshyi, guhinga mu bishanga no kuhira",
    },
    "weather_caption": {
        "en": "Weather: Open-Meteo, {source}, observed to {as_of}, forecast to {fc_end}.",
        "fr": "Météo : Open-Meteo, {source}, observée jusqu'au {as_of}, prévisions jusqu'au {fc_end}.",
        "rw": "Ikirere: Open-Meteo, {source}, amakuru kugeza {as_of}, iteganyagihe kugeza {fc_end}.",
    },
    "source_live": {"en": "live", "fr": "en direct", "rw": "ako kanya"},
    "source_snapshot": {"en": "offline snapshot", "fr": "copie hors ligne", "rw": "amakuru abitswe"},
    "loading": {
        "en": "Fetching live weather for 30 districts...",
        "fr": "Récupération de la météo en direct pour 30 districts...",
        "rw": "Turimo kuzana amakuru y'ikirere y'uturere 30...",
    },
    # ---------------------------------------------------------------- header
    "intro": {
        "en": "Early warnings for **drought**, **heavy rain** and **post-harvest storage** risk "
              "in every district, from live weather and national crop statistics.",
        "fr": "Alertes précoces de **sécheresse**, de **fortes pluies** et de risques pour le "
              "**stockage après récolte** dans chaque district, à partir de la météo en direct "
              "et des statistiques agricoles nationales.",
        "rw": "Imiburo y'ibanze ku **mapfa**, **imvura nyinshi** n'**ibyago byo kubika umusaruro** "
              "muri buri karere, hashingiwe ku makuru y'ikirere y'ako kanya n'ibarurishamibare "
              "ry'ubuhinzi ry'igihugu.",
    },
    "api_down": {
        "en": "The live weather API is unreachable, so this shows the saved snapshot.",
        "fr": "L'API météo est injoignable : la dernière copie enregistrée est affichée.",
        "rw": "Amakuru y'ikirere y'ako kanya ntaboneka; turerekana amakuru aheruka kubikwa.",
    },
    "sample_notice": {
        "en": "District crop mix uses sample shares. Replace data/district_crops.csv with the "
              "NISR Seasonal Agricultural Survey figures to make alerts official.",
        "fr": "La répartition des cultures par district utilise des valeurs d'exemple. Remplacez "
              "data/district_crops.csv par les chiffres de l'Enquête agricole saisonnière du NISR.",
        "rw": "Ibihingwa bya buri karere ni ingero gusa. Simbuza data/district_crops.csv imibare "
              "y'Ubushakashatsi bw'Ihinga bw'Ibihembwe bwa NISR kugira ngo imiburo yemerwe.",
    },
    "kpi_high": {"en": "Districts at high risk", "fr": "Districts à risque élevé",
                 "rw": "Uturere dufite ibyago biri hejuru"},
    "kpi_moderate": {"en": "Districts at moderate risk", "fr": "Districts à risque modéré",
                     "rw": "Uturere dufite ibyago biri hagati"},
    "kpi_alerts": {"en": "Active alerts", "fr": "Alertes actives", "rw": "Imiburo iriho"},
    "kpi_rain": {"en": "Avg rain, last 30 days", "fr": "Pluie moyenne, 30 derniers jours",
                 "rw": "Impuzandengo y'imvura, iminsi 30"},
    "tab_map": {"en": "🗺️ Risk map", "fr": "🗺️ Carte des risques", "rw": "🗺️ Ikarita y'ibyago"},
    "tab_alerts": {"en": "🚨 All alerts", "fr": "🚨 Toutes les alertes", "rw": "🚨 Imiburo yose"},
    "tab_method": {"en": "📘 Method & data", "fr": "📘 Méthode et données", "rw": "📘 Uburyo n'amakuru"},
    # ---------------------------------------------------------------- map
    "desc_Overall": {"en": "Highest of the three risks", "fr": "Le plus élevé des trois risques",
                     "rw": "Ibyago biri hejuru kurusha ibindi muri bitatu"},
    "desc_Drought": {"en": "Rainfall vs crop water demand, last 30 days",
                     "fr": "Pluie face aux besoins en eau des cultures, 30 derniers jours",
                     "rw": "Imvura ugereranyije n'amazi ibihingwa bikeneye, iminsi 30 ishize"},
    "desc_Flood": {"en": "Heavy rain forecast for the coming week",
                   "fr": "Fortes pluies prévues pour la semaine à venir",
                   "rw": "Imvura nyinshi iteganyijwe mu cyumweru kiri imbere"},
    "desc_Storage": {"en": "Mould risk for stored grain from forecast humidity",
                     "fr": "Risque de moisissure des grains stockés selon l'humidité prévue",
                     "rw": "Ibyago by'uruhumbu ku myaka ibitswe bitewe n'ubuhehere buteganyijwe"},
    "map_title": {"en": "{layer} risk by district", "fr": "{layer} : risque par district",
                  "rw": "{layer}: ibyago kuri buri karere"},
    "map_click": {"en": "Click a district for details.", "fr": "Cliquez sur un district pour les détails.",
                  "rw": "Kanda ku karere urebe ibisobanuro."},
    "risk_index": {"en": "Risk index", "fr": "Indice de risque", "rw": "Igipimo cy'ibyago"},
    "hover_overall": {"en": "Overall", "fr": "Global", "rw": "Muri rusange"},
    "hover_rain30": {"en": "Rain last 30 days", "fr": "Pluie sur 30 jours", "rw": "Imvura y'iminsi 30"},
    "hover_fc": {"en": "Forecast this week", "fr": "Prévision cette semaine",
                 "rw": "Iteganyagihe ry'iki cyumweru"},
    "colorbar": {"en": "Risk", "fr": "Risque", "rw": "Ibyago"},
    "top_alerts": {"en": "Top alerts", "fr": "Alertes principales", "rw": "Imiburo y'ingenzi"},
    "no_alerts_selection": {
        "en": "No moderate or high alerts for this selection.",
        "fr": "Aucune alerte modérée ou élevée pour cette sélection.",
        "rw": "Nta muburo uri hagati cyangwa hejuru kuri aya mahitamo.",
    },
    # ---------------------------------------------------------------- district detail
    "district_heading": {"en": "{name} district, {province}", "fr": "District de {name}, {province}",
                         "rw": "Akarere ka {name}, {province}"},
    "rain_title": {
        "en": "**Daily rainfall**: observed (dark blue) and 6-day forecast (light blue)",
        "fr": "**Pluie quotidienne** : observée (bleu foncé) et prévision sur 6 jours (bleu clair)",
        "rw": "**Imvura ya buri munsi**: yaguye (ubururu bwijimye) n'iteganyagihe ry'iminsi 6 "
              "(ubururu bweruye)",
    },
    "rain_legend": {"en": "Rainfall (mm)", "fr": "Pluie (mm)", "rw": "Imvura (mm)"},
    "demand_legend": {"en": "Crop water demand (ET₀, mm)", "fr": "Besoin en eau des cultures (ET₀, mm)",
                      "rw": "Amazi ibihingwa bikeneye (ET₀, mm)"},
    "today": {"en": "today", "fr": "aujourd'hui", "rw": "uyu munsi"},
    "mm_day": {"en": "mm/day", "fr": "mm/jour", "rw": "mm/umunsi"},
    "crops_here": {"en": "**Crops in this district**", "fr": "**Cultures de ce district**",
                   "rw": "**Ibihingwa byo muri aka karere**"},
    "col_crop": {"en": "Crop", "fr": "Culture", "rw": "Igihingwa"},
    "col_area": {"en": "Area", "fr": "Surface", "rw": "Ubuso"},
    "col_water": {"en": "Water need met", "fr": "Besoin en eau couvert", "rw": "Amazi akenewe yabonetse"},
    "crop_caption": {
        "en": "Last 30 days: {rain} mm rain vs {et0} mm reference evapotranspiration. "
              "Forecast: {fc} mm, humidity {rh}%.",
        "fr": "30 derniers jours : {rain} mm de pluie pour {et0} mm d'évapotranspiration de "
              "référence. Prévision : {fc} mm, humidité {rh} %.",
        "rw": "Iminsi 30 ishize: imvura ya {rain} mm ugereranyije na {et0} mm y'amazi atakara "
              "(ET₀). Iteganyagihe: {fc} mm, ubuhehere {rh}%.",
    },
    "no_alerts_district": {
        "en": "No alerts for {name} this week. Conditions are within normal range.",
        "fr": "Aucune alerte pour {name} cette semaine. Les conditions sont normales.",
        "rw": "Nta muburo kuri {name} muri iki cyumweru. Ibihe biri mu rugero rusanzwe.",
    },
    "actions_heading": {
        "en": "**Recommended actions and SMS alert preview**",
        "fr": "**Actions recommandées et aperçu de l'alerte SMS**",
        "rw": "**Ibyo gukora n'ubutumwa bugufi (SMS) bw'umuburo**",
    },
    # ---------------------------------------------------------------- alerts tab
    "all_alerts": {"en": "All active alerts", "fr": "Toutes les alertes actives",
                   "rw": "Imiburo yose iriho"},
    "risk_type": {"en": "Risk type", "fr": "Type de risque", "rw": "Ubwoko bw'ibyago"},
    "level": {"en": "Level", "fr": "Niveau", "rw": "Urwego"},
    "col_risk": {"en": "Risk", "fr": "Risque", "rw": "Ibyago"},
    "col_index": {"en": "Index", "fr": "Indice", "rw": "Igipimo"},
    "col_why": {"en": "Why", "fr": "Pourquoi", "rw": "Impamvu"},
    "col_action": {"en": "Recommended action", "fr": "Action recommandée", "rw": "Icyo gukora"},
    "download": {"en": "⬇️ Download alerts (CSV)", "fr": "⬇️ Télécharger les alertes (CSV)",
                 "rw": "⬇️ Kuramo imiburo (CSV)"},
    "overview": {"en": "Risk overview", "fr": "Vue d'ensemble des risques", "rw": "Incamake y'ibyago"},
    # ---------------------------------------------------------------- method tab
    "method_title": {"en": "How AgriGuard works", "fr": "Comment fonctionne AgriGuard",
                     "rw": "Uko AgriGuard ikora"},
    "method_body": {
        "en": """
1. **Weather**: every 3 hours the app pulls the last 30 days and a 6-day forecast of rainfall,
   temperature, humidity and FAO-56 reference evapotranspiration (ET₀) from
   [Open-Meteo](https://open-meteo.com) for the centre of each of Rwanda's 30 districts.
2. **Crop mix**: each district's cultivated area by crop comes from `data/district_crops.csv`
   (NISR Seasonal Agricultural Survey format).
3. **Drought risk**: for each crop, crop water demand = ET₀ × FAO crop coefficient (Kc).
   We compare it with effective rainfall (80% of rain). Below 75% of demand met is Moderate,
   below 50% is High. Drought-tolerant crops (cassava, sorghum, sweet potato) are scaled down,
   and a dry forecast adds {penalty} points. District drought risk is the area-weighted average.
4. **Flood risk**: High when the forecast has 40 mm in one day or 80 mm in the week.
5. **Storage risk**: for districts that store grain or pulses, forecast mean humidity above
   80% is Moderate and above 85% is High, increased in warm (22°C or more) lowland districts.
6. **Alerts**: every Moderate or High risk becomes a plain-language alert with a recommended
   action and a short SMS-style message for farmers and extension officers.
""",
        "fr": """
1. **Météo** : toutes les 3 heures, l'application récupère les 30 derniers jours et une
   prévision sur 6 jours (pluie, température, humidité et évapotranspiration de référence
   FAO-56, ET₀) depuis [Open-Meteo](https://open-meteo.com) pour le centre de chacun des
   30 districts du Rwanda.
2. **Cultures** : la surface cultivée par culture et par district provient de
   `data/district_crops.csv` (format de l'Enquête agricole saisonnière du NISR).
3. **Sécheresse** : pour chaque culture, besoin en eau = ET₀ × coefficient cultural FAO (Kc),
   comparé à la pluie efficace (80 % de la pluie). Moins de 75 % du besoin couvert : Modéré ;
   moins de 50 % : Élevé. Les cultures tolérantes (manioc, sorgho, patate douce) sont pondérées
   à la baisse, et une prévision sèche ajoute {penalty} points. Le risque du district est la
   moyenne pondérée par la surface.
4. **Inondation** : Élevé si la prévision atteint 40 mm en un jour ou 80 mm sur la semaine.
5. **Stockage** : pour les districts qui stockent grains ou légumineuses, une humidité moyenne
   prévue au-dessus de 80 % est Modérée et au-dessus de 85 % Élevée, accrue dans les districts
   chauds de basse altitude (22 °C ou plus).
6. **Alertes** : chaque risque Modéré ou Élevé devient une alerte claire avec une action
   recommandée et un court message de type SMS pour les agriculteurs et les vulgarisateurs.
""",
        "rw": """
1. **Ikirere**: buri masaha 3, porogaramu ifata amakuru y'iminsi 30 ishize n'iteganyagihe
   ry'iminsi 6 (imvura, ubushyuhe, ubuhehere n'amazi atakara ET₀ ya FAO-56) kuri
   [Open-Meteo](https://open-meteo.com), ku gice cyo hagati cya buri karere mu turere 30 tw'u Rwanda.
2. **Ibihingwa**: ubuso buhingwaho buri gihingwa muri buri karere buva muri
   `data/district_crops.csv` (imiterere y'Ubushakashatsi bw'Ihinga bw'Ibihembwe bwa NISR).
3. **Amapfa**: kuri buri gihingwa, amazi gikeneye = ET₀ × igipimo cy'igihingwa cya FAO (Kc),
   bigereranywa n'imvura ifite akamaro (80% by'imvura). Iyo amazi abonetse ari munsi ya 75%
   y'akenewe ni Hagati; munsi ya 50% ni Hejuru. Ibihingwa bihanganira amapfa (imyumbati,
   amasaka, ibijumba) bigabanyirizwa, kandi iteganyagihe ry'izuba ryongeraho amanota {penalty}.
   Ibyago by'akarere ni impuzandengo ishingiye ku buso.
4. **Imyuzure**: Hejuru iyo hateganyijwe mm 40 ku munsi umwe cyangwa mm 80 mu cyumweru.
5. **Ububiko**: ku turere tubika imyaka y'ibinyampeke cyangwa ibinyamisogwe, ubuhehere
   buteganyijwe burenga 80% ni Hagati, burenga 85% ni Hejuru, bikiyongera mu turere dushyuha
   (22°C cyangwa birenga).
6. **Imiburo**: buri byago biri Hagati cyangwa Hejuru bihinduka umuburo usobanutse, urimo
   icyo gukora n'ubutumwa bugufi bwoherezwa abahinzi n'abajyanama b'ubuhinzi.
""",
    },
    "sources_title": {"en": "Data sources", "fr": "Sources des données", "rw": "Aho amakuru aturuka"},
    "crop_params": {"en": "**Crop parameters used**", "fr": "**Paramètres des cultures utilisés**",
                    "rw": "**Ibipimo by'ibihingwa byakoreshejwe**"},
    "footer": {
        "en": "AgriGuard Rwanda · Data: NISR, Open-Meteo, geoBoundaries, FAO · Built for the "
              "Agricultural Productivity hackathon track",
        "fr": "AgriGuard Rwanda · Données : NISR, Open-Meteo, geoBoundaries, FAO · Réalisé pour le "
              "volet Productivité agricole du hackathon",
        "rw": "AgriGuard Rwanda · Amakuru: NISR, Open-Meteo, geoBoundaries, FAO · Yakorewe "
              "irushanwa (hackathon) mu cyiciro cy'Umusaruro w'Ubuhinzi",
    },
    # ---------------------------------------------------------------- alert text
    "detail_Drought": {
        "en": "{rain} mm rain in 30 days vs crop need; {fc} mm forecast this week. Crops at risk: {crops}.",
        "fr": "{rain} mm de pluie en 30 jours face aux besoins des cultures ; {fc} mm prévus cette "
              "semaine. Cultures à risque : {crops}.",
        "rw": "Imvura ya {rain} mm mu minsi 30 ugereranyije n'ibyo ibihingwa bikeneye; hateganyijwe "
              "{fc} mm muri iki cyumweru. Ibihingwa biri mu byago: {crops}.",
    },
    "detail_Flood": {
        "en": "Up to {max} mm/day and {fc} mm total forecast this week.",
        "fr": "Jusqu'à {max} mm/jour et {fc} mm au total prévus cette semaine.",
        "rw": "Hateganyijwe imvura igera kuri {max} mm ku munsi na {fc} mm yose hamwe muri iki cyumweru.",
    },
    "detail_Storage": {
        "en": "Forecast humidity {rh}% at {temp}°C: high mould risk for stored maize, beans and other grain.",
        "fr": "Humidité prévue {rh} % à {temp} °C : risque élevé de moisissure pour le maïs, les "
              "haricots et autres grains stockés.",
        "rw": "Ubuhehere buteganyijwe ni {rh}% ku bushyuhe bwa {temp}°C: ibyago byinshi by'uruhumbu "
              "ku bigori, ibishyimbo n'indi myaka ibitswe.",
    },
    "main_crops": {"en": "main crops", "fr": "principales cultures", "rw": "ibihingwa by'ingenzi"},
    "sms": {
        "en": "AgriGuard {level} {risk} ALERT - {district}: {detail} Action: {action}.",
        "fr": "AgriGuard ALERTE {risk} {level} - {district} : {detail} Action : {action}.",
        "rw": "AgriGuard UMUBURO W'{risk} ({level}) - {district}: {detail} Icyo gukora: {action}.",
    },
}

LEVELS = {
    "High": {"en": "High", "fr": "Élevé", "rw": "Hejuru"},
    "Moderate": {"en": "Moderate", "fr": "Modéré", "rw": "Hagati"},
    "Low": {"en": "Low", "fr": "Faible", "rw": "Hasi"},
}

RISKS = {
    "Overall": {"en": "Overall", "fr": "Global", "rw": "Rusange"},
    "Drought": {"en": "Drought", "fr": "Sécheresse", "rw": "Amapfa"},
    "Flood": {"en": "Flood", "fr": "Inondation", "rw": "Imyuzure"},
    "Storage": {"en": "Storage", "fr": "Stockage", "rw": "Ububiko"},
}

PROVINCE_NAMES = {
    "Kigali City": {"en": "Kigali City", "fr": "Ville de Kigali", "rw": "Umujyi wa Kigali"},
    "Northern": {"en": "Northern Province", "fr": "Province du Nord", "rw": "Intara y'Amajyaruguru"},
    "Southern": {"en": "Southern Province", "fr": "Province du Sud", "rw": "Intara y'Amajyepfo"},
    "Eastern": {"en": "Eastern Province", "fr": "Province de l'Est", "rw": "Intara y'Iburasirazuba"},
    "Western": {"en": "Western Province", "fr": "Province de l'Ouest", "rw": "Intara y'Iburengerazuba"},
}

CROPS = {
    "Maize": {"en": "Maize", "fr": "Maïs", "rw": "Ibigori"},
    "Beans": {"en": "Beans", "fr": "Haricots", "rw": "Ibishyimbo"},
    "Irish potato": {"en": "Irish potato", "fr": "Pomme de terre", "rw": "Ibirayi"},
    "Cassava": {"en": "Cassava", "fr": "Manioc", "rw": "Imyumbati"},
    "Sorghum": {"en": "Sorghum", "fr": "Sorgho", "rw": "Amasaka"},
    "Rice": {"en": "Rice", "fr": "Riz", "rw": "Umuceri"},
    "Banana": {"en": "Banana", "fr": "Banane", "rw": "Urutoki"},
    "Sweet potato": {"en": "Sweet potato", "fr": "Patate douce", "rw": "Ibijumba"},
    "Wheat": {"en": "Wheat", "fr": "Blé", "rw": "Ingano"},
    "Soybean": {"en": "Soybean", "fr": "Soja", "rw": "Soya"},
}

ACTIONS = {
    "Drought": {
        "High": {
            "en": "Irrigate now if water is available; mulch to keep soil moisture; delay planting "
                  "of water-hungry crops; prioritise drought-tolerant varieties.",
            "fr": "Irriguez maintenant si l'eau est disponible ; paillez pour garder l'humidité du "
                  "sol ; reportez le semis des cultures exigeantes en eau ; privilégiez les variétés "
                  "tolérantes à la sécheresse.",
            "rw": "Uhire nonaha niba hari amazi; sasira imirima kugira ngo ubutaka bugumane "
                  "ubuhehere; igiza inyuma gutera ibihingwa bikenera amazi menshi; hitamo imbuto "
                  "zihanganira amapfa.",
        },
        "Moderate": {
            "en": "Monitor soil moisture; plan small-scale irrigation; mulch exposed fields.",
            "fr": "Surveillez l'humidité du sol ; préparez une petite irrigation ; paillez les champs exposés.",
            "rw": "Kurikirana ubuhehere bw'ubutaka; tegura kuhira ku buso buto; sasira imirima "
                  "itwikiriye nabi.",
        },
    },
    "Flood": {
        "High": {
            "en": "Clear drainage channels and terraces; harvest mature crops early; move stored "
                  "produce and inputs off the ground.",
            "fr": "Curez les canaux de drainage et les terrasses ; récoltez tôt les cultures mûres ; "
                  "surélevez les produits stockés et les intrants.",
            "rw": "Sibura imiyoboro y'amazi n'amaterasi; sarura hakiri kare imyaka yeze; zamura "
                  "umusaruro n'inyongeramusaruro bibitswe ubikure hasi.",
        },
        "Moderate": {
            "en": "Check drainage on terraces and marshland plots; avoid fertiliser before heavy rain.",
            "fr": "Vérifiez le drainage des terrasses et des parcelles de marais ; évitez d'épandre "
                  "de l'engrais avant de fortes pluies.",
            "rw": "Genzura imiyoboro y'amazi ku materasi no mu bishanga; irinde gushyira ifumbire "
                  "mbere y'imvura nyinshi.",
        },
    },
    "Storage": {
        "High": {
            "en": "Dry grain fully before storing; use hermetic (PICS) bags; store off the floor "
                  "in ventilated stores; inspect for mould weekly.",
            "fr": "Séchez complètement les grains avant le stockage ; utilisez des sacs hermétiques "
                  "(PICS) ; stockez hors du sol dans un local aéré ; inspectez chaque semaine.",
            "rw": "Umisha neza imyaka mbere yo kuyibika; koresha imifuka ifunga neza (PICS); bika "
                  "hejuru y'ubutaka mu bubiko bwinjiramo umwuka; genzura uruhumbu buri cyumweru.",
        },
        "Moderate": {
            "en": "Check grain moisture before storage; keep stores ventilated.",
            "fr": "Vérifiez l'humidité des grains avant le stockage ; gardez les magasins aérés.",
            "rw": "Genzura ubuhehere bw'imyaka mbere yo kuyibika; ubuhunikiro bujye bwinjiramo umwuka.",
        },
    },
}


def t(key: str, lang: str = "en", **kwargs) -> str:
    """Translated text for `key`, falling back to English."""
    entry = TEXT[key]
    text = entry.get(lang) or entry["en"]
    return text.format(**kwargs) if kwargs else text


def _name(table: dict, code: str, lang: str) -> str:
    entry = table.get(code)
    return (entry.get(lang) or entry["en"]) if entry else code


def level_name(code: str, lang: str) -> str:
    return _name(LEVELS, code, lang)


def risk_name(code: str, lang: str) -> str:
    return _name(RISKS, code, lang)


def province_name(code: str, lang: str) -> str:
    return _name(PROVINCE_NAMES, code, lang)


def crop_name(code: str, lang: str) -> str:
    return _name(CROPS, code, lang)


def action(risk: str, level: str, lang: str) -> str:
    entry = ACTIONS[risk][level]
    return entry.get(lang) or entry["en"]
