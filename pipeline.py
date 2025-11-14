from io_utils import lire_tous_les_cvs
from scoring import score_cv_frequence
from dataframe_utils import (
    construire_df_scores,
    mapper_cv_originaux,
    ajouter_gains,
    trier_groupes
)
from display import afficher_groupes_console

def pipeline_complet(folder, original_files, offre):
    cvs = lire_tous_les_cvs(folder)

    # Score des CV
    scores = {fname: score_cv_frequence(text, offre) for fname, text in cvs.items()}
    for f, s in scores.items():
        print(f"Score de correspondance pour {f} : {s:.1f} %")

    # Pipeline DataFrame
    df = construire_df_scores(scores)
    df = mapper_cv_originaux(df, original_files)
    df = ajouter_gains(df, original_files)
    df = trier_groupes(df, original_files)

    afficher_groupes_console(df)
    return df