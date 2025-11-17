# display.py
import streamlit as st
import pandas as pd
from typing import Dict, Any


# ---------------------------------------------------------
# Fonctions d'Affichage
# ---------------------------------------------------------
def display_global_ranking(df: pd.DataFrame):
    """
    Affiche un classement initial des CV triés par Score décroissant.
    """
    st.header("🏆 Classement Général des CV")
    
    # Assurez-vous d'avoir les colonnes nécessaires, puis triez
    if 'Score' in df.columns and 'Fichier' in df.columns:
        # Triez par score décroissant
        df_ranking = df.sort_values(by='Score', ascending=False).reset_index(drop=True)
        
        # Colonnes à afficher pour le classement global
        cols_to_display = ['Fichier', 'Score']
        
        # Si la colonne 'gain_vs_original' existe, l'ajouter pour l'info
        if 'gain_vs_original' in df_ranking.columns:
            cols_to_display.append('gain_vs_original')
        
        # Affichage du classement (utilise uniquement les colonnes sélectionnées)
        st.dataframe(
            df_ranking[cols_to_display],
            use_container_width=True,
            hide_index=True,
            column_config={
                "Score": st.column_config.NumberColumn("Score (Max 100)", format="%.2f"),
                "gain_vs_original": st.column_config.NumberColumn("Gain vs Original", format="%+.2f"),
            }
        )
        st.markdown("---") # Séparateur visuel avant l'affichage détaillé
    else:
        st.warning("Le DataFrame de résultats ne contient pas les colonnes 'Fichier' et 'Score' pour le classement.")


def afficher_groupes_console(df_sorted):
    """Affichage console (réutilisable ailleurs).
    Affiche les CV par groupes : l'original + les versions améliorées
    Exemple : Antoine original + Antoine enhanced 1 + Antoine enhanced 2 ... 
    """
    for base, group in df_sorted.groupby("base_name"):
        print(f"\n📄 {base}")
        for _, r in group.iterrows():
            gain = f"(+{r['gain_vs_original']:.2f})" if r['gain_vs_original'] > 0 else f"({r['gain_vs_original']:.2f})"
            print(f"   {r['Fichier']:<80} {r['Score']:6.2f} {gain}")
            
### Sur streamlit
# --- Fonction Utilitaires Nécessaire (Correction de l'Erreur) ---
def custom_format(row: Dict[str, Any]) -> str:
    """Formate la colonne Score et Gain dans une chaîne de caractères lisible."""
    score = f"{row['Score']:6.2f}"
    gain = row.get('gain_vs_original')
    
    # Assurez-vous que la colonne existe et n'est pas NaN
    if gain is not None and pd.notna(gain):
        # Utilise :+ pour forcer l'affichage du signe '+' pour les gains positifs
        gain_str = f"({gain:+.2f})" 
        return f"{score} {gain_str}"
    
    return score
            
def afficher_groupes_streamlit(df_sorted: pd.DataFrame):
    """
    Affiche le DataFrame des résultats groupés par 'base_name' (CV original),
    présentant le Fichier, le Score, et le Gain VS Original.

    Args:
        df_sorted (pd.DataFrame): DataFrame des résultats triés, 
                                  doit contenir les colonnes 'base_name', 
                                  'Fichier', 'Score', et 'gain_vs_original'.
    """
    st.header("🔍 Résultats Détaillés par CV Original")
    st.markdown("---")

    # 1. Groupement des données comme dans la fonction console
    grouped_data = df_sorted.groupby("base_name")

    for base, group in grouped_data:
        # 2. Affichage du groupe (CV Original)
        st.subheader(f"📄 CV Original : **{base}**")
        
        # Prépare les données pour l'affichage en gardant uniquement les colonnes pertinentes
        display_group = group[['Fichier', 'Score', 'gain_vs_original']].copy()
        
        # 3. Création d'une colonne formatée pour le score et le gain
        # Ceci est nécessaire car Streamlit gère mal l'alignement précis dans le Markdown/Tableau simple.
        
        # Note: Si la colonne 'gain_vs_original' n'existe pas, on l'ignore (utile si le dataframe n'a pas été enrichi)
        if 'gain_vs_original' in display_group.columns:
            display_group['Score & Gain'] = display_group.apply(custom_format, axis=1)
            final_display = display_group[['Fichier', 'Score & Gain']]
            # Renomme les colonnes pour une meilleure lisibilité
            final_display.columns = ['Fichier Modifié', 'Score et Différence']
        else:
            final_display = display_group[['Fichier', 'Score']]
            final_display.columns = ['Fichier Modifié', 'Score']
            
        # 4. Affichage du tableau de résultats pour ce groupe
        st.dataframe(
            final_display.reset_index(drop=True), 
            use_container_width=True,
            hide_index=True
        )

        st.markdown("---") # Séparateur visuel entre les groupes
        
        
def afficher_keyword_details_streamlit(keyword_details, df_sorted, top_n: int = 10, min_count: int = 1):
    """
    Affiche, par groupe (base_name), les occurrences par mot-clé pour chaque CV.
    Evite les expanders imbriqués : un expander par groupe seulement, puis affichage
    compact (colonnes + tableau) pour chaque fichier.
    """
    import pandas as pd

    st.header("🔎 Détails par mot-clé (occurrences)")
    st.markdown(f"Affiche jusqu'à les top {top_n} mots-clés par CV (seuil min {min_count}).")

    for base, group in df_sorted.groupby("base_name"):
        with st.expander(f"📄 Groupe : {base}", expanded=False):
            for _, row in group.iterrows():
                fname = row.get("Fichier") or row.get("filename") or row.get("nom", "<inconnu>")
                counts = keyword_details.get(fname, {})

                # Filtrer et trier par occurrences décroissantes
                # filtered = [(k, v) for k, v in counts.items() if v >= min_count]
                filtered = [(k, v) for k, v in counts.items()]
                if not filtered:
                    st.write(f"**{fname}** — Aucun mot-clé trouvé (selon le seuil).")
                    continue

                filtered.sort(key=lambda x: x[1], reverse=True)
                # top = filtered[:top_n]
                # df_kw = pd.DataFrame(top, columns=["Mot-clé", "Occurrences"])

                df_kw = filtered

                # Affichage compact : colonne gauche = nom du fichier, droite = tableau
                c1, c2 = st.columns([1, 3])
                c1.markdown(f"**{fname}**")
                c2.dataframe(df_kw, use_container_width=True)

                st.markdown("---")