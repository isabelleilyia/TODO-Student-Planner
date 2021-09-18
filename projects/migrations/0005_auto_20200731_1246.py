# Generated by Django 3.0.8 on 2020-07-31 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_auto_20200730_0831'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='doc_status',
            field=models.CharField(choices=[('Incomplete', 'Incomplete'), ('Complete', 'Complete')], default='Incomplete', max_length=64),
        ),
        migrations.AddField(
            model_name='link',
            name='due_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]