from pathlib import Path
import json

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.assessments.models import (
    QuestionCategory,
    LearningObjective,
    Question,
    Choice,
)
class Command(BaseCommand):

    help = "Import Question Bank"

    DATA_DIR = (
        Path(__file__)
        .resolve()
        .parents[2]
        / "data"
    )
    def _get_subjects(self):

        return sorted(

            [

                folder

                for folder in self.DATA_DIR.iterdir()

                if folder.is_dir()

            ]

        )
    def _load_category(self, subject_path):

        category_file = subject_path / "category.json"

        if not category_file.exists():
            self.stdout.write(
                self.style.WARNING(
                    f"{subject_path.name} : category.json پیدا نشد."
                )
            )
            return None
        if category_file.stat().st_size == 0:
            self.stdout.write(
                self.style.WARNING(
                    f"{subject_path.name} : category.json خالی است."
                )
            ) 
            return None

        with open(

            category_file,

            "r",

            encoding="utf-8",

        ) as f:

            return json.load(f)

    def _load_questions(self, subject_path):

        questions = []

        for file in sorted(subject_path.glob("*.json")):

            if file.name == "category.json":
                continue

            if file.stat().st_size == 0:

                self.stdout.write(
                    self.style.WARNING(
                        f"{file.name} خالی است."
                    )
                )
                continue

            with open(
                file,
                "r",
                encoding="utf-8",
            ) as f:

                data = json.load(f)
                objective_code = data["learning_objective"]
                file_questions = data["questions"]
                self.stdout.write(
                    self.style.SUCCESS(
                        f"{file.name} : {len(file_questions)} سوال"
                    )
                )
                for question in file_questions:
                    questions.append(
                        {
                            "objective": objective_code,
                            "question": question,
                        }

                    )
        return questions
    def _sync_category(self, data):

        category, created = QuestionCategory.objects.update_or_create(

            code=data["code"],

            defaults={
                "name": data["name"],
            },
        )

        if created:

            self.stdout.write(
                self.style.SUCCESS(
                    f"✓ Category Created : {category.code}"
                )
            )

        else:

            self.stdout.write(
                self.style.WARNING(
                    f"↺ Category Updated : {category.code}"
                )
            )

        return category   
    def _sync_question(self,data,):
        try:
            objective = LearningObjective.objects.get(
                code=data["objective"],
            )
        except LearningObjective.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                f"LearningObjective پیدا نشد: {data['learning_objective']}"
                ))
            return None

        question, created = Question.objects.update_or_create(

            code=data["code"],

            defaults={

                "title": data["title"],

                "body": data["body"],

                "learning_objective": objective,

                "difficulty": data["difficulty"],

                "question_type": data["question_type"],

                "score": data["score"],

                "estimated_seconds": data["estimated_seconds"],

            },
        )

        if created:

            self.stdout.write(
                self.style.SUCCESS(
                    f"        ✓ {question.code}"
                )
            )

        else:

            self.stdout.write(
                self.style.WARNING(
                    f"        ↺ {question.code}"
                )
            )

        return question

    def _sync_learning_objectives(
        self,
        category,
        data,
    ):

        for objective in data["learning_objectives"]:

            obj, created = LearningObjective.objects.update_or_create(

                code=objective["code"],

                defaults={

                    "name": objective["name"],

                    "category": category,

                },
            )

            if created:

                self.stdout.write(

                    self.style.SUCCESS(

                        f"    ✓ {obj.code}"

                    )

                )

            else:

                self.stdout.write(

                    self.style.WARNING(

                        f"    ↺ {obj.code}"

                    )

                )       

    def handle(self, *args, **kwargs):

        subjects = self._get_subjects()

        self.stdout.write("Subjects")

        for subject in subjects:

            category = self._load_category(subject)

            if category is None:
                continue

            category_obj = self._sync_category(category)

            self._sync_learning_objectives(
                category_obj,
                category,
            )

            questions = self._load_questions(subject)

            self.stdout.write(
                self.style.SUCCESS(
                    f"Importing {len(questions)} questions..."
                )
            )

            for question in questions:
                self._sync_question(question)

            
            

            