from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = "Setup project"

    def handle(self, *args, **kwargs):

        groups = [
            "Student",
            "Teacher",
            "Manager",
        ]

        for group_name in groups:
            group, created = Group.objects.get_or_create(
                name=group_name
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Group '{group_name}' created."
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Group '{group_name}' already exists."
                    )
                )