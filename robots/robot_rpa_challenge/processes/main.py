"""
ROBOT - main.py
===============
Script principal du robot RPA Challenge.
Lit les données d'un fichier Excel et remplit le formulaire RPA Challenge.

Emplacement : rpaaas-robots/robots/robot_rpa_challenge/processes/main.py

Structure du projet :
    rpaaas-robots/
    ├── vbo/
    │   ├── utility_browser/
    │   │   └── vbo_browser.py
    │   └── utility_excel/
    │       └── vbo_excel.py
    └── robots/
        └── robot_rpa_challenge/
            └── processes/
                └── main.py         ← CE FICHIER
"""

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
URL_RPA_CHALLENGE  = "http://www.rpachallenge.com"
CHEMIN_EXCEL       = r"C:\Users\Shadow\Documents\Projets\RPAaas\code_source\rpaaas-robots\robots\robot_rpa_challenge\data\challenge.xlsx"
FEUILLE_EXCEL      = "Sheet1"

# Correspondance : colonne Excel → sélecteur XPATH du formulaire
CHAMPS_FORMULAIRE = {
    "First Name"  : "//input[@ng-reflect-name='labelFirstName']",
    "Last Name"   : "//input[@ng-reflect-name='labelLastName']",
    "Company Name": "//input[@ng-reflect-name='labelCompanyName']",
    "Role in Company": "//input[@ng-reflect-name='labelRole']",
    "Address"     : "//input[@ng-reflect-name='labelAddress']",
    "Email"       : "//input[@ng-reflect-name='labelEmail']",
    "Phone Number": "//input[@ng-reflect-name='labelPhone']",
}


# ── Logique principale ────────────────────────────────────────────────────────

def main():
    logger.info("═" * 60)
    logger.info("Démarrage du robot RPA Challenge")
    logger.info("═" * 60)

    driver = None
    try:
        # ── Étape 1 : Lecture du fichier Excel ────────────────────────────────
        logger.info("Étape 1 : Lecture du fichier Excel")
        df = ouvrir_excel(CHEMIN_EXCEL, feuille=FEUILLE_EXCEL)
        if df is None:
            logger.error("Impossible de lire le fichier Excel. Arrêt du robot.")
            return

        logger.info("%d contacts trouvés dans le fichier.", len(df))

        # ── Étape 2 : Ouvrir le navigateur ───────────────────────────────────
        logger.info("Étape 2 : Ouverture du navigateur")
        driver = ouvrir_navigateur(headless=False)

        # ── Étape 3 : Naviguer vers le site ──────────────────────────────────
        logger.info("Étape 3 : Navigation vers le site")
        if not naviguer(driver, URL_RPA_CHALLENGE):
            logger.error("Impossible de charger le site. Arrêt du robot.")
            return

        # ── Étape 4 : Cliquer sur Start ───────────────────────────────────────
        logger.info("Étape 4 : Clic sur le bouton Start")
        if not cliquer_bouton(driver, By.XPATH, "//button[contains(text(),'Start')]"):
            logger.error("Bouton Start introuvable. Arrêt du robot.")
            return

        # ── Étape 5 : Traiter chaque ligne Excel ──────────────────────────────
        logger.info("Étape 5 : Traitement des contacts")

        for i in range(len(df)):
            logger.info("── Contact %d/%d ──────────────────────────────", i + 1, len(df))

            # Lire la ligne courante
            contact = lire_ligne(df, i)

            # Remplir chaque champ du formulaire avec la valeur Excel correspondante
            for colonne_excel, xpath_champ in CHAMPS_FORMULAIRE.items():
                valeur = contact.get(colonne_excel, "")
                ecrire_dans_champ(driver, By.XPATH, xpath_champ, valeur)

            # Soumettre le formulaire
            logger.info("Soumission du formulaire pour le contact %d", i + 1)
            if not cliquer_bouton(driver, By.XPATH, "//input[@value='Submit']"):
                logger.error("Bouton Submit introuvable au contact %d. Arrêt.", i + 1)
                return

            logger.info("Contact %d soumis avec succès.", i + 1)

    except Exception as e:
        logger.exception("Erreur inattendue : %s", e)

    finally:
        logger.info("Fermeture du navigateur")
        fermer_navigateur(driver)
        logger.info("═" * 60)
        logger.info("Fin du robot RPA Challenge")
        logger.info("═" * 60)


if __name__ == "__main__":
    main()