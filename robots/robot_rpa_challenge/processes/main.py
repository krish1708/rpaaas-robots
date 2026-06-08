"""
ROBOT - main.py
===============
Script principal du robot RPA Challenge.

Emplacement : rpaaas-robots/robots/robot_rpa_challenge/processes/main.py
"""

import sys
import os
import logging
from datetime import datetime

# ── Ajout du VBO dans le chemin Python ────────────────────────────────────────
chemin_vbo = r"C:\Users\Shadow\Documents\Projets\RPAaas\code_source\rpaaas-robots\vbo\utility_browser"
sys.path.append(chemin_vbo)

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

# ── Import du VBO ─────────────────────────────────────────────────────────────
from vbo_browser import (
    ouvrir_navigateur,
    naviguer,
    attendre_element,
    ecrire_dans_champ,
    cliquer_bouton,
    fermer_navigateur
)
from selenium.webdriver.common.by import By

# ── Configuration du robot ────────────────────────────────────────────────────
URL_RPA_CHALLENGE = "http://www.rpachallenge.com"


# ── Logique principale ────────────────────────────────────────────────────────

def main():
    logger.info("═" * 60)
    logger.info("Démarrage du robot RPA Challenge")
    logger.info("═" * 60)

    driver = None
    try:
        # Étape 1 : Ouvrir le navigateur
        logger.info("Étape 1 : Ouverture du navigateur")
        driver = ouvrir_navigateur(headless=False)

        # Étape 2 : Naviguer vers le site
        logger.info("Étape 2 : Navigation vers le site")
        succes = naviguer(driver, URL_RPA_CHALLENGE)
        if not succes:
            logger.error("Impossible de charger le site. Arrêt du robot.")
            return

        # Étape 3 : Cliquer sur Start
        logger.info("Étape 3 : Clic sur le bouton Start")
        if not cliquer_bouton(driver, By.XPATH, "//button[contains(text(),'Start')]"):
            logger.error("Bouton Start introuvable. Arrêt du robot.")
            return

        # Étape 4 : Remplir le formulaire (exemple avec les champs RPA Challenge)
        logger.info("Étape 4 : Remplissage du formulaire")

        ecrire_dans_champ(driver, By.XPATH, "//input[@ng-reflect-name='labelFirstName']", "John")
        ecrire_dans_champ(driver, By.XPATH, "//input[@ng-reflect-name='labelLastName']",  "Doe")
        ecrire_dans_champ(driver, By.XPATH, "//input[@ng-reflect-name='labelCompanyName']","Acme Corp")
        ecrire_dans_champ(driver, By.XPATH, "//input[@ng-reflect-name='labelRole']",       "Developer")
        ecrire_dans_champ(driver, By.XPATH, "//input[@ng-reflect-name='labelAddress']",    "123 Main St")
        ecrire_dans_champ(driver, By.XPATH, "//input[@ng-reflect-name='labelEmail']",      "john@acme.com")
        ecrire_dans_champ(driver, By.XPATH, "//input[@ng-reflect-name='labelPhone']",      "0600000000")

        # Étape 5 : Soumettre le formulaire
        logger.info("Étape 5 : Soumission du formulaire")
        if not cliquer_bouton(driver, By.XPATH, "//input[@value='Submit']"):
            logger.error("Bouton Submit introuvable. Arrêt du robot.")
            return

        logger.info("Formulaire soumis avec succès.")

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