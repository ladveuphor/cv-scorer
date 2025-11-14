import pandas as pd

def construire_df_scores(scores_dict):
    df = pd.DataFrame([{"Fichier": f, "Score": s} for f, s in scores_dict.items()])
    print("construire_df_scores res =", df.sort_values(by="Score", ascending=False).reset_index(drop=True))
    return df.sort_values(by="Score", ascending=False).reset_index(drop=True)

def mapper_cv_originaux(df_scores, original_files):
    original_bases = [f.rsplit(".", 1)[0] for f in original_files]

    def find_base(fname):
        for base in original_bases:
            if fname.startswith(base):
                return base + ".docx"
        return fname

    df_scores["base_name"] = df_scores["Fichier"].apply(find_base)
    print("mapper_cv_originaux res =", df_scores)
    return df_scores

def ajouter_gains(df_scores, original_files):
    original_score_dict = (
        df_scores[df_scores["Fichier"].isin(original_files)]
        .set_index("Fichier")["Score"]
        .to_dict()
    )

    df_scores["original_score"] = df_scores["base_name"].map(original_score_dict)
    df_scores["gain_vs_original"] = df_scores["Score"] - df_scores["original_score"]
    return df_scores

def trier_groupes(df_scores, original_files):
    df_scores["is_original"] = df_scores["Fichier"].isin(original_files)

    df_sorted = df_scores.sort_values(
        by=["base_name", "is_original", "Score"],
        ascending=[True, False, False]
    ).reset_index(drop=True)

    return df_sorted.drop(columns="is_original")
