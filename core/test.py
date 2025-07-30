import os
import sys
import django
from django.urls import reverse, get_resolver

# 1. Django settings modulini ko'rsat
# Agar papkang nomi boshqa bo‘lsa, masalan `myproject.settings`, shu yerda almashtir
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "otz_group.settings")

# 2. Django ilovasini ishga tushirish
sys.path.append(".")
django.setup()

print("=== URL Names Checker ===\n")

# 3. Barcha URL nomlarini chiqarish
resolver = get_resolver()
all_url_names = [name for name in resolver.reverse_dict.keys() if isinstance(name, str)]
print(f"Topilgan URL nomlari ({len(all_url_names)} ta):")
for name in sorted(all_url_names):
    print(" -", name)

# 4. Loglarda uchrayotgan URL larni tekshirish
urls_to_check = ["auth.user", "make_messages", "books"]

print("\n=== Yo‘q bo‘lishi mumkin bo‘lgan URL lar ===")
for url_name in urls_to_check:
    try:
        reverse(url_name)
        print(f"[OK] {url_name}")
    except Exception as e:
        print(f"[X] {url_name} -> {str(e)}")
