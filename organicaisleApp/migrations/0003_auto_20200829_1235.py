# Generated by Django 3.1 on 2020-08-29 07:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organicaisleApp', '0002_auto_20200828_1100'),
    ]

    operations = [
        migrations.CreateModel(
            name='SliderType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slider_type', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='slider',
            name='slider_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='organicaisleApp.slidertype'),
        ),
    ]
