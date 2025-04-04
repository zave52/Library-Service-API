# Generated by Django 5.1.7 on 2025-03-08 16:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('author', models.CharField(max_length=150)),
                ('cover', models.CharField(choices=[('HARD', 'Hard'), ('SOFT', 'Soft')], default='SOFT', max_length=4)),
                ('inventory', models.PositiveIntegerField()),
                ('daily_fee', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(0)])),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('title', 'author'), name='unique_title_author')],
            },
        ),
    ]
