# Generated by Django 5.0.6 on 2024-07-19 02:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("stt", "0002_calllogs"),
    ]

    operations = [
        migrations.AddField(
            model_name="calllogs",
            name="audio_file",
            field=models.FileField(
                null=True, upload_to="audio_files/", verbose_name="음성 파일"
            ),
        ),
    ]
