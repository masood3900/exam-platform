from django.contrib import admin
from apps.assessments.models import (
    QuestionCategory,
    LearningObjective,
    Question,
    Choice,
)
from apps.core.admin_mixins.department import (
     DepartmentRestrictedAdminMixin,
     DepartmentListFilter,
)
 

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1
    min_num = 0
    fields = (
        
        "text",
        "is_correct",
        "explanation",
    )

@admin.register(Question)
class QuestionAdmin(
    DepartmentRestrictedAdminMixin,
    admin.ModelAdmin,
):

    list_display = (
        "code",
        "title",
        "learning_objective",
        "difficulty",
        "question_type",
        "is_active",
    )

    list_filter = (
        "difficulty",
        "question_type",
        "is_active",
    )

    search_fields = (
        "code",
        "title",
        "body",
    )

    ordering = (
        "code",
    )

    list_per_page = 25

    list_select_related = (
        "learning_objective",
        "learning_objective__category",
        "learning_objective__category__department",
    )

    autocomplete_fields = (
        "learning_objective",
    )

    department_lookup = (
        "learning_objective__category__department"
    )

    department_foreignkeys = {
        "learning_objective": {
            "model": LearningObjective,
            "lookup": "category__department",
        },
    }

    inlines = [
        ChoiceInline,
    ]


    def save_formset(
        self,
        request,
        form,
        formset,
        change,
    ):

        instances = formset.save(commit=False)

        # حذف گزینه‌هایی که کاربر پاک کرده
        for obj in formset.deleted_objects:
            obj.delete()


        order = 1

        for instance in instances:

            if instance.text:

                instance.order = order

                instance.save()

                order += 1

        formset.save_m2m()
@admin.register(LearningObjective)
class LearningObjectiveAdmin(DepartmentRestrictedAdminMixin,admin.ModelAdmin):
    department_lookup = "category__department"
    list_display = (
        "code",
        "name",
        "category",
        "weight",
        "bloom_level",
        "is_active",
    )

    list_filter = (
        "bloom_level",
        "is_active",
    )

    search_fields = (
        "code",
        "name",
        "description",
    )

    ordering = (
        "order",
        "code",
    )

    filter_horizontal = (
        "prerequisites",
    )
    list_per_page = 25
    list_select_related = (
        "category",
        "category__department",
    )
    autocomplete_fields = (
        "category",
    )
    
    department_foreignkeys = {
        "category": {
            "model": QuestionCategory,
            "lookup": "department",
        },
    }
     
@admin.register(QuestionCategory)
class QuestionCategoryAdmin(DepartmentRestrictedAdminMixin,admin.ModelAdmin):

    list_display = (
        "code",
        "name",
        "course",
        "department",
        "parent",
        "order",
        "is_active",
    )

    list_filter = (
        DepartmentListFilter,
        
        "is_active",
    )

    search_fields = (
        "code",
        "name",
        "course__name",
        "parent__name",
    )

    ordering = (
        "order",
        "name",
    ) 
    list_per_page = 25

    list_select_related = (
        "course",
        "department",
        "parent",
        
    )
    autocomplete_fields = (
        "course",
        "parent",
    )
    department_field = "department"
    
    department_foreignkeys = {
        "parent": {
            "model": QuestionCategory,
            "lookup": "department",
        },
    }
   
@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):

    list_display = (
        "question",
        "order",
        "text",
        "is_correct",
    )

    list_filter = (
        "is_correct",
    )

    search_fields = (
        "question__code",
        "text",
    )

    ordering = (
        "question",
        "order",
    )
