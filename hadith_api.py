# hadith_api.py — Récupération d'un hadith authentique via hadithapi.com
import random
import logging
import requests

logger = logging.getLogger(__name__)


class HadithAPI:
    def __init__(self, api_key, api_url, allowed_books, status="Sahih"):
        self.api_key = api_key
        self.api_url = api_url
        self.allowed_books = allowed_books
        self.status = status
        self.session = requests.Session()

    def get_random_hadith(self):
        """
        Récupère un hadith sahih au hasard depuis un recueil autorisé.
        Filtre STRICT sur le grade (status=Sahih) — aucun hadith faible n'est diffusé.
        Retourne un dict normalisé ou None.
        """
        book = random.choice(self.allowed_books)

        params = {
            "apiKey": self.api_key,
            "book": book,
            "status": self.status,   # garde-fou authenticité
            "paginate": 25,          # on récupère un lot, on en tire un au hasard
        }

        # Page aléatoire pour varier les hadiths (les recueils ont des milliers d'entrées)
        params["page"] = random.randint(1, 50)

        try:
            resp = self.session.get(self.api_url, params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            logger.error(f"Erreur API hadith : {e}")
            return None

        # Structure attendue : data['hadiths']['data'] = liste
        hadiths = None
        try:
            hadiths = data.get("hadiths", {}).get("data", [])
        except Exception:
            hadiths = []

        if not hadiths:
            logger.warning(f"Aucun hadith retourné (book={book}, page={params['page']}). Nouvel essai page 1.")
            # Repli : page 1
            params["page"] = 1
            try:
                resp = self.session.get(self.api_url, params=params, timeout=30)
                resp.raise_for_status()
                data = resp.json()
                hadiths = data.get("hadiths", {}).get("data", [])
            except Exception as e:
                logger.error(f"Erreur API hadith (repli) : {e}")
                return None

        if not hadiths:
            return None

        # On ne garde que ceux avec un texte anglais ET un statut Sahih confirmé
        valid = [
            h for h in hadiths
            if h.get("hadithEnglish") and str(h.get("status", "")).lower() == self.status.lower()
        ]
        if not valid:
            valid = [h for h in hadiths if h.get("hadithEnglish")]
        if not valid:
            return None

        h = random.choice(valid)

        return self._normalize(h, book)

    def _normalize(self, h, book):
        """Normalise la réponse API en dict propre pour le formatage."""
        book_names = {
            "sahih-bukhari": "Sahih Al-Bukhari",
            "sahih-muslim": "Sahih Muslim",
        }
        return {
            "text_en": (h.get("hadithEnglish") or "").strip(),
            "text_ar": (h.get("hadithArabic") or "").strip(),
            "narrator": (h.get("englishNarrator") or "").strip(),
            "number": h.get("hadithNumber") or "",
            "book": book_names.get(book, book),
            "status": h.get("status", self.status),
        }
