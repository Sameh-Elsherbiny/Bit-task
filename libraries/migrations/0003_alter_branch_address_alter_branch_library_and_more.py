# Generated by Django 5.1.4 on 2025-01-11 20:25

import django.contrib.gis.db.models.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraries', '0002_delete_branchbook'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='address',
            field=models.CharField(max_length=100, verbose_name='Address'),
        ),
        migrations.AlterField(
            model_name='branch',
            name='library',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='libraries.library', verbose_name='Library'),
        ),
        migrations.AlterField(
            model_name='branch',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326, verbose_name='Location'),
        ),
        migrations.AlterField(
            model_name='library',
            name='email',
            field=models.EmailField(max_length=100, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='library',
            name='image',
            field=models.ImageField(blank=True, upload_to='library_images', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='library',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='library',
            name='phone',
            field=models.CharField(max_length=100, verbose_name='Phone'),
        ),
        migrations.AlterField(
            model_name='library',
            name='website',
            field=models.URLField(max_length=100, verbose_name='Website'),
        ),
    ]