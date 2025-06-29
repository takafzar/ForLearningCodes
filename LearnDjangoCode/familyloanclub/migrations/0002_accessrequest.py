# Generated by Django 5.2.2 on 2025-06-08 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('familyloanclub', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=11)),
                ('referrer_phone', models.CharField(max_length=11)),
                ('access_code', models.CharField(blank=True, max_length=6, null=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
