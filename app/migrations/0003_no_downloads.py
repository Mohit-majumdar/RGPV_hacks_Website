# Generated by Django 2.2.7 on 2020-03-03 19:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20200205_1603'),
    ]

    operations = [
        migrations.CreateModel(
            name='No_downloads',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('downloads', models.IntegerField(null=True)),
                ('note', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Notes')),
            ],
        ),
    ]
