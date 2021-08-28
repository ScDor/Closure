# Generated by Django 3.2.4 on 2021-08-28 19:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0004_auto_20210629_0256'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='courses',
        ),
        migrations.RemoveField(
            model_name='student',
            name='year_in_studies',
        ),
        migrations.RemoveField(
            model_name='take',
            name='student',
        ),
        migrations.CreateModel(
            name='CoursePlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=50, null=True)),
                ('public', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rest_api.student')),
            ],
        ),
        migrations.AddField(
            model_name='take',
            name='course_plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rest_api.courseplan'),
            preserve_default=False,
        ),
    ]
