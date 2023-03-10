# Generated by Django 3.1.5 on 2021-02-08 07:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PastList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=200)),
                ('capacity', models.IntegerField()),
            ],
            options={
                'ordering': ('number',),
            },
        ),
        migrations.CreateModel(
            name='SingleSubject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=200)),
                ('pastList', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assigner.pastlist')),
            ],
        ),
    ]
