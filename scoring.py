from collections import Counter
from text_utils import nettoyer_texte, extraire_mots_cles_offre

def score_cv_offre(cv_text: str, offre_text: str):
    """Score simple basé sur la présence des mots-clés."""
    cv_clean = nettoyer_texte(cv_text)
    cv_mots = set(cv_clean.split())

    mots_cles = extraire_mots_cles_offre(offre_text)
    nb_trouves = sum(1 for mot in mots_cles if mot in cv_mots)

    return (nb_trouves / len(mots_cles) * 100) if mots_cles else 0

# def score_cv_frequence(cv_text: str, offre_text: str, max_occurrences=2):
#     """Score pondéré par la fréquence avec limite max."""
#     cv_clean = nettoyer_texte(cv_text)
#     cv_mots = cv_clean.split()
#     cv_counts = Counter(cv_mots)

#     mots_cles = extraire_mots_cles_offre(offre_text)

#     score_total = sum(min(cv_counts.get(mot, 0), max_occurrences) for mot in mots_cles)
#     max_score = len(mots_cles) * max_occurrences

#     return (score_total / max_score * 100) if max_score > 0 else 0

def score_cv_frequence(cv_text: str, 
                       offre_text: str, 
                       max_occurrences=2):
    """
    Score pondéré par la fréquence avec limite max.
    Retourne le score et le détail des occurrences par mot-clé.
    
    Args:
        cv_text (str): Le texte nettoyé du CV.
        offre_text (str): Le texte de l'offre de poste.
        max_occurrences (int): La limite maximale de fréquence pour le scoring.

    Returns:
        tuple: (float score_final, dict details_des_occurrences)
    """
    print("In score_cv_frequence with max_occurrences =", max_occurrences)
    cv_clean = nettoyer_texte(cv_text)
    cv_mots = cv_clean.split()
    cv_counts = Counter(cv_mots)

    mots_cles = extraire_mots_cles_offre(offre_text)

    score_total = 0
    keyword_occurrences = {} # Dictionnaire pour stocker les détails

    for mot in mots_cles:
        count = cv_counts.get(mot, 0)
        
        # 1. Calcul du score (avec la limite max_occurrences)
        score_contribution = min(count, max_occurrences)
        score_total += score_contribution
        
        # 2. Enregistrement des détails (occurrence réelle)
        # On enregistre la valeur réelle trouvée dans le CV, pas la contribution plafonnée.
        keyword_occurrences[mot] = count 
        
    # Afficher toutes valeurs uniques trouvées
    unique_values = set(keyword_occurrences.values())
    print("Valeurs uniques des occurrences trouvées :", unique_values)

    max_score = len(mots_cles) * max_occurrences
    final_score = (score_total / max_score * 100) if max_score > 0 else 0

    return final_score, keyword_occurrences
