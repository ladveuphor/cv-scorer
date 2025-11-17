import streamlit as st
import pandas as pd
import os

from pipeline import pipeline_complet
from scoring import score_cv_frequence
from display import display_global_ranking, afficher_groupes_streamlit
from display import afficher_keyword_details_streamlit

# ---------------------------------------------------------
# Configuration Streamlit
# ---------------------------------------------------------
st.set_page_config(page_title="CV Scorer", layout="wide")
st.title("📋 CV Scorer — Compare CVs vs Offre")

# ---------------------------------------------------------
# Sidebar : uniquement le dossier et options fréquence
# ---------------------------------------------------------
with st.sidebar:
    st.header("Paramètres")

    folder = st.text_input(
        "Dossier contenant les CV (.docx)",
        value="./CVs",
        help="Indique un chemin local contenant uniquement des fichiers .docx"
    )

    st.markdown("---")
    st.write("Options de scoring (présence + fréquence)")
    max_occ = st.slider("Max occurrences par mot-clé", 1, 20, 8)

# ---------------------------------------------------------
# Zone de texte de l'offre
# ---------------------------------------------------------
st.header("Offre de poste")
offre_par_defaut = """
Dans le cadre de sa mission d’exploitation et de valorisation des données médicales, la DIDM fait face à un besoin croissant de données fiables. C’est pourquoi un nouveau poste est créé.
Vous viendrez compléter une équipe composée d’une Chargée d’études et développements à 50 % et d’un Responsable Etudes et Développements. Sous la responsabilité de ce dernier, vos missions seront les suivantes :
Construire des pipelines de données pour alimenter la BI et l’analytique.
Modéliser et structurer les flux, tables et schémas
Garantir la qualité, la fiabilité et la sécurité des données
Développer de nouveaux datasets pour la BI de la DIDM
Mettre en place des standards de développement et de bonnes pratiques
Assurer le support et la résolution des incidents sur votre périmètre...

Votre boîte à outils
Excellente maîtrise de SQL (Oracle) et solide expérience en R
Connaissances en Julia, Java ou Scala appréciées
Pratique des outils de versioning (Git, Bitbucket, Github)
Expérience avec un outil ETL, idéalement Talend
Une première approche de la dataviz (Tableau, QlikView) est un atout
"""
offre_text = st.text_area(
    "Collez l'offre de poste ici",
    value=offre_par_defaut,
    height=220
)

# ---------------------------------------------------------
# Lancement du scoring
# ---------------------------------------------------------
if st.button("▶ Lancer le scoring des CV"):
    if not offre_text.strip():
        st.error("Merci d’indiquer une offre avant de lancer le scoring.")
    elif not os.path.isdir(folder):
        st.error("Le dossier indiqué n’existe pas ou est invalide.")
    else:
        st.info("Scoring en cours… Veuillez patienter.")

        # --- LOGIQUE CLÉ : Récupération des fichiers .docx ---
        original_files = []
        try:
            # Liste tous les fichiers et filtre uniquement les .docx
            all_entries = os.listdir(folder)
            original_files = [f for f in all_entries if f.lower().endswith(".docx")]
            
            if not original_files:
                st.warning(f"Aucun fichier .docx trouvé dans le dossier : `{folder}`.")
                st.stop()
                
            st.write(f"Fichiers trouvés ({len(original_files)}) : {', '.join(original_files[:3])}...")
            
        except Exception as e:
            st.error(f"Erreur lors de la lecture du contenu du dossier : {e}")
            st.stop()
        # ---------------------------------------------------------
        # Appel du pipeline simplifié
        try:
            df, keyword_details = pipeline_complet(
                        folder=folder,
                        original_files=original_files,  # PASSAGE DE LA LISTE DES CV DÉTECTÉS
                        offre=offre_text,
                        max_occ=max_occ
            )
    
            st.success("Terminé !")

            # 1. AFFICHAGE DU CLASSEMENT GLOBAL (NOUVEAU)
            display_global_ranking(df)

            # 2. AFFICHAGE DES RÉSULTATS DÉTAILLÉS (ANCIEN)
            afficher_groupes_streamlit(df)

            # 3. AFFICHAGE COMPACT DES DÉTAILS PAR MOT-CLÉ (occurrences)
            # Utilise les détails renvoyés par pipeline_complet : keyword_details
            # Fonction ajoutée dans display.py : afficher_keyword_details_streamlit
            try:
                afficher_keyword_details_streamlit(keyword_details, df, top_n=10, min_count=0)
            except Exception as _e:
                # Ne pas planter l'UI si affichage détaillé échoue
                st.warning("Impossible d'afficher les détails par mot-clé : " + str(_e))
            
        except Exception as e:
             st.error(f"Erreur d'exécution du pipeline : {e}")
             st.exception(e)