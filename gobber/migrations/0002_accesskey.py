# Generated by Django 4.0.2 on 2022-10-09 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gobber', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=10)),
            ],
        ),
    ]
