from shared.logger import get_logger

log = get_logger()

def run():
    log.info("Démarrage du robot demo")

    try:
        log.info("Étape 1 : lecture des données")
        log.info("Étape 2 : traitement")
        log.info("Étape 3 : export du résultat")

        log.success("Robot terminé avec succès")

    except Exception as e:
        log.exception(f"Erreur robot : {e}")
        raise