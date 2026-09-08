# WinStorageGuard (حارس التخزين الذكي لنظام ويندوز)

**WinStorageGuard** هي أداة متخصصة ومصممة للمطورين والمهندسين لتشخيص وتحليل وتطهير قرص النظام `C:\` في Windows بأمان تام ودون كسر أي بيئات عمل أو مسارات برمجية.

---

## 🚀 المميزات الرئيسية

1. **التحليل السريع فائق الأداء (Multi-threaded Fast Analysis):**
   - استخدام محرك Win32 Robocopy الموازي لفحص أحجام المجلدات الضخمة ومجلدات النظام في ثوانٍ معدودة.
2. **تطهير كاش أدوات التطوير (Dev-Cache Purge):**
   - تنظيف كاش أدوات البناء وحزم اللغات (Gradle, NPM, Pip, Poetry, Dart, Playwright) دون المساس بمسارات بايثون أو الـ PATH.
3. **إصلاح وتصفير تحديثات ويندوز (Windows Update Reset):**
   - إيقاف خدمات `wuauserv` و `bits` وفك قفل التنزيلات المعطوبة وتفريغ `SoftwareDistribution\Download` لحل خطأ "نفاد المساحة" أثناء التحديثات.
4. **تطهير كاش التطبيقات وسطح المكتب (App & Temp Cleanup):**
   - تفريغ كاش `%TEMP%`، كاش برامج التواصل والأدوات (Discord, Notion, VS Code VSIX caches)، وكاش معالجة الرسوميات (DirectX Shaders).
5. **طبقة الحماية القصوى (Zero-Risk Safety Layer):**
   - قائمة بيضاء صارمة للمجلدات المسموح بتنظيفها، مع منع قطعي للمساس بالأكواد المصدرية، المستودعات، أو قواعد البيانات.

---

## 📁 هيكلية المشروع

```
win-storage-guard/
├── engine/
│   ├── __init__.py
│   ├── analyzer.py       # محرك فحص وتحليل استهلاك القرص
│   ├── cleaner.py        # محرك التنظيف الآمن للكاش والتطبيقات
│   ├── windows_update.py # وحدة إدارة وتصفير خدمات وكاش التحديثات
│   └── safety.py         # صمام الأمان والتحقق من المسارات المحمية
├── scripts/
│   ├── quick_clean.ps1   # تشغيل سريع عبر PowerShell
│   ├── analyze_disk.ps1  # فحص تفصيلي للمساحة
│   └── reset_windows_update.ps1
├── storage_guard.py      # الواجهة التفاعلية الرئيسية (CLI / TUI)
├── run.bat               # مشغل سريع بنقرة واحدة
└── requirements.txt
```

---

## 🛠️ كيفية الاستخدام

### 1. عبر Python CLI:
```bash
# تشغيل الفحص والتحليل
python storage_guard.py --analyze

# تشغيل التنظيف الآمن الشامل
python storage_guard.py --clean

# إصلاح كاش تحديثات ويندوز العالقة
python storage_guard.py --reset-wu
```

### 2. عبر PowerShell مباشرة:
```powershell
# تشغيل التنظيف السريع
.\scripts\quick_clean.ps1

# تحليل القرص C
.\scripts\analyze_disk.ps1
```

### 3. بنقرة واحدة:
تشغيل الملف `run.bat`.
