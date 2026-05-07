# هنستخدم بايثون 3.9 (تقدر تغيرها لنسختك)
FROM python:3.10-slim

# بنحدد مسار الشغل
WORKDIR /code

# بننسخ ملف المكتبات الأول
COPY ./requirements.txt /code/requirements.txt

# بنسطب المكتبات
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# بننسخ باقي ملفات المشروع (الكود والموديل)
COPY . .

# Hugging Face بتطلب إن السيرفر يشتغل على بورت 7860
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]