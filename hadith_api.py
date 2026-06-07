# hadith_api.py — Récupération d'un hadith en FRANÇAIS via l'API fawazahmed0
# Source : https://github.com/fawazahmed0/hadith-api (gratuit, sans clé)
# On utilise UNIQUEMENT Bukhari et Muslim (recueils intégralement authentiques/sahih).
import random
import logging
import requests
 
logger = logging.getLogger(__name__)
 
 
class HadithAPI:
    def __init__(self, allowed_books=None, status="Sahih"):
        # Éditions FRANÇAISES de Bukhari et Muslim
        self.editions = ["fra-bukhari", "fra-muslim"]
        # Nb approximatif de hadiths par recueil (pour tirer un numéro au hasard)
        # Bukhari ~7563, Muslim ~7563 dans cette numérotation ; on reste prudent.
        self.max_num = {"fra-bukhari": 7000, "fra-muslim": 7000}
        self.base = "https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1/editions"
        self.session = requests.Session()
 
    def _book_label(self, edition):
        return {
            "fra-bukhari": "Sahih Al-Bukhari",
            "fra-muslim": "Sahih Muslim",
        }.get(edition, edition)
 
    def get_random_hadith(self, max_tries=6):
        """
        Tire un hadith FR au hasard dans Bukhari ou Muslim.
        Réessaie si le numéro tiré n'existe pas (trous dans la numérotation).
        """
        for attempt in range(max_tries):
            edition = random.choice(self.editions)
            num = random.randint(1, self.max_num[edition])
            url = f"{self.base}/{edition}/{num}.min.json"
 
            try:
                resp = self.session.get(url, timeout=30)
                if resp.status_code != 200:
                    # numéro inexistant → on retente
                    continue
                data = resp.json()
            except Exception as e:
                logger.warning(f"Essai {attempt+1} échoué ({url}) : {e}")
                continue
 
            # Structure attendue : {"hadiths":[{"hadithnumber":N,"text":"...","grades":[...]}], ...}
            # On gère liste OU objet unique, par robustesse.
            hadiths = data.get("hadiths", [])
            if isinstance(hadiths, list):
                if not hadiths:
                    continue
                h = hadiths[0]
            elif isinstance(hadiths, dict):
                h = hadiths
            else:
                logger.warning(f"Format inattendu pour 'hadiths' : {type(hadiths)}")
                continue
 
            text = (h.get("text") or "").strip()
            if not text:
                continue
 
            number = h.get("hadithnumber", num)
            grades = h.get("grades", [])
 
            logger.info(f"Hadith FR récupéré : {edition} n°{number}")
            return {
                "text_fr": text,
                "number": number,
                "book": self._book_label(edition),
                "grades": grades,
            }
 
        logger.error(f"Impossible de récupérer un hadith après {max_tries} essais.")
        return None
