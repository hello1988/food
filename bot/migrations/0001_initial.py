# Generated by Django 2.0.2 on 2018-02-18 11:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FoodLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image_url', models.CharField(max_length=512)),
                ('starch', models.FloatField(default=0.0, verbose_name='主食')),
                ('protein', models.FloatField(default=0.0, verbose_name='蛋白質')),
                ('fruit', models.FloatField(default=0.0, verbose_name='水果')),
                ('vegetables', models.FloatField(default=0.0, verbose_name='蔬菜')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('line_id', models.CharField(max_length=64)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='foodlog',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.Member'),
        ),
    ]
