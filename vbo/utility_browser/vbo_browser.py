"""
VBO - vbo_browser.py
====================
Bibliothèque générique de gestion du navigateur Chrome via Selenium.
Utilisable par n'importe quel robot du projet rpaaas-robots.

Emplacement : rpaaas-robots/vbo/utility_browser/vbo_browser.py

Fonctions exposées :
    - ouvrir_navigateur(headless)              : démarre Chrome, retourne le driver
    - naviguer(driver, url)                    : ouvre une URL et attend le chargement
    - attendre_element(driver, by, selecteur)  : attend qu'un élément soit visible
    - ecrire_dans_champ(driver, by, selecteur, texte) : efface et écrit dans un champ
    - cliquer_bouton(driver, by, selecteur)    : clique sur un élément
    - fermer_navigateur(driver)                : ferme proprement le navigateur
"""

import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


# ── Logger ────────────────────────────────────────────────────────────────────
logger = logging.getLogger("rpaaas.vbo_browser")

# ── Configuration par défaut ──────────────────────────────────────────────────
TIMEOUT = 15   # secondes d'attente maximale


# ── Fonctions ─────────────────────────────────────────────────────────────────

def ouvrir_navigateur(headless: bool = False) -> webdriver.Chrome:
    """
    Démarre Chrome et retourne le driver Selenium.

    Paramètres :
        headless (bool) : False = fenêtre visible (défaut)
                          True  = mode silencieux, sans interface graphique
    Retour :
        driver (webdriver.Chrome)
    """
    options = Options()

    if headless:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")

    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver  = webdriver.Chrome(service=service, options=options)

    logger.info("Navigateur Chrome ouvert (headless=%s)", headless)
    return driver


def naviguer(driver: webdriver.Chrome, url: str) -> bool:
    """
    Ouvre une URL et attend que la page soit complètement chargée.

    Paramètres :
        driver (webdriver.Chrome) : driver actif
        url    (str)              : adresse à ouvrir
    Retour :
        True si succès, False en cas d'erreur
    """
    try:
        logger.info("Navigation vers : %s", url)
        driver.get(url)

        WebDriverWait(driver, TIMEOUT).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        logger.info("Page chargée : %s", driver.title)
        return True

    except Exception as e:
        logger.error("Erreur de navigation vers %s : %s", url, e)
        return False


def attendre_element(
    driver: webdriver.Chrome,
    by: By,
    selecteur: str,
    timeout: int = TIMEOUT
):
    """
    Attend qu'un élément soit visible et le retourne.

    Paramètres :
        driver    (webdriver.Chrome) : driver actif
        by        (By)               : type de sélecteur (By.XPATH, By.ID, ...)
        selecteur (str)              : valeur du sélecteur
        timeout   (int)              : secondes d'attente (défaut : 15)
    Retour :
        WebElement si trouvé, None sinon
    """
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((by, selecteur))
        )
        logger.info("Élément trouvé : %s", selecteur)
        return element

    except Exception as e:
        logger.warning("Élément introuvable (%s) : %s", selecteur, e)
        return None


def ecrire_dans_champ(
    driver: webdriver.Chrome,
    by: By,
    selecteur: str,
    texte: str,
    timeout: int = TIMEOUT
) -> bool:
    """
    Efface le contenu d'un champ de texte et écrit la valeur souhaitée.

    Paramètres :
        driver    (webdriver.Chrome) : driver actif
        by        (By)               : type de sélecteur (By.XPATH, By.ID, ...)
        selecteur (str)              : valeur du sélecteur
        texte     (str)              : texte à saisir dans le champ
        timeout   (int)              : secondes d'attente (défaut : 15)
    Retour :
        True si succès, False en cas d'erreur

    Exemples :
        ecrire_dans_champ(driver, By.XPATH, "//input[@ng-reflect-name='labelFirstName']", "John")
        ecrire_dans_champ(driver, By.ID, "email", "john@example.com")
    """
    try:
        champ = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, selecteur))
        )
        champ.clear()                  # efface le contenu existant
        champ.send_keys(texte)         # écrit le nouveau texte
        logger.info("Champ renseigné (%s) : '%s'", selecteur, texte)
        return True

    except Exception as e:
        logger.error("Impossible d'écrire dans le champ (%s) : %s", selecteur, e)
        return False


def cliquer_bouton(
    driver: webdriver.Chrome,
    by: By,
    selecteur: str,
    timeout: int = TIMEOUT
) -> bool:
    """
    Attend qu'un bouton (ou n'importe quel élément cliquable) soit disponible
    et clique dessus.

    Paramètres :
        driver    (webdriver.Chrome) : driver actif
        by        (By)               : type de sélecteur (By.XPATH, By.ID, ...)
        selecteur (str)              : valeur du sélecteur
        timeout   (int)              : secondes d'attente (défaut : 15)
    Retour :
        True si succès, False en cas d'erreur

    Exemples :
        cliquer_bouton(driver, By.XPATH, "//button[contains(text(),'Start')]")
        cliquer_bouton(driver, By.ID, "btnSubmit")
        cliquer_bouton(driver, By.CSS_SELECTOR, ".btn-primary")
    """
    try:
        bouton = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, selecteur))
        )
        bouton.click()
        logger.info("Clic effectué sur : %s", selecteur)
        return True

    except Exception as e:
        logger.error("Impossible de cliquer sur (%s) : %s", selecteur, e)
        return False


def fermer_navigateur(driver: webdriver.Chrome) -> None:
    """
    Ferme le navigateur et libère les ressources.

    Paramètres :
        driver (webdriver.Chrome) : driver à fermer
    """
    if driver:
        driver.quit()
        logger.info("Navigateur fermé.")