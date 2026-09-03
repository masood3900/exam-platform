import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View

from apps.assessments.services.code_executor import CodeExecutor


class CodeExecuteView(LoginRequiredMixin, View):
    """اجرای کد"""

    def post(self, request):
        try:
            data = json.loads(request.body)
            code = data.get("code", "")
            language = data.get("language", "python")
            test_input = data.get("test_input", "")
            
            if not code.strip():
                return JsonResponse({"error": "کد خالی است"}, status=400)
            
            result = CodeExecutor.execute(code, language, test_input)
            return JsonResponse(result)
            
        except json.JSONDecodeError:
            return JsonResponse({"error": "داده نامعتبر"}, status=400)


class CodeCheckView(LoginRequiredMixin, View):
    """بررسی درستی کد تمرین با تست‌کیس"""

    def post(self, request, exercise_id):
        try:
            data = json.loads(request.body)
            code = data.get("code", "")
            
            from apps.assessments.models import Exercise, ExerciseAttempt, UserScore
            from apps.assessments.services.exercise_checker import ExerciseChecker
            
            exercise = Exercise.objects.get(id=exercise_id)
            
            # تعداد تلاش‌های قبلی
            attempts_count = ExerciseAttempt.objects.filter(
                user=request.user,
                exercise=exercise,
            ).count()
            
            # بررسی
            result = ExerciseChecker.check_exercise(
                code=code,
                exercise=exercise,
                language=exercise.language,
            )
            
            if result["is_correct"]:
                # محاسبه امتیاز با کسر
                score_earned = ExerciseChecker.calculate_score(exercise, attempts_count)
                
                # ثبت تلاش
                ExerciseAttempt.objects.create(
                    user=request.user,
                    exercise=exercise,
                    is_correct=True,
                    score_earned=score_earned,
                )
                
                # اضافه کردن امتیاز
                user_score = UserScore.get_or_create(request.user)
                user_score.add_score(score_earned)
                
                result["score_earned"] = score_earned
                result["attempts_used"] = attempts_count + 1
                
                # نمایش نتایج تست‌کیس‌ها
                result["message"] = "✅ همه تست‌ها پاس شد!"
                
            else:
                # ثبت تلاش غلط
                ExerciseAttempt.objects.create(
                    user=request.user,
                    exercise=exercise,
                    is_correct=False,
                    score_earned=0,
                )
                
                # پیام خطا با جزئیات
                failed_tests = [r for r in result["results"] if not r["passed"]]
                
                result["message"] = f"❌ {len(failed_tests)} تست از {result['total_count']} پاس نشد:"
                result["failed_tests"] = failed_tests
                result["attempts_used"] = attempts_count + 1
            
            return JsonResponse(result)
            
        except Exercise.DoesNotExist:
            return JsonResponse({"error": "تمرین یافت نشد"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "داده نامعتبر"}, status=400)