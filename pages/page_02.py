import streamlit as st

st.set_page_config(
    page_title="Check this out",  # Titre affiché dans l'onglet du navigateur
    page_icon="🌈",  # Icône de l'onglet
)

import json
import streamlit as st
from streamlit_lottie import st_lottie

# Charger l'animation depuis un fichier local
def load_lottie_file(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

# 🔹 Remplace "stuff/anim.json" par le chemin réel de ton fichier
lottie_animation = load_lottie_file("stuff/anim.json")

# Afficher l'animation
st_lottie(lottie_animation, height=300, key="custom")
