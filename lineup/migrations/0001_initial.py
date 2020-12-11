# Generated by Django 3.1.4 on 2020-12-11 09:14

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    operations = [
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(help_text='Display name on the website.', max_length=50, verbose_name='label')),
                ('slug', models.SlugField(help_text='Unique identifier for the menu voice.', unique=True, verbose_name='slug')),
                ('link', models.CharField(blank=True, max_length=255, null=True, verbose_name='link')),
                ('order', models.IntegerField(verbose_name='order')),
                ('enabled', models.BooleanField(verbose_name='enabled')),
                ('login_required', models.BooleanField(default=False, help_text='If this is checked, only logged-in users will be able to view the page.', verbose_name='login required')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='lineup.menuitem', verbose_name='parent')),
                ('permissions', models.ManyToManyField(blank=True, help_text='If empty, the menu item will be publicly visible, otherwise only users with at least one of the selected permissions could see it.', to='auth.Permission', verbose_name='permissions')),
            ],
            options={
                'verbose_name': 'Menu item',
                'verbose_name_plural': 'Menu items',
            },
        ),
    ]