# Generated by Django 3.1.3 on 2020-11-26 15:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0003_auto_20201126_1118'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='application',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='server.application'),
        ),
    ]
