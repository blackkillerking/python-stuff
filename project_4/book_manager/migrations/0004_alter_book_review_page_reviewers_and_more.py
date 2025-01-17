# Generated by Django 5.1.4 on 2025-01-12 08:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_manager', '0003_remove_book_reveiw_page_book_review_page_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book_review_page',
            name='reviewers',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='reviewers', to='book_manager.reviewer'),
        ),
        migrations.AlterField(
            model_name='reviewer',
            name='reviewer_texts',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='reviewer_text', to='book_manager.reviewer_text'),
        ),
    ]
