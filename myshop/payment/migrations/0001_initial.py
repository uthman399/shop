# Generated by Django 3.0.4 on 2022-03-12 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=150)),
                ('lastname', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=254)),
                ('phonenumber', models.CharField(max_length=20)),
                ('amount', models.IntegerField(default=1000)),
                ('state', models.CharField(default='enter state', max_length=150)),
            ],
        ),
    ]
