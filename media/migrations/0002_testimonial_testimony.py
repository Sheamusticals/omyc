# Generated by Django 5.1.1 on 2024-11-18 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='testimonial',
            name='testimony',
            field=models.TextField(default=1, max_length=2000),
            preserve_default=False,
        ),
    ]