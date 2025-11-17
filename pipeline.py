from io_utils import lire_tous_les_cvs
from scoring import score_cv_frequence
from dataframe_utils import (
    construire_df_scores,
    mapper_cv_originaux,
    ajouter_gains,
    trier_groupes
)
from display import afficher_groupes_console, afficher_groupes_streamlit

def pipeline_complet(folder, original_files, offre, max_occ):
    """
    Entrees :
        original_files (liste de string) : liste des noms des fichiers CV originaux, utile pour récuperer leur préfixe
        offre (string) : texte de l'offre de poste
        folder (string) : chemin du dossier contenant les CV à scorer
        max_occ (int) : nombre maximum d'occurrences par mot-clé à prendre en compte dans le scoring
    
    Sorties :
        keyword_details (dict str[int]) : Npmbre d'occurrences de chaque mot-clé dans le CV
    """
    cvs = lire_tous_les_cvs(folder)

    # --- 1. INITIALISATION ---
    scores = {}             # Pour stocker les scores (float) qui alimenteront le DataFrame
    keyword_details = {}    # Variable de sortie pour les occurrences détaillées
    
    # --- 2. SCORING et Collecte des détails ---
    print("\n--- Démarrage du Scoring et de la collecte des détails ---")

    for fname, text in cvs.items():
        # score_cv_frequence retourne (score_final, details_des_occurrences)
        final_score, details_dict = score_cv_frequence(text, offre, max_occ) 
        
        # Stockage des deux résultats
        scores[fname] = final_score
        keyword_details[fname] = details_dict
        
    # --- 3. Pipeline DataFrame ---
    # Les fonctions suivantes (construire_df_scores, mapper_cv_originaux, etc.) 
    # sont supposées être définies ailleurs et fonctionner avec le dictionnaire 'scores'.
    df = construire_df_scores(scores)
    df = mapper_cv_originaux(df, original_files)
    df = ajouter_gains(df, original_files)
    df = trier_groupes(df, original_files)
    
    # --- 4. RETOUR DOUBLE ---
    # Retourne le DataFrame (pour l'affichage des scores) et le dictionnaire de détails
    return df, keyword_details