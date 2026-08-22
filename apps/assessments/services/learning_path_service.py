from django.db.models import Count

from apps.assessments.models import (
    LearningPath,
    Attempt,
)


class LearningPathService:

    @staticmethod
    def user_paths(user):

        paths = (
            LearningPath.objects
            .filter(
                is_active=True,
                categories__learning_objectives__questions__attemptquestion__attempt__student=user,
            )
            .distinct()
        )

        result = []

        for path in paths:

            attempts = Attempt.objects.filter(
                student=user,
                assessment__rules__category__learning_path=path,
            ).distinct()

            graded_attempts = attempts.filter(
                status=Attempt.Status.GRADED,
            )

            last_attempt = (
                graded_attempts
                .order_by(
                    "-finished_at"
                )
                .first()
            )

            average = (
                graded_attempts
                .aggregate(
                    avg=Count("id")
                )
            )

            result.append(
                {
                    "path": path,
                    "attempts": attempts.count(),
                    "completed": graded_attempts.count(),
                    "last_attempt": last_attempt,
                }
            )

        return result