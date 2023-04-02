from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Kitty(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    content = models.TextField(blank=True, verbose_name='Содержание')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='Фото')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    is_published = models.BooleanField(default=True, verbose_name='Опубликован')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категории')

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})
    
    class Meta:
        verbose_name = 'кошки' #переименование в админке (ед число)
        verbose_name_plural = 'кошки' #переименование в даминке (мн число)
        ordering = ['time_create', 'title'] #сортировка в админке
    
class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})
    
    class Meta:
        verbose_name = 'категории' #переименование в админке (ед число)
        verbose_name_plural = 'категории' #переименование в даминке (мн число)
        ordering = ['id'] #сортировка в админке