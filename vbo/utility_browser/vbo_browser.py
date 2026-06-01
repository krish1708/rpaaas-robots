"""
VBO Browser - Visual Business Object
Équivalent Blue Prism : Web Browser Object Page
Toutes les actions élémentaires sur le navigateur web.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
import time

from typing import Optional, Any

logger = logging.getLogger(__name__)


class VBOBrowser:
    """
    VBO Web Browser
    Inspiré des Object Pages Blue Prism.
    Chaque méthode = 1 action atomique réutilisable.
    """

    def __init__(self, headless: bool = False, timeout: int = 10):
        self.driver = None
        self.timeout = timeout
        self.headless = headless

    # ─────────────────────────────────────────
    # INITIALISATION / FERMETURE
    # Équivalent : "Initialise" et "Close" en BP
    # ─────────────────────────────────────────

    def initialise(self) -> bool:
        """Ouvre le navigateur Chrome."""
        try:
            options = Options()
            if self.headless:
                options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--window-size=1920,1080")

            self.driver = webdriver.Chrome(options=options)
            self.driver.implicitly_wait(self.timeout)
            logger.info("[VBO Browser] Navigateur initialisé")
            return True
        except Exception as e:
            logger.error(f"[VBO Browser] Erreur initialisation : {e}")
            return False

    def close(self) -> bool:
        """Ferme le navigateur proprement."""
        try:
            if self.driver:
                self.driver.quit()
                self.driver = None
            logger.info("[VBO Browser] Navigateur fermé")
            return True
        except Exception as e:
            logger.error(f"[VBO Browser] Erreur fermeture : {e}")
            return False

    # ─────────────────────────────────────────
    # NAVIGATION
    # Équivalent : actions "Navigate" en BP
    # ─────────────────────────────────────────

    def navigate_to(self, url: str) -> bool:
        """Navigue vers une URL."""
        try:
            self.driver.get(url)
            logger.info(f"[VBO Browser] Navigation vers : {url}")
            return True
        except Exception as e:
            logger.error(f"[VBO Browser] Erreur navigation : {e}")
            return False

    def get_current_url(self) -> str:
        """Retourne l'URL courante."""
        return self.driver.current_url

    def get_page_title(self) -> str:
        """Retourne le titre de la page."""
        return self.driver.title

    def go_back(self) -> bool:
        """Retour à la page précédente."""
        try:
            self.driver.back()
            return True
        except Exception as e:
            logger.error(f"[VBO Browser] Erreur retour : {e}")
            return False

    # ─────────────────────────────────────────
    # INTERACTIONS ÉLÉMENTS
    # Équivalent : actions "Click", "Type" en BP
    # ─────────────────────────────────────────

    def click_element(self, locator: str, by: By = By.XPATH) -> bool:
        """Clique sur un élément."""
        try:
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.element_to_be_clickable((by, locator))
            )
            element.click()
            logger.info(f"[VBO Browser] Clic sur : {locator}")
            return True
        except TimeoutException:
            logger.error(f"[VBO Browser] Élément non cliquable : {locator}")
            return False

    def type_text(self, locator: str, text: str, by: By = By.XPATH, clear_first: bool = True) -> bool:
        """Saisit du texte dans un champ."""
        try:
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((by, locator))
            )
            if clear_first:
                element.clear()
            element.send_keys(text)
            logger.info(f"[VBO Browser] Saisie dans {locator} : '{text}'")
            return True
        except TimeoutException:
            logger.error(f"[VBO Browser] Champ introuvable : {locator}")
            return False

    def press_key(self, locator: str, key: Keys, by: By = By.XPATH) -> bool:
        """Appuie sur une touche clavier dans un élément."""
        try:
            element = self.driver.find_element(by, locator)
            element.send_keys(key)
            return True
        except NoSuchElementException:
            logger.error(f"[VBO Browser] Élément introuvable pour key press : {locator}")
            return False

    # ─────────────────────────────────────────
    # LECTURE DE DONNÉES
    # Équivalent : actions "Get Text", "Get Value" en BP
    # ─────────────────────────────────────────

    def get_text(self, locator: str, by: By = By.XPATH) -> Optional[str]:
        """Récupère le texte d'un élément."""
        try:
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((by, locator))
            )
            text = element.text
            logger.info(f"[VBO Browser] Texte lu : '{text}'")
            return text
        except TimeoutException:
            logger.error(f"[VBO Browser] Élément introuvable pour lecture : {locator}")
            return None

    def get_attribute(self, locator: str, attribute: str, by: By = By.XPATH) -> Optional[str]:
        """Récupère la valeur d'un attribut HTML."""
        try:
            element = self.driver.find_element(by, locator)
            return element.get_attribute(attribute)
        except NoSuchElementException:
            logger.error(f"[VBO Browser] Attribut '{attribute}' introuvable sur : {locator}")
            return None

    # ─────────────────────────────────────────
    # ATTENTES / CONDITIONS
    # Équivalent : "Wait For Element" en BP
    # ─────────────────────────────────────────

    def wait_for_element(self, locator: str, by: By = By.XPATH, timeout: int = None) -> bool:
        """Attend qu'un élément soit présent."""
        t = timeout or self.timeout
        try:
            WebDriverWait(self.driver, t).until(
                EC.presence_of_element_located((by, locator))
            )
            logger.info(f"[VBO Browser] Élément trouvé : {locator}")
            return True
        except TimeoutException:
            logger.warning(f"[VBO Browser] Timeout - élément absent : {locator}")
            return False

    def wait_for_url_contains(self, partial_url: str, timeout: int = None) -> bool:
        """Attend que l'URL contienne une chaîne."""
        t = timeout or self.timeout
        try:
            WebDriverWait(self.driver, t).until(
                EC.url_contains(partial_url)
            )
            return True
        except TimeoutException:
            logger.warning(f"[VBO Browser] URL n'a pas changé vers : {partial_url}")
            return False

    def element_exists(self, locator: str, by: By = By.XPATH) -> bool:
        """Vérifie si un élément existe sur la page."""
        try:
            self.driver.find_element(by, locator)
            return True
        except NoSuchElementException:
            return False

    # ─────────────────────────────────────────
    # UTILITAIRES
    # ─────────────────────────────────────────

    def take_screenshot(self, path: str) -> bool:
        """Prend une capture d'écran."""
        try:
            self.driver.save_screenshot(path)
            logger.info(f"[VBO Browser] Screenshot : {path}")
            return True
        except Exception as e:
            logger.error(f"[VBO Browser] Erreur screenshot : {e}")
            return False

    def scroll_to_element(self, locator: str, by: By = By.XPATH) -> bool:
        """Scroll jusqu'à un élément."""
        try:
            element = self.driver.find_element(by, locator)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.3)
            return True
        except Exception as e:
            logger.error(f"[VBO Browser] Erreur scroll : {e}")
            return False

    def execute_js(self, script: str) -> any:
        """Exécute du JavaScript dans la page."""
        return self.driver.execute_script(script)
