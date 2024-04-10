# Generated by Django 5.0.4 on 2024-04-10 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_post_description_alter_post_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='board',
            field=models.CharField(choices=[('General', 'General'), ('Academic', 'Academic'), ('Entertainment', 'Entertainment'), ('Sports', 'Sports'), ('Religion', 'Religion'), ('Technology', 'Technology'), ('Health', 'Health'), ('Fashion', 'Fashion'), ('Business', 'Business'), ('Science', 'Science'), ('Agriculture', 'Agriculture'), ('Hackclub', 'Hackclub')], default='General', max_length=255),
        ),
    ]
