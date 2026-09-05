# 📝 Exam Platform

سامانه آزمون آنلاین و مدیریت آموزشی با جنگو

## ✨ امکانات

### 👥 داشبوردهای تخصصی
- **مدیر کل**: مدیریت کاربران، پرداخت‌ها، کدهای تخفیف
- **مدیر علمی**: مدیریت موضوع‌ها، آزمون‌ها، طراحان
- **طراح سوال**: طراحی و ارسال سوال برای تایید
- **دانشجو**: ثبت‌نام و شرکت در آزمون

## 🛠️ تکنولوژی‌ها
- Python 3.13 + Django
- PostgreSQL
- Docker
- Bootstrap 5

## 🚀 اجرا

git clone git@github.com:masood3900/exam-platform.git
cd exam-platform
docker compose up -d
docker compose exec web python manage.py migrate
docker compose exec web python manage.py runserver 0.0.0.0:8000
