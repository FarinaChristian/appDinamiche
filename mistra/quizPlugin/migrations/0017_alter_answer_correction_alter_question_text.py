# Generated by Django 5.2.3 on 2025-07-01 09:20

import django_ckeditor_5.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizPlugin', '0016_alter_answer_correction_alter_question_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='correction',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='Correzione della risposta'),
        ),
        migrations.AlterField(
            model_name='question',
            name='text',
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name='Testo della domanda'),
        ),
    ]
