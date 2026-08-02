class ProfileService:

    @staticmethod
    def completion(user):

        profile = user.profile

        fields = {
            "نام": bool(user.first_name),
            "نام خانوادگی": bool(user.last_name),
            "ایمیل": bool(user.email),
            "کد ملی": bool(profile.national_code),
            "موبایل": bool(profile.phone),
            "تاریخ تولد": bool(profile.birth_date),
            "جنسیت": bool(profile.gender),
            "تصویر": bool(profile.avatar),
        }

        completed = sum(fields.values())
        total = len(fields)

        percent = int((completed / total) * 100)

        return {
            "percent": percent,
            "completed": completed,
            "total": total,
            "fields": fields,
        }