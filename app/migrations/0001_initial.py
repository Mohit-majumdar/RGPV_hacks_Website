# Generated by Django 2.2.7 on 2020-01-30 17:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Semseter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sem', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Suggetion_Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('massege', models.TextField(max_length=400, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User_contect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.IntegerField(null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Previous_year_question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('year', models.IntegerField(null=True)),
                ('file', models.FileField(null=True, upload_to='')),
                ('branch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Branch')),
                ('sem', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Semseter')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Book')),
                ('moblie', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.User_contect')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('note', models.FileField(null=True, upload_to='')),
                ('branch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Branch')),
                ('sem', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Semseter')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='branch',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Branch'),
        ),
        migrations.AddField(
            model_name='book',
            name='sem',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Semseter'),
        ),
    ]
