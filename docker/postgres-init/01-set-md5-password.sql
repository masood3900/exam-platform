-- تنظیم پسورد با md5 از ابتدا
-- این فایل موقع اولین ساخت Volume اجرا می‌شه
SET password_encryption = 'md5';
ALTER USER postgres WITH PASSWORD 'postgres';
