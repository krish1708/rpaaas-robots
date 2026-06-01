"""
MAIN.PY — Point d'entrée du robot RPA
Inspiré de l'architecture Blue Prism :
  - Main Process Page qui orchestre les sous-processus
  - Appels aux VBO (Visual Business Objects)
  - Gestion des exceptions et du log centralisé

Exemple de cas métier :
  → Se connecter à un site web
  → Rechercher une information
  → Extraire le résultat
  → Fermer proprement
"""

import logging
import sys
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
from typing import Optional, Any

# Remonte à la racine du projet (rpaaas-robots)
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)

# Import du VBO Browser (notre Object Page)
from vbo.utility_browser.vbo_browser import VBOBrowser

# ─────────────────────────────────────────────────────────
# CONFIGURATION DU LOG — Équivalent journal Blue Prism
# ─────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    handlers=[
        logging.FileHandler(f"logs/robot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────
# PROCESSUS : INITIALISE
# Équivalent Blue Prism : page "Initialise"
# ─────────────────────────────────────────────────────────
def process_initialise(browser: VBOBrowser) -> bool:
    """
    Initialise les ressources nécessaires au robot.
    Retourne False si l'initialisation échoue → stop du robot.
    """
    logger.info("=" * 60)
    logger.info("PROCESSUS : Initialise")
    logger.info("=" * 60)

    success = browser.initialise()
    if not success:
        logger.error("Échec de l'initialisation du navigateur")
        return False

    logger.info("Initialisation réussie")
    return True


# ─────────────────────────────────────────────────────────
# PROCESSUS : GET DATA (depuis le web)
# Équivalent Blue Prism : page "Get Input Data"
# ─────────────────────────────────────────────────────────
def process_get_data(browser: VBOBrowser, search_term: str) -> Optional[str]:
    """
    Navigue sur un site, effectue une recherche,
    et récupère les données.
    Retourne un dict avec les résultats ou None si erreur.
    """
    logger.info("=" * 60)
    logger.info("PROCESSUS : Get Data")
    logger.info("=" * 60)

    # ── Action VBO : naviguer vers le site ──
    if not browser.navigate_to("https://www.wikipedia.org"):
        logger.error("Impossible d'accéder au site")
        return None

    # ── Attente de la page ──
    champ_recherche = "//input[@id='searchInput']"
    if not browser.wait_for_element(champ_recherche):
        logger.error("Page non chargée - champ recherche absent")
        return None

    # ── Action VBO : saisir le terme de recherche ──
    if not browser.type_text(champ_recherche, search_term):
        logger.error("Impossible de saisir le terme de recherche")
        return None

    # ── Action VBO : valider la recherche ──
    if not browser.press_key(champ_recherche, Keys.RETURN):
        logger.error("Impossible de valider la recherche")
        return None

    # ── Attente de la page de résultat ──
    if not browser.wait_for_url_contains("wiki"):
        logger.error("Page de résultat non chargée")
        return None

    # ── Action VBO : récupérer le titre de la page ──
    titre = browser.get_page_title()

    # ── Action VBO : récupérer le premier paragraphe ──
    premier_paragraphe = browser.get_text("(//div[@id='mw-content-text']//p[not(@class)])[1]")

    # ── Action VBO : screenshot pour audit ──
    browser.take_screenshot(f"logs/screenshot_{search_term.replace(' ', '_')}.png")

    data = {
        "search_term": search_term,
        "url": browser.get_current_url(),
        "titre": titre,
        "premier_paragraphe": premier_paragraphe,
    }

    logger.info(f"Données récupérées : {data['titre']}")
    return data


# ─────────────────────────────────────────────────────────
# PROCESSUS : PROCESS DATA
# Équivalent Blue Prism : page "Process Data"
# ─────────────────────────────────────────────────────────
def process_data(data: dict) -> dict:
    """
    Traite et enrichit les données récupérées.
    Ici : nettoyage, validation, transformation.
    """
    logger.info("=" * 60)
    logger.info("PROCESSUS : Process Data")
    logger.info("=" * 60)

    if not data:
        logger.warning("Aucune donnée à traiter")
        return {}

    # Nettoyage basique
    data["titre_propre"] = data.get("titre", "").replace(" — Wikipédia", "").strip()
    data["extrait"] = (data.get("premier_paragraphe") or "")[:300] + "..."
    data["traitement_ok"] = True

    logger.info(f"Traitement OK : {data['titre_propre']}")
    return data


# ─────────────────────────────────────────────────────────
# PROCESSUS : CLOSE DOWN
# Équivalent Blue Prism : page "Clean Up / Close Down"
# ─────────────────────────────────────────────────────────
def process_close_down(browser: VBOBrowser):
    """
    Ferme proprement toutes les ressources.
    Toujours exécuté, même en cas d'erreur.
    """
    logger.info("=" * 60)
    logger.info("PROCESSUS : Close Down")
    logger.info("=" * 60)

    browser.close()
    logger.info("Ressources libérées")


# ─────────────────────────────────────────────────────────
# MAIN — Orchestrateur principal
# Équivalent Blue Prism : Main Process avec exception handling
# ─────────────────────────────────────────────────────────
def main():
    logger.info("╔══════════════════════════════════════════════════════╗")
    logger.info("║           ROBOT RPA — DÉMARRAGE                     ║")
    logger.info("╚══════════════════════════════════════════════════════╝")

    # Instanciation du VBO Browser
    browser = VBOBrowser(headless=False, timeout=10)

    # Paramètre d'entrée du robot
    search_term = "Automatisation robotisée des processus"

    try:
        # ── ÉTAPE 1 : Initialise ──
        if not process_initialise(browser):
            logger.critical("Arrêt du robot : échec initialisation")
            sys.exit(1)

        # ── ÉTAPE 2 : Récupérer les données ──
        raw_data = process_get_data(browser, search_term)

        if raw_data is None:
            logger.error("Arrêt du robot : échec récupération données")
            sys.exit(1)

        # ── ÉTAPE 3 : Traiter les données ──
        final_data = process_data(raw_data)

        # ── RÉSULTAT FINAL ──
        logger.info("=" * 60)
        logger.info("RÉSULTAT FINAL")
        logger.info("=" * 60)
        logger.info(f"  Terme recherché : {final_data.get('search_term')}")
        logger.info(f"  Titre           : {final_data.get('titre_propre')}")
        logger.info(f"  URL             : {final_data.get('url')}")
        logger.info(f"  Extrait         : {final_data.get('extrait')}")

    except Exception as e:
        # Gestion exception globale — comme le "Global Exception Handler" en BP
        logger.critical(f"EXCEPTION NON GÉRÉE : {e}", exc_info=True)
        browser.take_screenshot("logs/screenshot_erreur.png")
        sys.exit(1)

    finally:
        # ── ÉTAPE 4 : Close Down — TOUJOURS exécuté ──
        process_close_down(browser)

    logger.info("╔══════════════════════════════════════════════════════╗")
    logger.info("║           ROBOT RPA — FIN OK                        ║")
    logger.info("╚══════════════════════════════════════════════════════╝")


if __name__ == "__main__":
    main()
