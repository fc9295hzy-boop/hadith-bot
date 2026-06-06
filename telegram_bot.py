# telegram_bot.py — Envoi du message formaté sur Telegram
import logging
import requests
 
logger = logging.getLogger(__name__)
 
 
class TelegramBot:
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{token}/sendMessage"
 
    def format_message(self, hadith):
        text = hadith.get("text_en", "").strip()
        narrator = hadith.get("narrator", "").strip()
        number = hadith.get("number", "")
        book = hadith.get("book", "")
 
        if narrator.lower().startswith("narrated"):
            narrator = narrator[len("narrated"):].strip(" :")
 
        lines = []
        lines.append("🕌 *Rappel du jour* 📖")
        lines.append("")
        lines.append("*Hadith du jour*")
        lines.append("")
        lines.append(f"_{text}_")
        lines.append("")
        lines.append(f"📚 *Source :* {book} — Hadith n°{number}")
        if narrator:
            lines.append(f"🔖 *Rapporté par :* {narrator}")
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
            # On affiche TOUJOURS la réponse détaillée de Telegram
            if resp.status_code != 200:
                logger.error(f"Telegram a refusé (HTTP {resp.status_code}). "
                             f"chat_id utilisé : '{self.chat_id}'. "
                             f"Réponse détaillée : {resp.text}")
                return False
            logger.info("✅ Hadith envoyé sur Telegram")
            return True
        except Exception as e:
            logger.error(f"Erreur réseau envoi Telegram : {e}")
            return False
