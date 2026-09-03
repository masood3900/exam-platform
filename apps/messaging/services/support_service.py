class SupportService:
    """سرویس پشتیبانی"""

    FAQ = {
        "ثبت نام": "برای ثبت‌نام از منوی بالا روی «ثبت‌نام» کلیک کنید.",
        "پرداخت": "برای پرداخت، کارت به کارت کنید و رسید را در بخش پرداخت ارسال کنید.",
        "آزمون": "برای مشاهده آزمون‌ها از منوی «آزمون‌ها» استفاده کنید.",
        "هزینه": "هزینه هر آزمون در صفحه همان آزمون نمایش داده شده است.",
        "سلام": "سلام! 🌹 چطور می‌تونم کمکتون کنم؟",
    }

    @staticmethod
    def get_faq_answer(text):
        """چک کن سوال متداول هست"""
        text = text.lower()
        for keyword, answer in SupportService.FAQ.items():
            if keyword.lower() in text:
                return answer
        return None
