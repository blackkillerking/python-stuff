# Generated by Django 5.1.4 on 2025-01-08 10:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(max_length=500)),
                ('category_image', models.ImageField(null=True, upload_to='category/image/')),
            ],
        ),
        migrations.CreateModel(
            name='Reader_Favorite_Books',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_id', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reveiwer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=255)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reveiwer_Text',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_text', models.TextField(max_length=500)),
                ('rating', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Readers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=255)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('profile_picture', models.ImageField(null=True, upload_to='readers/profile_picture/')),
                ('favorite_books', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_books', to='books.reader_favorite_books')),
            ],
        ),
        migrations.CreateModel(
            name='Book_Reveiw_Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reveiwers', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reveiwers', to='books.reveiwer')),
            ],
        ),
        migrations.AddField(
            model_name='reveiwer',
            name='reveiwer_text',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='reveiwer_text', to='books.reveiwer_text'),
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(max_length=500)),
                ('publication_date', models.DateField()),
                ('cover_image', models.ImageField(upload_to='book/covers/')),
                ('sample_pdf', models.FileField(null=True, upload_to='book/samples/')),
                ('is_published', models.BooleanField()),
                ('author', models.ManyToManyField(related_name='author', to='books.author')),
                ('reveiw_page', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='reveiw_page', to='books.book_reveiw_page')),
                ('category', models.ManyToManyField(related_name='category', to='books.categories')),
                ('reader', models.ManyToManyField(related_name='reader', to='books.readers')),
                ('tag', models.ManyToManyField(related_name='tag', to='books.tags')),
            ],
        ),
    ]
