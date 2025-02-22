# Generated by Django 4.2.18 on 2025-02-01 19:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses_app', '0009_progress_completed'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='progress',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='materialprogress',
            name='completed',
        ),
        migrations.AddField(
            model_name='materialprogress',
            name='progress_percentage',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='progress',
            name='material',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='progress_records', to='courses_app.material'),
        ),
        migrations.AlterField(
            model_name='materialprogress',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='material_progress_records', to='courses_app.material'),
        ),
        migrations.AlterUniqueTogether(
            name='progress',
            unique_together={('student', 'course', 'material')},
        ),
    ]
