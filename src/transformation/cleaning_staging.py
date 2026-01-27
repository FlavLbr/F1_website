import requests
import json
from genericpath import exists
import os
import pandas as pd

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from package_commun import verification_dossier_parents,enregistrement_donnees,lecture_fichier_json
lien = "/workspaces/F1_website/data"
url_base = "https://api.openf1.org/v1/"
niveau="staging"


# Code pour la création des tables dans staging

# Création de la table teams et drivers propre
drivers=lecture_fichier_json("drivers")

teams = drivers[["meeting_key","team_name","team_colour"]].drop_duplicates()
verification_dossier_parents("teams", niveau)
enregistrement_donnees(niveau,teams,"teams")

table_nation=drivers[["full_name","country_code"]][~drivers["country_code"].isnull()].drop_duplicates()
table=drivers[["meeting_key","driver_number", "full_name","name_acronym","team_name","headshot_url"]].drop_duplicates()
table = pd.merge(table, table_nation, on=["full_name"], how="left")
drivers2 = table[["meeting_key","driver_number", "full_name","name_acronym","team_name","headshot_url","country_code"]].drop_duplicates()
verification_dossier_parents("drivers", niveau)
enregistrement_donnees(niveau,drivers2,"drivers")

# création des tables country, circuit et meeting
meet=lecture_fichier_json("meetings",True)

countries = meet[["country_code","country_name","country_flag"]].drop_duplicates()
verification_dossier_parents("countries", niveau)
enregistrement_donnees(niveau,countries,"countries")

circuits = meet[["circuit_key","location","country_code","circuit_short_name","circuit_type","circuit_image"]].drop_duplicates()
verification_dossier_parents("circuits", niveau)
enregistrement_donnees(niveau,circuits,"circuits")

meetings = meet.loc[meet["meeting_name"].str.contains("Grand Prix"),["meeting_key","meeting_name","meeting_official_name","circuit_key","gmt_offset","date_start","date_end","year"]]
verification_dossier_parents("meetings", niveau)
enregistrement_donnees(niveau,meetings,"meetings")