import streamlit as st
import datetime
import requests
import pandas as pd
import numpy as np
from PIL import Image
import os
st.set_page_config(
    page_title="Prettier but not working!",
    page_icon="🚕"
)

st.title("🗺️ Something is off with those adresses")

# 🔹 Initialisation des coordonnées dans `st.session_state`
if "pickup_latitude" not in st.session_state:
    st.session_state["pickup_latitude"] = None
    st.session_state["pickup_longitude"] = None
    st.session_state["dropoff_latitude"] = None
    st.session_state["dropoff_longitude"] = None

# 🔹 Affichage des coordonnées enregistrées
st.subheader("📌 Coordinates")
if all([
    st.session_state["pickup_latitude"],
    st.session_state["pickup_longitude"],
    st.session_state["dropoff_latitude"],
    st.session_state["dropoff_longitude"]
]):
    st.write(f"📍 **Pickup Latitude:** {st.session_state['pickup_latitude']}")
    st.write(f"📍 **Pickup Longitude:** {st.session_state['pickup_longitude']}")
    st.write(f"🏁 **Dropoff Latitude:** {st.session_state['dropoff_latitude']}")
    st.write(f"🏁 **Dropoff Longitude:** {st.session_state['dropoff_longitude']}")
else:
    st.warning("🚨 Adresses!!!")

# 🔹 Chargement de la carte avec bouton "Enregistrer"
mapbox_access_token = "pk.eyJ1IjoiY2Fyb3plcjAiLCJhIjoiY204OGtvZXk4MHJydDJrc2Zvcnh4cHF3YyJ9.EQmgQnfL0WpeBnF6h7RjSw"

map_html = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>NY Taxi Fare Map</title>
    <script src="https://api.mapbox.com/mapbox-gl-js/v2.6.1/mapbox-gl.js"></script>
    <script src="https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-geocoder/v4.7.0/mapbox-gl-geocoder.min.js"></script>
    <link href="https://api.mapbox.com/mapbox-gl-js/v2.6.1/mapbox-gl.css" rel="stylesheet">
    <link rel="stylesheet" href="https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-geocoder/v4.7.0/mapbox-gl-geocoder.css">
    <style>
        body {{ margin: 0; padding: 0; }}
        #map {{ width: 100%; height: 500px; border-radius: 10px; }}
        .geocoder-container {{
            position: absolute;
            top: 10px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 1000;
            background: white;
            padding: 10px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            display: flex;
            flex-direction: column;
            gap: 10px;
            max-width: 400px;
        }}
        .save-button {{
            padding: 10px;
            background-color: #007bff;
            color: white;
            border: none;
            cursor: pointer;
            border-radius: 5px;
            margin-top: 10px;
            width: 100%;
        }}
    </style>
</head>
<body>
    <div id="map"></div>
    <div class="geocoder-container">
        <div id="pickup"></div>
        <div id="dropoff"></div>
        <button class="save-button" onclick="saveLocations()">📍 Enregistrer les coordonnées</button>
    </div>

    <!-- Champ caché pour stocker les coordonnées -->
    <input type="hidden" id="coords_data" value="">

    <script>
        mapboxgl.accessToken = '{mapbox_access_token}';

        const map = new mapboxgl.Map({{
            container: 'map',
            style: 'mapbox://styles/mapbox/streets-v11',
            center: [-74.006, 40.7128],
            zoom: 12
        }});

        map.addControl(new mapboxgl.NavigationControl());

        const pickupGeocoder = new MapboxGeocoder({{
            accessToken: mapboxgl.accessToken,
            placeholder: 'Pickup location',
            mapboxgl: mapboxgl
        }});

        const dropoffGeocoder = new MapboxGeocoder({{
            accessToken: mapboxgl.accessToken,
            placeholder: 'Drop-off location',
            mapboxgl: mapboxgl
        }});

        document.getElementById('pickup').appendChild(pickupGeocoder.onAdd(map));
        document.getElementById('dropoff').appendChild(dropoffGeocoder.onAdd(map));

        let pickupCoords = null;
        let dropoffCoords = null;

        pickupGeocoder.on('result', function(e) {{
            pickupCoords = e.result.geometry.coordinates;
            console.log('📍 Pickup Coordinates:', pickupCoords);
        }});

        dropoffGeocoder.on('result', function(e) {{
            dropoffCoords = e.result.geometry.coordinates;
            console.log('🏁 Dropoff Coordinates:', dropoffCoords);
        }});

        function saveLocations() {{
            if (pickupCoords && dropoffCoords) {{
                const message = {{
                    pickup_latitude: pickupCoords[1],
                    pickup_longitude: pickupCoords[0],
                    dropoff_latitude: dropoffCoords[1],
                    dropoff_longitude: dropoffCoords[0]
                }};

                console.log("🚀 Enregistrement des coordonnées :", message);

                // Vérifier si l'input caché existe
                const inputField = document.getElementById("coords_data");
                if (!inputField) {{
                    console.error("⚠️ Champ caché 'coords_data' introuvable !");
                    return;
                }}

                // Insérer les coordonnées dans le champ caché
                inputField.value = JSON.stringify(message);
                console.log("✅ Données insérées dans coords_data :", inputField.value);

                // Forcer la détection du changement par Streamlit
                inputField.dispatchEvent(new Event('input', {{ bubbles: true }}));

                // Passer les coordonnées à Streamlit
                window.parent.postMessage(message, "*");

                alert("✅ Coordonnées enregistrées ! Elles devraient s'afficher immédiatement.");
            }} else {{
                alert("🚨 Sélectionnez une adresse avant d'enregistrer.");
            }}
        }}
    </script>
</body>
</html>
"""

st.components.v1.html(map_html, height=600)



col3, col4 = st.columns(2)

with col3:
    d = st.date_input(
    "When do you plan to book your next ride in NY?",
    datetime.date.today())

with col4:
    t= st.time_input('What time shall I stop by?', datetime.datetime.now().time())#datetime.time(8, 45))

#st.markdown('''You got a fast car''')
passenger_count= st.number_input('Passenger count (trunk included)',min_value=1, max_value=12, value=1)
## Here we would like to add some controllers in order to ask the user to select the parameters of the ride


if st.button("Should I apply for a 20-year loan? 💸"):
    url = 'https://taxifare.lewagon.ai/predict'
    params = {
        "pickup_datetime": datetime.datetime.combine(d, t).strftime("%Y-%m-%d %H:%M:%S"),
        "pickup_longitude": pickup_longitude,
        "pickup_latitude": pickup_latitude,
        "dropoff_longitude": dropoff_longitude,
        "dropoff_latitude": dropoff_latitude,
        "passenger_count": passenger_count
    }


    response = requests.get(url, params=params)

    if response.status_code == 200:
        fare = response.json().get("fare", "inf")
        st.success(f"No you're fine this time! Expected amount ${fare:.2f}")
    else:
        st.error(f"Erreur {response.status_code}: {response.text}")
