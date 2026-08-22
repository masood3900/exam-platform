from collections import defaultdict
from apps.assessments.models import Attempt

class AnalyticsService:
    @staticmethod
    def learning_objective_report(attempt:Attempt):
        """تحلیل عملکرد بر اساس اهداف آموزشی """
        report = []

        questions = (
            attempt.questions
            .select_related(
                "question__learning_objective",
            )
        )
        grouped = defaultdict(list)
        for aq in questions:
            grouped[
               aq.question.learning_objective 
            ].append(aq)
        for objective, items in grouped.items():
            total = len(items)
            correct = sum(1 for q in items if q.is_correct)
            percentage = (
                round(correct *100/total,2)
                if total
                else 0
            )
            report.append(
              {
                  "objective": objective,
                  "total": total,
                  "correct": correct,
                  "percentage": percentage,  
              }  
            )
        return report

