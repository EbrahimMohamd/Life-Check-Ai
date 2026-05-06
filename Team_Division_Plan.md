# 👥 خطة تقسيم المشروع على الفريق (3 أعضاء)

## الفكرة الأساسية
كل عضو في الفريق أخذ موديل مرض واحد (سكري / قلب / رئة).
التقسيم التالي يوزع **باقي ملفات المشروع** (البنية التحتية، الشات بوت، الواجهة، قاعدة البيانات، إلخ) بشكل **عادل ومنطقي** بحيث كل شخص يشرح الملفات المرتبطة بتخصصه + جزء من الملفات المشتركة.

---

## 👤 العضو الأول — مسؤول موديل السكري (Diabetes)

### ملفات الموديل الخاصة به:
| الملف | المسار |
|---|---|
| `diabetes_model.pkl` | `app/models/` |
| `diabetes_features.pkl` | `app/models/` |
| `diabetes_model.py` | `app/models/` |
| `diabetes.py` | `app/routes/` |
| `diabetes_model.py` | `app/training_scripts/` |
| `diabetes_prediction_dataset.csv` | `app/data/` |

### ملفات المشروع المشتركة المسؤول عنها:
| الملف | المسار | السبب |
|---|---|---|
| `prediction_schema.py` | `app/schemas/` | مخططات البيانات (Pydantic) للتحقق من مدخلات الأمراض |
| `prediction_service.py` | `app/services/` | الخدمة المشتركة التي تربط الـ Routes بالموديلات |
| `forms.py` | `frontend/components/` | واجهة إدخال بيانات المريض (السكري + القلب) |
| `requirements.txt` | `/` (الجذر) | ملف المتطلبات والمكتبات |
| `run.py` | `/` (الجذر) | ملف تشغيل السيرفر |
| `Start_LifeCheck_AI.bat` | `/` (الجذر) | ملف التشغيل الآلي |

### إجمالي الملفات: 12 ملف

---

## 👤 العضو الثاني — مسؤول موديل القلب (Heart)

### ملفات الموديل الخاصة به:
| الملف | المسار |
|---|---|
| `heart_model.pkl` | `app/models/` |
| `heart_features.pkl` | `app/models/` |
| `heart_scaler.pkl` | `app/models/` |
| `heart_model.py` | `app/models/` |
| `heart.py` | `app/routes/` |
| `heart_model.py` | `app/training_scripts/` |
| `heart_2020_cleaned.csv` | `app/data/` |

### ملفات المشروع المشتركة المسؤول عنها:
| الملف | المسار | السبب |
|---|---|---|
| `database.py` | `app/db/` | إعداد قاعدة البيانات (SQLAlchemy + SQLite) |
| `models.py` | `app/db/` | جداول قاعدة البيانات (Users, Records) |
| `lifecheck.db` | `app/data/` | ملف قاعدة البيانات الفعلي |
| `auth.py` | `app/routes/` | مسارات تسجيل الدخول والتسجيل (JWT) |
| `auth.py` | `app/schemas/` | مخططات بيانات المصادقة |
| `patient.py` | `app/routes/` | مسارات إدارة حساب المريض (الإعدادات) |

### إجمالي الملفات: 13 ملف

---

## 👤 العضو الثالث — مسؤول موديل الرئة (Lung Cancer)

### ملفات الموديل الخاصة به:
| الملف | المسار |
|---|---|
| `lung_model.h5` | `app/models/` |
| `lung_model.py` | `app/models/` |
| `classes.txt` | `app/models/` |
| `lung.py` | `app/routes/` |
| `lungcancer_train.py` | `app/training_scripts/` |
| `lungcancer_finetune.py` | `app/training_scripts/` |
| `lung cancer dataset/` | `app/data/` |

