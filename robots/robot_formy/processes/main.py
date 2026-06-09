import sys
import os
import logging
from datetime import datetime

# ── Ajout des VBO dans le chemin Python ───────────────────────────────────────
RACINE = r"C:\Users\Shadow\Documents\Projets\RPAaas\code_source\rpaaas-robots"

sys.path.append(os.path.join(RACINE, "vbo", "utility_browser"))
sys.path.append(os.path.join(RACINE, "vbo", "utility_excel"))

# ── Configuration des logs ────────────────────────────────────────────────────
DOSSIER_LOGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
os.makedirs(DOSSIER_LOGS, exist_ok=True)

NOM_FICHIER_LOG = f"robot_rpa_challenge_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
CHEMIN_LOG = os.path.join(DOSSIER_LOGS, NOM_FICHIER_LOG)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(CHEMIN_LOG, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("rpaaas.main")

# ── Import des VBO ────────────────────────────────────────────────────────────
from vbo_browser import (
    ouvrir_navigateur,
    naviguer,
    attendre_element,
    ecrire_dans_champ,
    cliquer_bouton,
    fermer_navigateur
)
from vbo_excel import ouvrir_excel, lire_ligne
from selenium.webdriver.common.by import By

# ── Configuration du robot ────────────────────────────────────────────────────
URL_RPA_CHALLENGE  = "https://formy-project.herokuapp.com/form"
CHEMIN_EXCEL       = r"C:\Users\Shadow\Documents\Projets\RPAaas\code_source\rpaaas-robots\robots\formy\data\challenge.xlsx"
FEUILLE_EXCEL      = "Sheet1"