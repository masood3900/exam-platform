-- تنظیم کامل کاربر postgres
-- این فایل موقع ساخت اولیه Volume اجرا می‌شه
SET password_encryption = 'md5';
ALTER USER postgres WITH LOGIN SUPERUSER PASSWORD 'postgres';
