from collections import Counter
from text_utils import nettoyer_texte, extraire_mots_cles_offre

def score_cv_offre(cv_text: str, offre_text: str):
    """Score simple basé sur la présence des mots-clés."""
    cv_clean = nettoyer_texte(cv_text)
    cv_mots = set(cv_clean.split())

    mots_cles = extraire_mots_cles_offre(offre_text)
    nb_trouves = sum(1 for mot in mots_cles if mot in cv_mots)

    return (nb_trouves / len(mots_cles) * 100) if mots_cles else 0

def score_cv_frequence(cv_text: str, offre_text: str, max_occurrences=2):
    """Score pondéré par la fréquence avec limite max."""
    cv_clean = nettoyer_texte(cv_text)
    cv_mots = cv_clean.split()
    cv_counts = Counter(cv_mots)

    mots_cles = extraire_mots_cles_offre(offre_text)

    score_total = sum(min(cv_counts.get(mot, 0), max_occurrences) for mot in mots_cles)
    max_score = len(mots_cles) * max_occurrences

    return (score_total / max_score * 100) if max_score > 0 else 0
