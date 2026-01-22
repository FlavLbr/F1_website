import requests
import json
from genericpath import exists
import os
import pandas as pd

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from package_commun import verification_dossier_parents,enregistrement_donnees
lien = "/workspaces/F1_website/data"
url_base = "https://api.openf1.org/v1/"
niveau="staging"


# Code pour la création des tables dans staging

# Création de la table teams et drivers propre
with open(f"/workspaces/F1_website/data/raw/drivers/drivers.json") as f:
    drivers=pd.json_normalize(json.load(f))

teams = drivers[["meeting_key","team_name","team_colour"]].drop_duplicates()

verification_dossier_parents("teams", niveau)
teams.to_parquet(f"{lien}/{niveau}/teams/teams.parquet", compression="ZSTD")