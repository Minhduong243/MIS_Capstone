# Generated by Django 2.1.1 on 2018-09-30 22:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('university', '0001_initial'),
        ('partners', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='campuspartner',
            name='college',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='university.College'),
        ),
        migrations.AddField(
            model_name='campuspartner',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='university.Department'),
        ),
        migrations.AddField(
            model_name='campuspartner',
            name='education_system',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='university.EducationSystem'),
        ),
        migrations.AddField(
            model_name='campuspartner',
            name='university',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='university.University'),
        ),
    ]
