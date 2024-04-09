# Generated by Django 5.0.4 on 2024-04-09 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_alter_post_board'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.ImageField(blank=True, null=True, upload_to='posts/'),
        ),
    ]