from pipeline import pipeline_complet

original_files = [
    "NRJBI_CEC_CV_Senior.docx",
    "NRJBI_ERE_CV - 20250930.docx",
    "NRJBI_CV_EMO_202510_revisionElise.docx",
]

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

df_resultat = pipeline_complet(
    folder="CVs",
    original_files=original_files,
    offre=offre,
    mode="console"
)
