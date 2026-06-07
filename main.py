#!/usr/bin/env python3
# main.py — Bot Hadith : un hadith authentique en FRANÇAIS chaque jour à 8h
import logging
import sys
 
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s : %(message)s",
)
logger = logging.getLogger(__name__)
 
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone
 
from config import (
    TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID,
    SEND_HOUR, SEND_MINUTE, TIMEZONE,
)
from hadith_api import HadithAPI
from telegram_bot import TelegramBot
 
 
def send_daily_hadith(hadith_api, telegram_bot):
    logger.info("Récupération du hadith du jour...")
    hadith = hadith_api.get_random_hadith()
    if not hadith:
        logger.error("Impossible de récupérer un hadith. Réessai au prochain cycle.")
        return
    telegram_bot.send_hadith(hadith)
 
 
def main():
    logger.info("══════════════════════════════════════════")
    logger.info("  Bot Hadith (FR) — Démarrage")
    logger.info("══════════════════════════════════════════")
 
    missing = [n for n, v in [
        ("TELEGRAM_BOT_TOKEN", TELEGRAM_BOT_TOKEN),
        ("TELEGRAM_CHAT_ID", TELEGRAM_CHAT_ID),
    ] if not v]
    if missing:
        logger.error(f"Variables manquantes : {', '.join(missing)}.")
        sys.exit(1)
 
    hadith_api = HadithAPI()
    telegram_bot = TelegramBot(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
 
    logger.info("Envoi d'un hadith de test au démarrage...")
    send_daily_hadith(hadith_api, telegram_bot)
 
    tz = timezone(TIMEZONE)
    scheduler = BlockingScheduler(timezone=tz)
    scheduler.add_job(
        send_daily_hadith,
        CronTrigger(hour=SEND_HOUR, minute=SEND_MINUTE, timezone=tz),
        args=[hadith_api, telegram_bot],
    )
    logger.info(f"✅ Planifié : chaque jour à {SEND_HOUR:02d}h{SEND_MINUTE:02d} ({TIMEZONE})")
    logger.info("Bot en attente...")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Arrêt du bot.")
 
 
if __name__ == "__main__":
    main()
