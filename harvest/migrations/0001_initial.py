# Generated by Django 4.2.7 on 2023-12-10 10:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=128)),
                ('task', models.CharField(max_length=128)),
                ('priority', models.IntegerField()),
                ('status', models.CharField(choices=[('preparation', 'preparation'), ('annotation', 'annotation'), ('done', 'done')], db_index=True, default='preparation', max_length=64)),
                ('required_answers', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'batches',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.TextField()),
                ('meta', models.TextField()),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='harvest.batch')),
            ],
        ),
        migrations.CreateModel(
            name='Annotation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hate_level', models.CharField(choices=[('preparation', 'preparation'), ('annotation', 'annotation'), ('done', 'done')], default='preparation', max_length=64)),
                ('hate_cathegory', models.CharField(choices=[('preparation', 'preparation'), ('annotation', 'annotation'), ('done', 'done')], default='preparation', max_length=64)),
                ('username', models.CharField(db_index=True, max_length=128)),
                ('answer', models.CharField(choices=[('accept', 'accept'), ('ignore', 'ignore'), ('reject', 'reject')], max_length=64)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='harvest.question')),
            ],
        ),
    ]
