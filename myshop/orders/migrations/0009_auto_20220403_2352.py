# Generated by Django 3.0.4 on 2022-04-03 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_auto_20220403_2308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='city',
            field=models.CharField(choices=[('TARAUNI', 'TARAUNI'), ('NASARAWA', 'NASARAWA'), ('KANO MUNICIPAL', 'KANO MUNICIPAL'), ('FAGGE', 'FAGGE'), ('KUMBOTSO', 'KUMBOTSO'), ('RIMI', 'RIMI'), ('UNGOGO', 'UNGOGO')], default='NASARAWA', max_length=100),
        ),
    ]
