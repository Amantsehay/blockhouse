# Generated by Django 5.1.2 on 2024-10-26 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EMAStrategy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_window', models.PositiveIntegerField()),
                ('long_window', models.PositiveIntegerField()),
                ('stock_symbol', models.CharField(max_length=20)),
                ('initial_investment', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='PredictedPriceModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=20)),
            ],
        ),
    ]
