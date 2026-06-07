# config.py — Configuration du Bot Hadith (français)
import os
 
# ── Telegram (variables Railway) ──
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID   = os.environ.get("TELEGRAM_CHAT_ID", "")
 
# ── Planification ──
SEND_HOUR   = 8
SEND_MINUTE = 0
TIMEZONE    = "Europe/Paris"
 
