"""
VBO - vbo_excel.py
==================
Bibliothèque générique de lecture et mise à jour de fichiers Excel via pandas.
Utilisable par n'importe quel robot du projet rpaaas-robots.

Emplacement : rpaaas-robots/vbo/utility_excel/vbo_excel.py

Fonctions exposées :
    - ouvrir_excel(chemin_fichier, feuille)   : charge le fichier Excel en DataFrame
    - lire_cellule(df, ligne, colonne)         : lit la valeur d'une cellule
    - lire_ligne(df, ligne)                    : lit toute une ligne sous forme de dict
    - ecrire_cellule(df, ligne, colonne, valeur) : modifie la valeur d'une cellule
    - sauvegarder_excel(df, chemin_fichier, feuille) : sauvegarde le DataFrame dans le fichier
"""

import logging
import pandas as pd

# ── Logger ────────────────────────────────────────────────────────────────────
logger = logging.getLogger("rpaaas.vbo_excel")


# ── Fonctions ─────────────────────────────────────────────────────────────────

def ouvrir_excel(chemin_fichier: str, feuille: str = "Sheet1") -> pd.DataFrame:
    """
    Charge un fichier Excel et retourne son contenu sous forme de DataFrame.

    Paramètres :
        chemin_fichier (str) : chemin complet vers le fichier .xlsx
        feuille        (str) : nom de l'onglet à lire (défaut : "Sheet1")

    Retour :
        DataFrame pandas si succès, None en cas d'erreur

    Exemple :
        df = ouvrir_excel(r"C:\data\contacts.xlsx", feuille="Contacts")
    """
    try:
        df = pd.read_excel(chemin_fichier, sheet_name=feuille, dtype=str)
        df = df.fillna("")   # remplace les cellules vides par "" (plus pratique)
        logger.info("Fichier ouvert : %s | Feuille : %s | %d lignes, %d colonnes",
                    chemin_fichier, feuille, len(df), len(df.columns))
        return df

    except FileNotFoundError:
        logger.error("Fichier introuvable : %s", chemin_fichier)
        return None

    except Exception as e:
        logger.error("Erreur lors de l'ouverture du fichier (%s) : %s", chemin_fichier, e)
        return None


def lire_cellule(df: pd.DataFrame, ligne: int, colonne: str) -> str:
    """
    Lit la valeur d'une cellule à partir de son numéro de ligne et du nom de colonne.

    Paramètres :
        df      (DataFrame) : DataFrame chargé avec ouvrir_excel()
        ligne   (int)       : numéro de ligne (commence à 0)
        colonne (str)       : nom de la colonne (correspond à l'en-tête Excel)

    Retour :
        Valeur de la cellule (str), None en cas d'erreur

    Exemple :
        valeur = lire_cellule(df, 0, "FirstName")   # lit la 1ère ligne, colonne "FirstName"
    """
    try:
        valeur = df.at[ligne, colonne]
        logger.info("Lecture cellule [ligne=%d, colonne=%s] : '%s'", ligne, colonne, valeur)
        return valeur

    except KeyError:
        logger.error("Colonne introuvable : '%s'", colonne)
        return None

    except Exception as e:
        logger.error("Erreur lecture cellule [ligne=%d, colonne=%s] : %s", ligne, colonne, e)
        return None


def lire_ligne(df: pd.DataFrame, ligne: int) -> dict:
    """
    Lit toute une ligne et retourne ses valeurs sous forme de dictionnaire.

    Paramètres :
        df    (DataFrame) : DataFrame chargé avec ouvrir_excel()
        ligne (int)       : numéro de ligne (commence à 0)

    Retour :
        Dictionnaire {nom_colonne: valeur}, None en cas d'erreur

    Exemple :
        data = lire_ligne(df, 0)
        # → {"FirstName": "John", "LastName": "Doe", "Email": "john@acme.com", ...}
    """
    try:
        data = df.iloc[ligne].to_dict()
        logger.info("Lecture ligne %d : %s", ligne, data)
        return data

    except IndexError:
        logger.error("Ligne introuvable : %d (le fichier contient %d lignes)", ligne, len(df))
        return None

    except Exception as e:
        logger.error("Erreur lecture ligne %d : %s", ligne, e)
        return None


def ecrire_cellule(df: pd.DataFrame, ligne: int, colonne: str, valeur: str) -> bool:
    """
    Modifie la valeur d'une cellule dans le DataFrame.
    ⚠️ La modification est en mémoire uniquement — appelle sauvegarder_excel() pour persister.

    Paramètres :
        df      (DataFrame) : DataFrame chargé avec ouvrir_excel()
        ligne   (int)       : numéro de ligne (commence à 0)
        colonne (str)       : nom de la colonne (correspond à l'en-tête Excel)
        valeur  (str)       : nouvelle valeur à écrire

    Retour :
        True si succès, False en cas d'erreur

    Exemple :
        ecrire_cellule(df, 0, "Statut", "Traité")
    """
    try:
        ancienne_valeur = df.at[ligne, colonne]
        df.at[ligne, colonne] = valeur
        logger.info("Écriture cellule [ligne=%d, colonne=%s] : '%s' → '%s'",
                    ligne, colonne, ancienne_valeur, valeur)
        return True

    except KeyError:
        logger.error("Colonne introuvable : '%s'", colonne)
        return False

    except Exception as e:
        logger.error("Erreur écriture cellule [ligne=%d, colonne=%s] : %s", ligne, colonne, e)
        return False


def sauvegarder_excel(df: pd.DataFrame, chemin_fichier: str, feuille: str = "Sheet1") -> bool:
    """
    Sauvegarde le DataFrame dans le fichier Excel.
    Écrase le contenu de l'onglet spécifié.

    Paramètres :
        df             (DataFrame) : DataFrame modifié à sauvegarder
        chemin_fichier (str)       : chemin complet vers le fichier .xlsx
        feuille        (str)       : nom de l'onglet cible (défaut : "Sheet1")

    Retour :
        True si succès, False en cas d'erreur

    Exemple :
        sauvegarder_excel(df, r"C:\data\contacts.xlsx", feuille="Contacts")
    """
    try:
        with pd.ExcelWriter(chemin_fichier, engine="openpyxl", mode="w") as writer:
            df.to_excel(writer, sheet_name=feuille, index=False)

        logger.info("Fichier sauvegardé : %s | Feuille : %s", chemin_fichier, feuille)
        return True

    except PermissionError:
        logger.error("Fichier ouvert dans Excel, impossible de sauvegarder : %s", chemin_fichier)
        return False

    except Exception as e:
        logger.error("Erreur lors de la sauvegarde (%s) : %s", chemin_fichier, e)
        return False