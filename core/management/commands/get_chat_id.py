"""Telegram chat ID ni aniqlash uchun buyruq.

Ishlatish:
  1) .env ga TELEGRAM_BOT_TOKEN ni qo'ying
  2) Telegramda botingizga /start (yoki istalgan xabar) yozing
  3) python manage.py get_chat_id
Chiqqan ID ni .env dagi TELEGRAM_CHAT_ID ga yozing.
"""
import json
import urllib.request

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Botga yozilgan oxirgi xabardan chat ID ni aniqlaydi"

    def handle(self, *args, **options):
        token = getattr(settings, "TELEGRAM_BOT_TOKEN", "")
        if not token:
            self.stderr.write("❌ TELEGRAM_BOT_TOKEN topilmadi. Avval .env ga token qo'ying.")
            return

        url = f"https://api.telegram.org/bot{token}/getUpdates"
        try:
            with urllib.request.urlopen(url, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            self.stderr.write(f"❌ Xatolik: {e}")
            return

        if not data.get("ok"):
            self.stderr.write(f"❌ Telegram javobi: {data}")
            return

        updates = data.get("result", [])
        if not updates:
            self.stdout.write(
                "⚠️  Hech qanday xabar topilmadi.\n"
                "    Telegramda botingizni toping va unga /start yoki istalgan xabar yozing,\n"
                "    so'ng shu buyruqni qayta ishga tushiring."
            )
            return

        seen = {}
        for u in updates:
            msg = u.get("message") or u.get("edited_message") or {}
            chat = msg.get("chat", {})
            if chat.get("id") is not None:
                seen[chat["id"]] = chat.get("first_name") or chat.get("title") or ""

        self.stdout.write(self.style.SUCCESS("✅ Topilgan chatlar:"))
        for cid, name in seen.items():
            self.stdout.write(f"   CHAT_ID = {cid}   ({name})")
        self.stdout.write("\n👉 Kerakli ID ni .env dagi TELEGRAM_CHAT_ID ga yozing.")
