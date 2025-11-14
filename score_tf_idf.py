import re
import os
from docx import Document
from collections import Counter
from nltk.corpus import stopwords
import nltk
import pandas as pd
pd.set_option('display.max_colwidth', None)

# Téléchargement des stopwords français si nécessaire
nltk.download('stopwords')
stop_fr = set(stopwords.words('french'))

def lire_docx(path):
    """Extrait le texte brut d'un fichier Word (.docx)."""
    doc = Document(path)
    full_text = [p.text for p in doc.paragraphs]
    return "\n".join(full_text)

# --- Nettoyage de texte ---
def nettoyer_texte(texte: str) -> str:
    """Met en minuscules et supprime caractères spéciaux."""
    texte = texte.lower()
    texte = re.sub(r"[^a-zàâçéèêëîïôûùüÿñæœ0-9\s]", " ", texte)
    texte = re.sub(r"\s+", " ", texte)
    return texte.strip()

# --- Extraction des mots clés d'une offre (stop words exclus) ---
def extraire_mots_cles_offre(offre_text: str):
    """
    Retourne la liste des mots clés uniques de l'offre après nettoyage
    et suppression des stop words français.
    """
    texte = nettoyer_texte(offre_text)
    mots = texte.split()
    # Exclusion des stop words
    mots_cles = [mot for mot in mots if mot not in stop_fr]
    return list(set(mots_cles))  # mots uniques

# --- Score de correspondance CV vs offre ---
def score_cv_offre(cv_text: str, offre_text: str):
    """
    Calcule un score de correspondance CV vs offre basé à la fois sur la présence 
    et la fréquence des mots-clés de l'offre dans le CV.

    Contrairement à la version simple, cette fonction prend en compte plusieurs 
    occurrences d'un mot-clé dans le CV tout en limitant l'impact d'un mot très 
    répété grâce à `max_occurrences`.

    Algorithme :
    1. Nettoyage du texte du CV (minuscules, suppression de ponctuation, etc.).
    2. Séparation du texte en mots et comptage des occurrences de chaque mot via Counter.
    3. Extraction des mots-clés uniques de l'offre (après nettoyage).
    4. Pour chaque mot-clé de l'offre, ajouter au score le nombre d’occurrences 
       présentes dans le CV, limité par `max_occurrences` pour éviter qu’un mot
       unique répété 100 fois domine le score.
    5. Normalisation : le score total est divisé par le score maximum possible 
       (nombre de mots-clés * max_occurrences) pour obtenir un pourcentage.
    
    Arguments :
    - cv_text (str) : texte complet du CV.
    - offre_text (str) : texte complet de l'offre.
    - max_occurrences (int, optionnel) : nombre maximal d’occurrences par mot-clé
      comptabilisées pour le score (défaut 2).

    Retour :
    - score_pct (float) : pourcentage de correspondance entre le CV et l'offre, 
      basé sur la diversité et la fréquence des mots-clés.

    Exemple :
    >>> score_cv_frequence(cv_text, offre_text)
    62.5
    """
    cv_clean = nettoyer_texte(cv_text)
    cv_mots = set(cv_clean.split())

    mots_cles = extraire_mots_cles_offre(offre_text)
    # print("mots_cles:", mots_cles)

    nb_trouves = sum(1 for mot in mots_cles if mot in cv_mots)
    Score = nb_trouves / len(mots_cles) if mots_cles else 0

    return Score * 100  # Score en pourcentage

def score_cv_frequence(cv_text: str, offre_text: str, max_occurrences=2):
    """
    Score basé sur la présence et la fréquence des mots-clés contrairement à
    la fonction précedente.
    max_occurrences limite l'impact d'un mot répété.
    """
    cv_clean = nettoyer_texte(cv_text)
    cv_mots = cv_clean.split()
    cv_counts = Counter(cv_mots)

    mots_cles = extraire_mots_cles_offre(offre_text)

    score_total = 0
    for mot in mots_cles:
        score_total += min(cv_counts.get(mot, 0), max_occurrences)

    max_score = len(mots_cles) * max_occurrences
    score_pct = (score_total / max_score) * 100 if max_score > 0 else 0

    return score_pct

offre = """
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

# Test sur plusieurs CV 
# Faire une boucle sur les CV dans le dossier CVs
dossier_cvs = "CVs"
all_scores = {}
for nom_fichier in os.listdir(dossier_cvs):
    # Lis un CV .docx
    cv_text = lire_docx(f"./{dossier_cvs}/{nom_fichier}")

    Score = score_cv_offre(cv_text, offre)
    all_scores[nom_fichier] = Score
    print(f"Score de correspondance pour {nom_fichier} : {Score:.1f} %")
    
# Convertir all_scores en DataFrame pandas pour analyse ultérieure
df_scores = pd.DataFrame(list(all_scores.items()), columns=['Fichier', 'Score'])

# Tri par ordre croissant du Score
df_scores = df_scores.sort_values(by='Score', ascending=False)
df_scores

#### Tri par ordre alphabétique des fichiers
df_scores = df_scores.sort_values(by='Fichier', ascending=True)
df_scores

# Affichage par ordre croissant pour chaque groupe de CVs communs (CV original + CV améliorés)
# Liste connue des fichiers originaux
original_files = [
    "NRJBI_CEC_CV_Senior.docx",
    "NRJBI_ERE_CV - 20250930.docx",
    "NRJBI_CV_EMO_202510_revisionElise.docx",
]

# Extraire juste le nom sans extension pour faciliter la recherche
original_bases = [f.rsplit('.', 1)[0] for f in original_files]

# Trouver à quel original correspond chaque fichier
def find_base(Fichier):
    for base in original_bases:
        if Fichier.startswith(base):  # on compare le début du nom
            return base
    return Fichier  # si aucun match, on garde le nom lui-même

df_scores["base_name"] = df_scores["Fichier"].apply(find_base)

# S'il manque l'extension .docx dans base_name, on l'ajoute pour correspondre aux clés originales
df_scores["base_name"] = df_scores["base_name"].apply(lambda x: x + ".docx" if not x.endswith(".docx") else x)

# Trier : d’abord par base_name, puis par Score décroissant
df_sorted = df_scores.sort_values(["base_name", "Score"], ascending=[True, False]).reset_index(drop=True)

# On crée un dictionnaire base_name -> score original
original_score_dict = df_scores.set_index("Fichier").loc[original_files, "Score"].to_dict()

# Ajouter la colonne original_score à tous les fichiers selon leur base_name
df_sorted["original_score"] = df_sorted["base_name"].map(original_score_dict)

# Calculer le gain par rapport à l’original
df_sorted["gain_vs_original"] = df_sorted["Score"] - df_sorted["original_score"]

# Créer une colonne booléenne : True si c'est le CV original
df_sorted["is_original"] = df_sorted["Fichier"].isin(original_files)

# Trier : d'abord par base_name, puis par is_original (True en premier), puis par Score décroissant
df_sorted = df_sorted.sort_values(
    by=["base_name", "is_original", "Score"],
    ascending=[True, False, False]
).reset_index(drop=True)

# Supprimer la colonne temporaire si nécessaire
df_sorted = df_sorted.drop(columns="is_original")

# Affichage lisible
for base, group in df_sorted.groupby("base_name"):
    print(f"\n📄 {base}")
    for _, r in group.iterrows():
        gain = f"(+{r['gain_vs_original']:.2f})" if r['gain_vs_original'] > 0 else f"({r['gain_vs_original']:.2f})"
        print(f"   {r['Fichier']:<80} {r['Score']:6.2f} {gain}")