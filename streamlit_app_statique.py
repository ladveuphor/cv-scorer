import streamlit as st
import os
import pandas as pd

# --- Import de ton pipeline sans modification ---
from pipeline import pipeline_complet

# -----------------------------
# CONFIGURATION STATIQUE
# -----------------------------

# Liste des CV "originaux" → À ADAPTER à TA vraie arborescence
original_files = [
    "NRJBI_CEC_CV_Senior.docx",
    "NRJBI_ERE_CV - 20250930.docx",
    "NRJBI_CV_EMO_202510_revisionElise.docx",
]

# Dossier contenant tes CV
DEFAULT_CV_FOLDER = "CVs"

# -----------------------------
# INTERFACE STREAMLIT
# -----------------------------

st.set_page_config(page_title="Scoring CVs", layout="wide")

st.title("📄 Scoring automatique des CVs")
st.write("Compare des CVs avec une offre pour identifier les meilleurs candidats.")


# --- Choix du dossier CV ---
st.subheader("1️⃣ Sélection du dossier contenant les CV (.docx)")

folder = st.text_input(
    "Chemin du dossier contenant les CV :",
    value=DEFAULT_CV_FOLDER
)

if not os.path.isdir(folder):
    st.warning("⚠️ Dossier introuvable. Vérifie le chemin.")
else:
    st.success("Dossier OK")


# --- Offre de poste ---
st.subheader("2️⃣ Offre de poste")

offre_text = st.text_area(
    "Colle ici le texte complet de l’offre",
    height=250
)

# --- Bouton de lancement ---
st.subheader("3️⃣ Lancer le scoring")

if st.button("🚀 Lancer l’analyse et le scoring des CV"):
    if not offre_text.strip():
        st.error("❌ Tu dois d'abord saisir une offre.")
    elif not os.path.isdir(folder):
        st.error("❌ Le dossier de CV n'existe pas.")
    else:
        st.info("⏳ Analyse en cours...")

        # ------------------------
        # APPEL DU PIPELINE
        # ------------------------
        try:
            df_result = pipeline_complet(
                folder=folder,
                original_files=original_files,
                offre=offre_text,
                mode="streamlit"
            )

            st.success("🎉 Scoring terminé !")
            
            # Affichage du résultat
            st.subheader("📊 Résultat du scoring")
            st.dataframe(df_result)

        except Exception as e:
            st.error(f"❌ Erreur durant l'exécution : {e}")
