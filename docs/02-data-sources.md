# منابع داده و مجوزها

| داده | فایل در مخزن | منبع | توضیح |
|---|---|---|---|
| مرز مناطق ۲۲گانه | `data/districts/tehran-22-districts-shp.zip` | شیپ‌فایلی که پدرام فرستاد (لایه‌ی شهرداری تهران) | UTM 39N. فیلدها: Region_ID، pop، Area و… (آمار جمعیت در نسخه‌ی نهایی نمایش داده نمی‌شود) |
| مرز زرد و مناطق، به‌صورت آماده | `data/geo.json` | خروجی اسکریپت‌ها | شامل `districts`، `city`، `outer` (مرز زرد نسخه‌ی ۵)، `places` (شهرهای اطراف با لایه‌ی محاسبه‌شده) |
| مرز زرد قبلی | `data/legacy/geo.v4.json` | نسخه‌ی ۱ تا ۴ | برای مقایسه یا برگشت |
| داده‌ی خیابان‌ها | `data/osm/tehran-region.osm.pbf` | برش سفارشی BBBike از OpenStreetMap، کادر 50.95,35.42 تا 51.85,35.90 | © OpenStreetMap contributors، مجوز ODbL |
| نقشه‌ی پایه‌ی آماده | `data/basemap/base.json.gz`، `minor.json.gz` | خروجی `osm_extract.py` | فرمت: مختصات دلتا-کد با دقت ۱e-5 درجه |
| تطبیق تصاویر | `data/georef/*.json` | خروجی اسکریپت‌ها | `v5-blue-line.json` خط دستی نسخه‌ی ۵ را هم به پیکسل و هم به مختصات دارد |
| لوگو | `data/logo/payamgostar-logo.svg`، `images/brand/*.png` | فایل‌های لوگوی پیام‌گستر | وکتورشده با potrace |

## داده‌هایی که امتحان شدند ولی کنار رفتند

- **Natural Earth 10m roads:** خیلی کلی بود (۱۶ جاده برای کل منطقه). فقط در نسخه‌ی ۱ امتحان شد.
- **فایل آماده‌ی Tehran.osm.pbf از BBBike:** فقط مرکز تهران را داشت (51.27 تا 51.55 شرقی). نسخه‌ی ۲ با آن ساخته شد و بعد با برش سفارشی جایگزین شد.
- **نقشه‌ی «کتاب اول»** (`images/inputs/01-avval-22-districts-reference.png`): فقط مرجع بصری بود. به‌خاطر واترمارک و حق نشر در نقشه استفاده نشد.

## ساخت دوباره‌ی برش OSM

```
https://extract.bbbike.org/?sw_lng=50.95&sw_lat=35.42&ne_lng=51.85&ne_lat=35.90&format=osm.pbf&city=Tehran-Support
```

فایل دانلودی را به‌جای `data/osm/tehran-region.osm.pbf` بگذارید و مرحله‌ی «به‌روزرسانی خیابان‌ها» را در [03-build-runbook.md](03-build-runbook.md) اجرا کنید.
