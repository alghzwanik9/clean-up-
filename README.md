# WinStorageGuard (حارس التخزين ومحسن أداء نظام ويندوز)

**WinStorageGuard** هي أداة احترافية وشاملة للمطورين ومستخدمي Windows لتشخيص وتحليل وتطهير قرص النظام `C:\`، بالإضافة إلى تحسين أداء الجهاز ومكوناته (SSD, RAM, Network, Windows Health) بأمان تام دون المساس ببيئات العمل أو الأكواد البرمجية.

---

## 🚀 المميزات الرئيسية

### 1. إدارة وتطهير التخزين (Storage & Cache Optimizer):
- **التحليل السريع فائق الأداء (Multi-threaded Fast Analysis):** فحص أحجام المجلدات الضخمة ومجلدات النظام في ثوانٍ معدودة عبر محرك Robocopy الموازي.
- **تطهير كاش أدوات التطوير (Dev-Cache Purge):** تنظيف كاش أدوات البناء وحزم اللغات (Gradle, NPM, Pip, Poetry, Dart, Playwright) بأمان.
- **إصلاح وتصفير تحديثات ويندوز (Windows Update Reset):** إيقاف الخدمات المعلقة وتفريغ تنزيلات التحديثات التالفة `SoftwareDistribution\Download`.
- **تنظيف مكونات ويندوز العميقة (Deep WinSxS Cleanup):** تنظيف مخزن مكونات النظام عبر DISM واستعادة مساحات هائلة.
- **تطهير كاش التطبيقات والرسوميات (App & Shaders Cleanup):** تفريغ كاش `%TEMP%`، وتطبيقات سطح المكتب (Discord, Notion, VS Code, Cursor)، وكاش DirectX Shaders.

### 2. تحسين أداء واستقرار الجهاز (System & Performance Optimizer):
- **تحسين سرعة أقراص الـ SSD (SSD TRIM & Volume Optimization):** إعادة تهيئة خلايا التخزين (ReTrim) لتسريع عمليات القراءة والكتابة وإطالة عمر الـ SSD.
- **تفريغ كاش الشبكة والـ DNS (Network & DNS Flush):** تصفير كاشات DNS Resolver وNetBIOS وARP لتسريع استجابة التصفح وحل تعليق اتصالات الشبكة.
- **تفريغ الذاكرة المؤقتة (RAM Working Sets Trim):** إطلاق الذاكرة غير المستخدمة وتحفيز الـ Garbage Collection في النظام.
- **رصد برامج بدء التشغيل (Startup Impact Analyzer):** فحص سجل النظام (Registry) ومجلدات الإقلاع لاكتشاف البرامج التي تبطئ تشغيل الويندوز.
- **فحص وإصلاح ملفات النظام (System Health Check & SFC):** فحص سلامة ملفات ويندوز الأساسية ومخزن المكونات وإصلاح التالف منها تلقائياً.

---

## 📁 هيكلية المشروع

```
win-storage-guard/
├── engine/
│   ├── __init__.py
│   ├── analyzer.py       # محرك فحص وتحليل استهلاك القرص والكاشات
│   ├── cleaner.py        # محرك التنظيف الآمن للملفات والمجلدات
│   ├── optimizer.py      # محرك تحسين أداء الـ SSD، الشبكة، الرام، والـ Startup
│   ├── windows_update.py # تصفير وإصلاح خدمات وتنزيلات Windows Update
│   ├── scheduler.py      # إدارة جدولة التنظيف الدوري في مهام ويندوز
│   └── safety.py         # صمام الأمان والتحقق من المسارات المحمية
├── scripts/
│   ├── quick_clean.ps1      # تنظيف سريع فوري
│   ├── analyze_disk.ps1     # تحليل تفصيلي للقرص
│   ├── optimize_system.ps1  # تحسين أداء الجهاز الشامل (TRIM + DNS + RAM)
│   ├── system_health.ps1    # فحص وإصلاح ملفات النظام (SFC + DISM)
│   ├── cleanup_winsxs.ps1   # تنظيف عميق لمخزن مكونات ويندوز WinSxS
│   ├── reset_windows_update.ps1 # تصفير كاش التحديثات
│   ├── setup_automation.ps1 # تفعيل الأتمتة الأسبوعية
│   └── remove_automation.ps1# إلغاء الأتمتة
├── storage_guard.py         # الواجهة التفاعلية الرئيسية عبر سطر الأوامر (CLI)
├── run.bat                  # مشغل تفاعلي سريع بنقرة واحدة (Menu Launcher)
└── requirements.txt
```

---

## 🛠️ كيفية الاستخدام

### 1. عبر مشغل القائمة السريعة (بنقرة واحدة):
شغّل الملف [run.bat](file:///d:/DEV/ACTIVE/win-storage-guard/run.bat) لاختيار أي وظيفة من القائمة التفاعلية مباشرة.

### 2. عبر Python CLI:
```bash
# تشغيل الفحص والتحليل
python storage_guard.py --analyze

# تشغيل التنظيف الآمن الشامل
python storage_guard.py --clean

# تشغيل تحسين أداء النظام الكامل (TRIM + Network + Memory)
python storage_guard.py --optimize

# فحص البرامج التي تبطئ بدء التشغيل
python storage_guard.py --startup

# فحص سلامة ملفات نظام ويندوز (SFC)
python storage_guard.py --health

# تفريغ كاش الـ DNS والشبكة
python storage_guard.py --flush-dns

# تحسين وتنشيط خلايا الـ SSD (TRIM)
python storage_guard.py --trim

# فحص حالة الأتمتة المجدولة
python storage_guard.py --schedule-status
```

### 3. عبر PowerShell مباشرة:
```powershell
# تحسين أداء النظام الشامل (صلاحيات المسؤول)
.\scripts\optimize_system.ps1

# فحص وإصلاح ملفات النظام (SFC / DISM)
.\scripts\system_health.ps1

# التنظيف السريع
.\scripts\quick_clean.ps1
```
