# دستور عمل ساخت و به‌روزرسانی

## پیش‌نیازها

```bash
pip install numpy shapely pyproj osmium opencv-python-headless scikit-image networkx scipy pyshp potracer pillow
# Node 18+ و pnpm (npm i -g pnpm)
# برای اسکرین‌شات: playwright با Chromium
```

همه‌ی اسکریپت‌ها با یک «پوشه‌ی کاری» کار می‌کنند که مسیرش در متغیر `TEHRANMAP_WORK` است (پیش‌فرض `./work`). این پوشه را `tools/setup_work.sh` از روی داده‌های مخزن می‌سازد و در git نیست.

```bash
bash tools/setup_work.sh            # یک بار
export TEHRANMAP_WORK=$PWD/work
```

## ساخت کامل (رایج‌ترین کار)

```bash
bash tools/build.sh
```

خروجی‌ها:
- `dist/payamgostar-support-map.html` (نسخه‌ی مستقل)
- `dist/wordpress/payamgostar-support-map-X.Y.Z.zip`

این روند در مخزن آزمایش شد و فایل خروجی بایت‌به‌بایت هم‌اندازه‌ی نسخه‌ی منتشرشده بود.

## سناریو ۱: تغییر ظاهر یا متن‌ها

1. فقط `src/template.html` را ویرایش کنید. CSS در بلوک دوم `<style>` است، HTML باکس‌ها بعد از آن، و منطق نقشه در `<script>` آخر.
2. `bash tools/build.sh`
3. نتیجه را با مرورگر باز کنید یا اسکرین‌شات بگیرید (`scripts/screenshots/shot4.js`).

> فایل‌های `app/src/mapEngine.ts`، `map.css` و `App.tsx` ساختگی‌اند و با هر ساخت از روی template بازنویسی می‌شوند. آن‌ها را مستقیم ویرایش نکنید.

## سناریو ۲: کشیدن دوباره‌ی مرز زرد (مثل نسخه‌ی ۵)

1. از نقشه‌ی فعلی اسکرین‌شات بگیرید و خط جدید را با **آبی پررنگ خالص** بکشید. سر و ته خط باید روی خط زرد فعلی باشد. اسم چند شهر باید در تصویر دیده شود.
2. تصویر را در `work/v5/draw.png` بگذارید.
3. در `scripts/v5-redraw/v5_georef.py` جای وسط اسم شهرها را در تصویر جدید بنویسید (لیست `cp`، به پیکسل) و اجرا کنید. خطای هر نقطه باید زیر ۲ پیکسل باشد.
4. اجرا کنید:
   ```bash
   python3 scripts/v5-redraw/v5_blue.py     # استخراج خط → v5/blue.json و blue_check.png
   python3 scripts/v5-redraw/v5_build.py    # صاف کردن + چسباندن به جاده و مرز منطقه + بستن چندضلعی
   python3 scripts/v5-redraw/v5_check.py    # تصویر مقایسه: v5/new_check.png
   ```
5. `new_check.png` را با چشم بررسی کنید: خط قرمز باید روی آبی یا روی جاده‌ی نزدیکش باشد.
6. `python3 scripts/v5-redraw/v5_apply.py` مرز جدید را در `work/data/geo.json` می‌نویسد و لایه‌ی شهرها را دوباره حساب می‌کند. اسم شهرهایی که لایه‌شان عوض می‌شود چاپ می‌شود. این فهرست را برای تأیید به واحد فروش بدهید. بعد فایل را به `data/geo.json` کپی کنید.
7. `bash tools/build.sh`

پارامترهای قابل تنظیم در `v5_build.py`:

| پارامتر | مقدار | اثر |
|---|---|---|
| `T` | ۳۲۰ متر | خط دستی تا این فاصله از جاده باشد تا به آن بچسبد |
| `MINRUN` | ۷۰۰ متر | قطعه‌های کوتاه‌تر جایگزین نمی‌شوند |
| زاویه‌ی هم‌جهتی | ۳۵ درجه برای جاده، ۴۰ درجه برای مرز منطقه | جلوی چسبیدن به جاده‌های عمود را می‌گیرد |
| طول مسیر جاده | حداکثر ۱٫۳۵ برابر قطعه‌ی دستی | جلوی دور زدن‌های بی‌جا را می‌گیرد |
| despike | ۱۴۵ درجه | حذف رأس‌های برگشتی در محل اتصال‌ها |

## سناریو ۳: به‌روزرسانی خیابان‌ها از OSM

```bash
python3 -I scripts/v2-v4-basemap/osm_extract.py data/osm/tehran-region.osm.pbf $TEHRANMAP_WORK/out2
gzip -9 -k -f $TEHRANMAP_WORK/out2/base.json $TEHRANMAP_WORK/out2/minor.json
cp $TEHRANMAP_WORK/out2/*.gz data/basemap/
bash tools/build.sh
```

کادر پوشش در خود اسکریپت (`W, S, E, N`) تعریف شده و باید با کادر فایل pbf یکی باشد.

## سناریو ۴: نسخه‌ی جدید افزونه‌ی وردپرس

1. `Version:` و `PGSM_VERSION` را در `dist/wordpress/payamgostar-support-map/payamgostar-support-map.php` و `Stable tag` و changelog را در `readme.txt` بالا ببرید.
2. `bash tools/build.sh`. فایل zip با شماره‌ی نسخه‌ی جدید ساخته می‌شود.
3. در وردپرس همان zip را دوباره بارگذاری کنید و گزینه‌ی جایگزینی را بزنید. تنظیمات حفظ می‌شود و نسخه در آدرس iframe کش را باطل می‌کند.

## بررسی‌ها پیش از تحویل

- [ ] فایل مستقل را مستقیم از دیسک (`file://`) باز کنید. خیابان‌ها باید بیایند و کنسول خطا نداشته باشد.
- [ ] پهنای دسکتاپ (۱۴۴۰) و موبایل (۴۰۰) را چک کنید: باکس‌ها روی کنترل‌های زوم نیفتند.
- [ ] موس را روی هر سه لایه ببرید و متن را چک کنید.
- [ ] چند جستجو امتحان کنید: «منطقه ۵»، «قدس»، «سعادت‌آباد».
- [ ] برای افزونه: `php -l` روی فایل‌ها و پیش‌نمایش در صفحه‌ی تنظیمات.
