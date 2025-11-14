import os
from docx import Document

def lire_docx(path):
    """Extrait le texte brut d'un fichier docx."""
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs)

def lire_tous_les_cvs(folder_path):
    """Retourne un dict {nom_fichier: texte}."""
    cvs = {}
    for f in os.listdir(folder_path):
        if f.lower().endswith(".docx"):
            cvs[f] = lire_docx(os.path.join(folder_path, f))
    return cvs