### ملفات المشروع المشتركة المسؤول عنها:
| الملف | المسار | السبب |
|---|---|---|
| `config.py` | `app/chatbot_engine/` | إعدادات الشات بوت |
| `embeddings.py` | `app/chatbot_engine/` | تحويل النصوص لأرقام (Embeddings) |
| `extractor.py` | `app/chatbot_engine/` | استخراج الأعراض من النص |
| `generator.py` | `app/chatbot_engine/` | توليد الرد الطبي |
| `llm.py` | `app/chatbot_engine/` | الاتصال بالنموذج اللغوي |
| `matcher.py` | `app/chatbot_engine/` | مطابقة الأعراض |
| `rag.py` | `app/chatbot_engine/` | نظام الـ RAG |
| `safety.py` | `app/chatbot_engine/` | فلتر الأمان الطبي |
| `triage.py` | `app/chatbot_engine/` | تصنيف الأولوية الطبية |
| `utils_language.py` | `app/chatbot_engine/` | أدوات اللغة |
| `chat.py` | `app/routes/` | مسار الشات بوت في السيرفر |
| `chat_schema.py` | `app/schemas/` | مخطط بيانات الشات |
| `chat_service.py` | `app/services/` | خدمة الشات بوت |
| `conditions.json` | `app/data/` | قاعدة بيانات الأمراض |
| `medical_kb.json` | `app/data/` | قاعدة المعرفة الطبية |
| `symptom_lexicon.json` | `app/data/` | قاموس الأعراض |

### إجمالي الملفات: 23 ملف (لكن أغلبها ملفات صغيرة جداً < 2 KB)

---

## 🌐 ملفات الواجهة المشتركة (Frontend) — تقسيم بالتساوي

| الملف | المسار | المسؤول | السبب |
|---|---|---|---|
| `app.py` | `frontend/` | **العضو الأول (السكري)** | الملف الأساسي للواجهة والـ CSS والتنقل |
| `auth_ui.py` | `frontend/components/` | **العضو الثاني (القلب)** | واجهة تسجيل الدخول (مرتبط بالـ Auth) |
| `chat_ui.py` | `frontend/components/` | **العضو الثالث (الرئة)** | واجهة الشات بوت (مرتبط بالـ Chatbot Engine) |
| `settings.py` | `frontend/components/` | **العضو الثاني (القلب)** | واجهة الإعدادات (مرتبط بالـ Patient Routes) |
| `uploader.py` | `frontend/components/` | **العضو الثالث (الرئة)** | واجهة رفع الأشعة |
| `api_client.py` | `frontend/services/` | **العضو الأول (السكري)** | دوال الاتصال بالسيرفر |
| `pdf_generator.py` | `frontend/services/` | **العضو الأول (السكري)** | توليد التقارير الطبية |
| `main.py` | `app/` | **العضو الثاني (القلب)** | نقطة الدخول الرئيسية للسيرفر |
| `config.toml` | `.streamlit/` | **العضو الأول (السكري)** | إعدادات Streamlit |
| `logo.png` | `frontend/static/` | **العضو الثالث (الرئة)** | الصور والأصول |
| `bot_icon.png` | `frontend/assets/` | **العضو الثالث (الرئة)** | أيقونة الشات بوت |

---

## 📊 ملخص التقسيم النهائي

| العضو | الموديل | عدد الملفات الكلي | المسؤوليات الإضافية |
|---|---|---|---|
| **الأول** | السكري | ~15 ملف | الواجهة الرئيسية (`app.py`) + الـ API Client + التقارير (PDF) + ملف التشغيل |
| **الثاني** | القلب | ~17 ملف | قاعدة البيانات + المصادقة (JWT/Auth) + الإعدادات + نقطة الدخول (`main.py`) |
| **الثالث** | الرئة | ~28 ملف | الشات بوت بالكامل (10 ملفات) + واجهة رفع الأشعة + الأصول البصرية |

> **ملاحظة:** العضو الثالث (الرئة) أخذ عدد ملفات أكبر، لكنها ملفات **صغيرة جداً** (أغلب ملفات الشات بوت أقل من 2 كيلوبايت). بينما العضو الأول أخذ `app.py` وهو ملف ضخم (600 سطر)، والعضو الثاني أخذ نظام قاعدة البيانات + المصادقة وهو الأكثر تعقيداً. **التقسيم متوازن من حيث الجهد المطلوب.**
