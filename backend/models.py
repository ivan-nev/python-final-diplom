from django.db import models

class Shop(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    url = models.URLField(verbose_name='Ссылка', null=True, blank=True)
    filename = models.FilePathField(verbose_name='Путь к файлу')

    # class Meta:
    #     verbose_name = 'Магазин'
    #     verbose_name_plural = "Список магазинов"
    #     ordering = ('-name',)

    def __str__(self):
        return self.name

