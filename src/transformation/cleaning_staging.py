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


# Création de la table race_control
race_control=lecture_fichier_json("race_control")
race_control=race_control.loc[((race_control["category"].isin(["Flag","SafetyCar"]))&(~race_control["flag"].isin(["BLUE","BLACK AND WHITE"])))|((race_control["category"]=="Other") & (race_control["message"].str.contains("SECOND TIME PENALTY")) & ~race_control["message"].str.contains("PENALTY SERVED")),["session_key","lap_number","category","flag","scope","sector","qualifying_phase","message"]].drop_duplicates()
race_control["driver_number"] = race_control["message"].str.extract(r'PENALTY FOR CAR ([0-9]*) ').astype('Int64') # il faut créer pour le numéro du pilote lors des penalites
race_control["lap_number"] = race_control["lap_number"].astype('Int64')
race_control["sector"] = race_control["sector"].astype('Int64')
race_control["qualifying_phase"] = race_control["qualifying_phase"].astype('Int64')
verification_dossier_parents("race_control", niveau)
enregistrement_donnees(niveau,race_control,"race_control")


# Création de la table session_result
session_result=lecture_fichier_json("session_result")
session_result = session_result[["position","driver_number","number_of_laps","dnf","dns","dsq","duration","gap_to_leader","session_key","points"]]
session_result["number_of_laps"] = session_result["number_of_laps"].astype('Int64')
session_result["duration"] = session_result["duration"].astype(str)
session_result["gap_to_leader"] = session_result["gap_to_leader"].astype(str)
verification_dossier_parents("session_result", niveau)
enregistrement_donnees(niveau,session_result,"session_result")


# création des tables sessions
sessions=lecture_fichier_json("sessions",True)
sessions = sessions[["session_key","session_type","session_name","date_start","date_end","meeting_key","year"]]
verification_dossier_parents("sessions", niveau)
enregistrement_donnees(niveau,sessions,"sessions")


# Création de la table starting_grid
starting_grid=lecture_fichier_json("starting_grid")
starting_grid = starting_grid[["position","driver_number","lap_duration","session_key"]]
verification_dossier_parents("starting_grid", niveau)
enregistrement_donnees(niveau,starting_grid,"starting_grid")