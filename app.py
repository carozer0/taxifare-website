import streamlit as st
import datetime
import requests
import pandas as pd
import numpy as np
from PIL import Image
import os


st.set_page_config(
    page_title="Allo Taxi Rougerie.com", # => Quick reference - Streamlit
    page_icon="🚕",
    layout="centered", # wide
    initial_sidebar_state="auto") # collapsed

'''
# 🚕🚕 Allo Taxi Rougerie.com 🚕🚕
'''

st.markdown('''
Prenez le vélo c'est mieux! Faites du stop sinon c'est super!
''')


col3, col4 = st.columns(2)

with col3:
    d = st.date_input(
    "When do you plan to book your next ride in NY?",
    datetime.date.today())

with col4:
    t= st.time_input('What time shall I stop by?', datetime.datetime.now().time())#datetime.time(8, 45))



st.markdown('''
Passion navigation, sors tes coordonnées
''')

default_pickup_latitude = 40.7580   # Times Square
default_pickup_longitude = -73.9855
default_dropoff_latitude = 40.7128  # Lower Manhattan
default_dropoff_longitude = -74.0060

col1, col2 = st.columns(2)

with col1:
    st.subheader("🚕 Pickup")
    pickup_latitude = st.number_input('Pickup latitude', value=default_pickup_latitude)
    pickup_longitude = st.number_input('Pickup longitude', value=default_pickup_longitude)

with col2:
    st.subheader("🏁 Dropoff")
    dropoff_latitude = st.number_input('Dropoff latitude', value=default_dropoff_latitude)
    dropoff_longitude = st.number_input('Dropoff longitude', value=default_dropoff_longitude)


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
    import streamlit as st




    df = pd.DataFrame([
    {"lat": pickup_latitude, "lon": pickup_longitude},  # Pickup point
    {"lat": dropoff_latitude, "lon": dropoff_longitude}  # Dropoff point
    ])

    st.title("📍 Let's check the map")
    st.map(df)


CSS = """
<style>
h1 {
    color: #FFD700 !important; /* Jaune taxi */
}
</style>
"""

# Injection du CSS
st.markdown(CSS, unsafe_allow_html=True)

#st.image("stuff/ragondins.jpeg", width=100)
 #  [Check this out!](https://www.ragondins.fr/)
# Ajout de CSS pour personnaliser le lien
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] a {
        color: yellow !important;
        text-decoration: none !important;
        font-weight: bold;
    }

    [data-testid="stSidebar"] a:hover {
        color: gold !important;
        text-decoration: underline !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("[Have you arranged your trip to Porto? Stephanie can't wait to meet you! ](https://www.kayak.fr/flights/BOD-OPO/2025-04-13/2025-04-20?ucs=1owfcp8&sort=bestflight_a)", unsafe_allow_html=True)


st.title("🚖 Spot the taxi and win big, upload your photo here!")





# Créer un dossier de stockage si inexistant
SAVE_DIR = "uploaded_images"
os.makedirs(SAVE_DIR, exist_ok=True)

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Ouvrir l'image avec PIL
    img = Image.open(uploaded_file)

    # Afficher l'image uploadée
    st.image(img, caption="Uploaded Image", width=300)

    # Définir le chemin de sauvegarde
    file_path = os.path.join(SAVE_DIR, uploaded_file.name)

    # Sauvegarder l’image
    img.save(file_path)

    # Afficher le message de confirmation
    st.success("You did not win shit but thanks for the pic!")
