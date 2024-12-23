# Generated by Django 5.1.1 on 2024-11-19 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0003_portfolio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gallery',
            name='image',
        ),
        migrations.AddField(
            model_name='gallery',
            name='media',
            field=models.FileField(default=1, upload_to='media/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gallery',
            name='media_type',
            field=models.CharField(choices=[('image', 'Image'), ('video', 'Video')], default='image', max_length=5),
        ),
    ]
