# Generated by Django 4.0.3 on 2022-04-01 05:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_remove_category_posts_category_post_tag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='post',
        ),
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='blog.category'),
        ),
    ]
