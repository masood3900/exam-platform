from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("assessments", "0013_alter_learningobjective_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="questioncategory",
            name="course",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="categories",
                to="assessments.course",
                verbose_name="دوره آموزشی",
            ),
        ),
    ]