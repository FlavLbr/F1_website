import requests
import json
from genericpath import exists
import os
import time
import pandas as pd
lien = "/workspaces/F1_website/data"
url_base = "https://api.openf1.org/v1/"

# Fonction qui vérifie si le fichier parents est créé.
# S'il ne l'est pas alors il le crée
def verification_dossier_parents(nom_table,partie):
    if not exists(f"{lien}/{partie}/{nom_table}"):
        os.mkdir(f"{lien}/{partie}/{nom_table}")

# Fonction qui permet d'enregister la données dans le dossier
def enregistrement_donnees(partie,fichier,nom_table, annee=None, is_annee=False):
    if partie=="raw":
        if is_annee:
            if not exists(f"{lien}/{partie}/{nom_table}/{annee}/"):
                os.mkdir(f"{lien}/{partie}/{nom_table}/{annee}/")
            with open(f"{lien}/{partie}/{nom_table}/{annee}/{nom_table}_{annee}.json","w") as fichier:
                json.dump(fichier,fichier)
        else:
            with open(f"{lien}/{partie}/{nom_table}/{nom_table}.json","w") as fichier:
                json.dump(fichier,fichier)

    else:
        fichier.to_parquet(f"{lien}/{partie}/{nom_table}/{nom_table}.parquet", compression="ZSTD")

def lecture_fichier_json(nom_table, is_annee=False):
    if is_annee:
        path_table=os.walk(f"/workspaces/F1_website/data/raw/{nom_table}")
        df=pd.DataFrame()
        for fichiers in path_table:
            for fichier in fichiers[2]:
                with open(fichiers[0]+"/"+fichier) as f:
                    data = json.load(f)
                    df=pd.concat([df,pd.json_normalize(data)])
    else:
        with open(f"/workspaces/F1_website/data/raw/{nom_table}/{nom_table}.json") as f:
            df=pd.json_normalize(json.load(f))
    
    return df
