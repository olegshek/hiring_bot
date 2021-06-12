# Generated by Django 3.2.3 on 2021-06-04 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hiring', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='resume',
            name='filled_out_at',
            field=models.DateTimeField(null=True, verbose_name='Filled out at'),
        ),
        migrations.AddField(
            model_name='resume',
            name='resume_id',
            field=models.IntegerField(null=True, verbose_name='Resume id'),
        ),
        migrations.AlterField(
            model_name='resume',
            name='info',
            field=models.CharField(max_length=4096, null=True, verbose_name='Info'),
        ),
        migrations.AlterField(
            model_name='resume',
            name='photo',
            field=models.ImageField(null=True, upload_to='', verbose_name='Photo'),
        ),
    ]
