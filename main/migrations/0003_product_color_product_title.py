# Generated by Django 4.2.7 on 2023-11-29 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_product_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='color',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='title',
            field=models.TextField(blank=True, null=True),
        ),
    ]
