from django import forms
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path

from apps.assessments.models import (
    Course,
    CourseInstructorAssignment,
    ScientificGroupMembership,
)


class CourseInstructorAssignmentForm(
    forms.ModelForm
):

    class Meta:
        model = CourseInstructorAssignment
        fields = "__all__"

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(
            *args,
            **kwargs,
        )

        instructor_queryset = (
            self.fields["instructor"]
            .queryset
        )

        self.fields["instructor"].queryset = (
            instructor_queryset.none()
        )

        self.fields["instructor"].help_text = (
            "ابتدا دوره را انتخاب کنید."
        )

        course = None

        if (
            self.instance.pk
            and self.instance.course_id
        ):
            course = self.instance.course

        course_id = self.data.get("course")

        if course_id:
            try:
                course = (
                    Course.objects
                    .select_related(
                        "scientific_group"
                    )
                    .get(
                        pk=course_id
                    )
                )
            except Course.DoesNotExist:
                course = None

        if (
            course
            and course.scientific_group_id
        ):
            self.fields["instructor"].queryset = (
                instructor_queryset
                .filter(
                    scientific_group_memberships__scientific_group=(
                        course.scientific_group
                    ),
                    scientific_group_memberships__role=(
                        ScientificGroupMembership
                        .Role
                        .INSTRUCTOR
                    ),
                    scientific_group_memberships__is_active=True,
                    is_active=True,
                )
                .distinct()
            )


@admin.register(CourseInstructorAssignment)
class CourseInstructorAssignmentAdmin(
    admin.ModelAdmin,
):

    form = CourseInstructorAssignmentForm

    list_display = (
        "course",
        "instructor",
        "role",
        "is_active",
        "assigned_at",
    )

    list_filter = (
        "role",
        "is_active",
        "course__scientific_group",
    )

    search_fields = (
        "course__code",
        "course__name",
        "instructor__username",
        "instructor__first_name",
        "instructor__last_name",
    )

    ordering = (
        "course",
        "role",
        "instructor",
    )

    autocomplete_fields = (
        "course",
    )

    readonly_fields = (
        "assigned_at",
    )

    def get_urls(self):

        urls = super().get_urls()

        custom_urls = [
            path(
                "instructors-for-course/",
                self.admin_site.admin_view(
                    self.instructors_for_course
                ),
                name=(
                    "assessments_course_instructors"
                ),
            ),
        ]

        return custom_urls + urls

    def instructors_for_course(
        self,
        request,
    ):

        course_id = request.GET.get(
            "course_id"
        )

        if not course_id:
            return JsonResponse(
                {
                    "instructors": []
                }
            )

        try:
            course = (
                Course.objects
                .select_related(
                    "scientific_group"
                )
                .get(
                    pk=course_id
                )
            )

        except Course.DoesNotExist:
            return JsonResponse(
                {
                    "instructors": []
                }
            )

        if not course.scientific_group_id:
            return JsonResponse(
                {
                    "instructors": []
                }
            )

        memberships = (
            ScientificGroupMembership.objects
            .filter(
                scientific_group=(
                    course.scientific_group
                ),
                role=(
                    ScientificGroupMembership
                    .Role
                    .INSTRUCTOR
                ),
                is_active=True,
                user__is_active=True,
            )
            .select_related(
                "user"
            )
            .order_by(
                "user__first_name",
                "user__last_name",
                "user__username",
            )
        )

        instructors = []

        for membership in memberships:

            user = membership.user

            instructors.append(
                {
                    "id": str(
                        user.pk
                    ),
                    "name": str(
                        user
                    ),
                }
            )

        return JsonResponse(
            {
                "instructors": instructors
            }
        )