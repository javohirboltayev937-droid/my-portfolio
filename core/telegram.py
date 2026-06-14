"""Telegram bot orqali xabar yuborish (qo'shimcha kutubxonasiz, urllib bilan)."""
import json
import urllib.parse
import urllib.request

from django.conf import settings


def send_telegram_message(text: str) -> bool:
    """Berilgan matnni sozlangan Telegram chatga yuboradi.
    Token yoki chat_id bo'lmasa yoki xato bo'lsa False qaytaradi (sayt to'xtab qolmaydi)."""
    token = getattr(settings, "TELEGRAM_BOT_TOKEN", "").strip().strip("'\"")
    raw_ids = getattr(settings, "TELEGRAM_CHAT_ID", "")
    # "8744146411", '6486995621' kabi xom qiymatlardan toza ID lar ajratib olamiz
    chat_ids = [c.strip().strip("'\"") for c in str(raw_ids).split(",")]
    chat_ids = [c for c in chat_ids if c]

    if not token or not chat_ids:
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    any_ok = False
    for chat_id in chat_ids:
        data = urllib.parse.urlencode({
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": "true",
        }).encode("utf-8")
        try:
            req = urllib.request.Request(url, data=data)
            with urllib.request.urlopen(req, timeout=10) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                if result.get("ok"):
                    any_ok = True
                else:
                    print(f"[Telegram] {chat_id} ga yuborilmadi: {result.get('description')}")
        except Exception as e:
            print(f"[Telegram] {chat_id} ga xatolik: {e}")
    return any_ok
