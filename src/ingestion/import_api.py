import requests
from genericpath import exists
import time

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from package_commun import verification_dossier_parents,enregistrement_donnees
lien = "/workspaces/F1_website/data"
url_base = "https://api.openf1.org/v1/"
niveau="raw"


# Partie pour les tables Meeting, Session et Pit qui ont une année
years=["2023","2024","2025","2026"]
noms=["meetings","sessions","pit"]

for n in noms:
    verification_dossier_parents(n, niveau)

    for y in years:
        if n=="pit":
            response = requests.get(url_base+n+f"?date>{int(y)-1}-12-31&date<{int(y)+1}-01-01")
        else:
            response = requests.get(url_base+n+"?year="+y)
        time.sleep(0.4)

        enregistrement_donnees(niveau, response.json(), n, y, True)



