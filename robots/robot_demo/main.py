import sys
import os

chemin_vbo = r"C:\Users\Shadow\Documents\Projets\RPAaas\code_source\rpaaas-robots\vbo\utility_browser"
sys.path.append(chemin_vbo)

print(f"chemin_vbo       : {chemin_vbo}")
print(f"Le dossier existe : {os.path.exists(chemin_vbo)}")

from vbo_browser import ouvrir_navigateur, naviguer, attendre_element, fermer_navigateur
from selenium.webdriver.common.by import By

URL_RPA_CHALLENGE = "http://www.rpachallenge.com"

def main():
    driver = None
    try:
        driver = ouvrir_navigateur(headless=False)

        succes = naviguer(driver, URL_RPA_CHALLENGE)
        if not succes:
            print("[MAIN] Impossible de charger le site. Arrêt.")
            return

        btn_start = attendre_element(driver, By.XPATH, "//button[contains(text(),'Start')]")
        if not btn_start:
            print("[MAIN] Bouton Start introuvable. Arrêt.")
            return

        print("[MAIN] Site prêt — actions métier à compléter ici.")

    except Exception as e:
        print(f"[MAIN] Erreur inattendue : {e}")

    finally:
        fermer_navigateur(driver)

if __name__ == "__main__":
    main()