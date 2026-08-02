from django.contrib.admin import SimpleListFilter
from django.db.models import QuerySet


class DepartmentListFilter(SimpleListFilter):
    """
    فیلتر دپارتمان بر اساس دسترسی کاربر
    """

    title = "دپارتمان"
    parameter_name = "department"

    def lookups(self, request, model_admin):

        department_field = getattr(
            model_admin,
            "department_field",
            "department",
        )

        department_lookup = getattr(
            model_admin,
            "department_lookup",
            department_field,
        )

        try:
            field = model_admin.model._meta.get_field(
                department_field
            )

            department_model = field.related_model

        except Exception:
            return []

        if request.user.is_superuser:

            departments = department_model.objects.all()

        else:

            department = getattr(
                request.user,
                "department",
                None,
            )

            if not department:
                return []

            departments = [
                department,
            ]

        return [
            (
                item.id,
                item.name,
            )
            for item in departments
        ]


    def queryset(
        self,
        request,
        queryset,
    ):

        if self.value():

            return queryset.filter(
                department_id=self.value()
            )

        return queryset



class DepartmentRestrictedAdminMixin:
    """
    محدودسازی داده‌های Admin بر اساس دپارتمان کاربر
    """

    department_field = "department"

    department_lookup = None

    department_foreignkeys = {}


    def get_queryset(
        self,
        request,
    ) -> QuerySet:

        queryset = super().get_queryset(request)

        if request.user.is_superuser:
            return queryset


        department = getattr(
            request.user,
            "department",
            None,
        )


        if not department:

            return queryset.none()


        lookup = (
            self.department_lookup
            or self.department_field
        )


        return queryset.filter(
            **{
                lookup: department
            }
        )


    def formfield_for_foreignkey(
        self,
        db_field,
        request,
        **kwargs,
    ):

        # محدود کردن فیلد مستقیم Department
        if db_field.name == self.department_field:

            if request.user.is_superuser:

                kwargs["queryset"] = (
                    db_field.related_model.objects.all()
                )

            else:

                department = getattr(
                    request.user,
                    "department",
                    None,
                )

                if department:

                    kwargs["queryset"] = (
                        db_field.related_model.objects.filter(
                            id=department.id
                        )
                    )

                else:

                    kwargs["queryset"] = (
                        db_field.related_model.objects.none()
                    )


        # محدود کردن ForeignKey های وابسته
        config = getattr(
            self,
            "department_foreignkeys",
            {},
        ).get(
            db_field.name
        )


        if config:

            model = config["model"]
            lookup = config["lookup"]


            if request.user.is_superuser:

                kwargs["queryset"] = (
                    model.objects.all()
                )

            else:

                department = getattr(
                    request.user,
                    "department",
                    None,
                )

                if department:

                    kwargs["queryset"] = (
                        model.objects.filter(
                            **{
                                lookup: department
                            }
                        )
                    )

                else:

                    kwargs["queryset"] = (
                        model.objects.none()
                    )


        return super().formfield_for_foreignkey(
            db_field,
            request,
            **kwargs,
        )


    def save_model(
        self,
        request,
        obj,
        form,
        change,
    ):

        if not request.user.is_superuser:

            department = getattr(
                request.user,
                "department",
                None,
            )

            if department and hasattr(
                obj,
                self.department_field,
            ):

                setattr(
                    obj,
                    self.department_field,
                    department,
                )


        super().save_model(
            request,
            obj,
            form,
            change,
        )