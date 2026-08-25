from django.contrib import admin
from apps.assessments.models import (
    QuestionCategory,
    LearningObjective,
    Question,
    Choice,
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
        
    )

    autocomplete_fields = (
        "learning_objective",
    )

   
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
class LearningObjectiveAdmin(admin.ModelAdmin):
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
    )
    autocomplete_fields = (
        "category",
    )
    

     
@admin.register(QuestionCategory)
class QuestionCategoryAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "name",
        "course",
        "parent",
        "order",
        "is_active",
    )

    list_filter = (
        
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
        "parent",
        
    )
    autocomplete_fields = (
        "course",
        "parent",
    )
    
   
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
