# Generated by Django 4.2.5 on 2023-10-07 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('multiple_images', '0002_alter_multipleimage_images'),
    ]

    operations = [
        migrations.AddField(
            model_name='multipleimage',
            name='name',
            field=models.CharField(max_length=64, null=True),
        ),
    ]
