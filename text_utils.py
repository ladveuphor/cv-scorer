import re
from collections import Counter
from nltk.corpus import stopwords
import nltk

# Charger stopwords FR
nltk.download('stopwords')
stop_fr = set(stopwords.words('french'))

def nettoyer_texte(texte: str) -> str:
    """Nettoyage standard : minuscules + suppression caractères spéciaux."""
    texte = texte.lower()
    texte = re.sub(r"[^a-zàâçéèêëîïôûùüÿñæœ0-9\s]", " ", texte)
    texte = re.sub(r"\s+", " ", texte)
    return texte.strip()

def extraire_mots_cles_offre(offre_text: str):
    """Extraction des mots-clés sans stop words."""
    texte = nettoyer_texte(offre_text)
    mots = texte.split()
    return list(set([mot for mot in mots if mot not in stop_fr]))