# Generated by Django 2.1.1 on 2018-10-28 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_semester_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='semester',
            name='description',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='status',
            name='description',
            field=models.CharField(max_length=255),
        ),
    ]
