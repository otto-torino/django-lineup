# Generated by Django 3.1.4 on 2020-12-13 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lineup', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='enabled',
            field=models.BooleanField(default=True, verbose_name='enabled'),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='login_required',
            field=models.BooleanField(default=False, help_text='If this is checked, only logged-in users will be able to view the item.', verbose_name='login required'),
        ),
    ]
