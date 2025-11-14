# display.py
import streamlit as st
import pandas as pd

def afficher_groupes_console(df_sorted):
    """Affichage console (réutilisable ailleurs)."""
    for base, group in df_sorted.groupby("base_name"):
        print(f"\n📄 {base}")
        for _, r in group.iterrows():
            gain = f"(+{r['gain_vs_original']:.2f})" if r['gain_vs_original'] > 0 else f"({r['gain_vs_original']:.2f})"
            print(f"   {r['Fichier']:<80} {r['Score']:6.2f} {gain}")

def st_afficher_table(df_sorted):
    """Affichage Streamlit : tableau + export CSV + grouping view."""
    st.write("### Résultats (triés)")
    st.dataframe(df_sorted.style.format({"Score": "{:.2f}", "gain_vs_original": "{:+.2f}"}), height=400)

    csv = df_sorted.to_csv(index=False).encode("utf-8")
    st.download_button("Télécharger CSV", csv, file_name="scores_cv.csv", mime="text/csv")

    st.write("### Vue groupée")
    for base, group in df_sorted.groupby("base_name"):
        with st.expander(f"{base} ({len(group)} files)"):
            st.table(group[["Fichier", "Score", "original_score", "gain_vs_original"]].round(2))
