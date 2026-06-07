# telegram_bot.py — Envoi du hadith (français) sur Telegram
import logging
import requests
 
logger = logging.getLogger(__name__)
 
 
class TelegramBot:
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{token}/sendMessage"
 
    def format_message(self, hadith):
        text = hadith.get("text_fr", "").strip()
        number = hadith.get("number", "")
        book = hadith.get("book", "")
 
        lines = []
        lines.append("🕌 *Rappel du jour* 📖")
        lines.append("")
        lines.append(text)
        lines.append("")
        lines.append(f"📚 *Source :* {book} — n°{number}")
        lines.append("")
        lines.append("━━━━━━━━━━━━━━━")
        lines.append("🤲 _Qu'Allah nous guide sur le droit chemin_")
        return "\n".join(lines)
 
    def send_hadith(self, hadith):
        message = self.format_message(hadith)
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True,
        }
        try:
            resp = requests.post(self.api_url, json=payload, timeout=30)
            if resp.status_code != 200:
                logger.error(f"Telegram a refusé (HTTP {resp.status_code}). "
                             f"chat_id : '{self.chat_id}'. Réponse : {resp.text}")
                return False
            logger.info("✅ Hadith envoyé sur Telegram")
            return True
        except Exception as e:
            logger.error(f"Erreur réseau envoi Telegram : {e}")
            return False
