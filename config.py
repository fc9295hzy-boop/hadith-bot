# config.py — Configuration du Bot Hadith
import os

# ── Telegram ──
# À définir en variables d'environnement Railway (NE PAS coder en dur) :
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID   = os.environ.get("TELEGRAM_CHAT_ID", "")   # @canal public ou ID

# ── Hadith API (hadithapi.com) ──
HADITH_API_KEY  = os.environ.get("HADITH_API_KEY", "")
HADITH_API_URL  = "https://hadithapi.com/api/hadiths"

# Recueils autorisés (sahih uniquement, les plus rigoureux)
ALLOWED_BOOKS = ["sahih-bukhari", "sahih-muslim"]

# Grade exigé — sécurité authenticité : on ne diffuse QUE du sahih
HADITH_STATUS = "Sahih"

# ── Planification ──
SEND_HOUR   = 8     # heure d'envoi (24h)
SEND_MINUTE = 0
TIMEZONE    = "Europe/Paris"
