---
name: tehran-support-map
description: Update or rebuild PayamGostar's Tehran on-site support coverage map (green 22 districts / yellow travel-cost ring / outside needs approval) from the TehranMap repo — redraw the yellow boundary from a hand-drawn screenshot, refresh OSM streets, restyle, and ship the standalone HTML and WordPress plugin.
---

# نقشه محدوده پشتیبانی پیام‌گستر

این اسکیل برای وقتی است که پدرام بخواهد نقشه‌ی محدوده‌ی پشتیبانی را تغییر دهد. همه‌چیز در مخزن `pedramharmonica-star/TehranMap` است. اول آن را clone کنید و `README.md` و `docs/03-build-runbook.md` را بخوانید.

## قواعد ثابت (عوض نکنید مگر کاربر بخواهد)

- **سه لایه:**
  - سبز `#15936A`: «پشتیبانی حضوری»، داخل مناطق ۲۲گانه.
  - زرد `#F5B800`: «پشتیبانی حضوری همراه با هزینه ایاب و ذهاب»، تا خط زرد.
  - هاشور سنگ‌لوح: «نیازمند تأیید فروشنده، با هزینه‌ی ایاب و ذهاب و حق مأموریت».
- **مرز زرد مهم‌ترین عنصر نقشه است:** پررنگ، متحرک و همیشه دیده‌شدنی.
- **متن روی موس** برای هر لایه همان جمله‌های بالاست.
- **جمعیت و آمار نمایش داده نمی‌شود.**
- **هویت پیام‌گستر:** نارنجی `#F26122`، زغالی `#1C1F23` و لوگوی `data/logo/payamgostar-logo.svg`. فونت بدنه وزیرمتن است و جای یکان بخ آماده است (با رسیدن فایل فونت).
- **نقشه باید بیرون از Claude و بدون اینترنت هم کار کند.** داده‌ها داخل HTML هستند. هیچ تایل یا fetch بیرونی اضافه نکنید.
- **پاسخ‌ها کاملاً فارسی.** کاربر نسخه‌ی قابل‌تست را مرحله‌به‌مرحله می‌خواهد.

## منبع حقیقت

- **ظاهر و منطق:** فقط `src/template.html`. فایل‌های `app/src/*` ساختگی‌اند.
- **مرزها و شهرها:** فقط `data/geo.json`.
- **خیابان‌ها:** `data/osm/tehran-region.osm.pbf` → `data/basemap/*.json.gz`
- **ساخت:** `bash tools/build.sh` → `dist/payamgostar-support-map.html` و zip وردپرس.

## کارهای رایج

### کاربر مرز زرد را دوباره کشیده است
1. ورودی باید اسکرین‌شات از خود نقشه با خط آبی پررنگ باشد، با سر و ته روی خط زرد فعلی. اگر روی گوگل‌مپ کشیده شده، از روش نسخه‌ی ۱ استفاده کنید (`scripts/v1-initial/georef.py` با برچسب شهرهای گوگل).
2. `bash tools/setup_work.sh`، بعد تصویر را در `work/v5/draw.png` بگذارید.
3. در `v5_georef.py` جای وسط اسم‌ها را بنویسید. خطای هر نقطه باید زیر ۲ پیکسل باشد.
4. `v5_blue.py` و بعد `v5_build.py` و بعد `v5_check.py` را اجرا کنید. `new_check.png` را **حتماً نگاه کنید**.
5. `v5_apply.py` را اجرا کنید. شهرهایی که لایه‌شان عوض شد را به کاربر بگویید تا تأیید کند.
6. `tools/build.sh` را اجرا کنید، اسکرین‌شات بگیرید و فایل HTML و zip را تحویل دهید.

### به‌روزرسانی خیابان‌ها
از BBBike برش سفارشی بگیرید (لینک در `docs/02-data-sources.md`)، بعد `osm_extract.py`، gzip و `build.sh`.

### تغییر ظاهر
`src/template.html` را ویرایش کنید، بعد `build.sh`. پیش از تحویل یک اسکرین‌شات در دسکتاپ (۱۴۴۰) و موبایل (۴۰۰) بگیرید.

### نسخه‌ی جدید افزونه‌ی وردپرس
نسخه را در `payamgostar-support-map.php` و `readme.txt` بالا ببرید، بعد `build.sh`.

## دام‌ها (جزئیات در docs/04-lessons-and-errors.md)
- **رندرر pane:** لایه با `pane` سفارشی رندرر خودش را دارد. برای `<defs>` از `layer.getElement().ownerSVGElement` استفاده کنید.
- **انیمیشن و hover:** انیمیشن با `fill-mode: both` روی ویژگی‌ای که hover هم عوض می‌کند، hover را از کار می‌اندازد.
- **html-inline:** با لینک‌های بیرونی و `crossorigin` بی‌مقدار می‌شکند. فونت را در `finalize.py` اضافه کنید.
- **شهر داخل مرز:** بعد از هر simplify دوباره با شهر اجتماع بگیرید تا شهر کامل داخل مرز زرد بماند.
- **تست بیرون از Claude:** همیشه فایل مستقل را از `file://` تست کنید.
