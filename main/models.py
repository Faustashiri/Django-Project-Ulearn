from django.db import models


class ProfessionPage(models.Model):
    title = models.TextField(blank=True, verbose_name='Название профессии')
    description = models.TextField(blank=True, verbose_name='Описание профессии')
    main_image = models.ImageField(blank=False, verbose_name='Основное изображение', upload_to='images/')


class ProfessionPageImage(models.Model):
    profession_page = models.ForeignKey(
        ProfessionPage,
        on_delete=models.CASCADE,
        related_name='extra_images',
        verbose_name='Страница профессии'
    )
    image = models.ImageField(verbose_name='Дополнительное изображение', upload_to='images/')


class DemandData(models.Model):
    salary_trend_graph = models.ImageField(
        blank=False,
        verbose_name='График трендов зарплат по годам'
    )
    vacancy_trend_graph = models.ImageField(
        blank=False,
        verbose_name='График трендов вакансий по годам'
    )
    salary_statistics_table = models.TextField(
        blank=False,
        verbose_name='Таблица статистики зарплат'
    )
    vacancy_statistics_table = models.TextField(
        blank=False,
        verbose_name='Таблица статистики вакансий'
    )


class CityStatistics(models.Model):
    salary_by_city_graph = models.ImageField(
        blank=False,
        verbose_name='График зарплат по городам'
    )
    vacancy_distribution_graph = models.ImageField(
        blank=False,
        verbose_name='График распределения вакансий по городам'
    )
    salary_by_city_table = models.TextField(
        blank=False,
        verbose_name='Таблица зарплат по городам'
    )
    vacancy_distribution_table = models.TextField(
        blank=False,
        verbose_name='Таблица распределения вакансий по городам'
    )


class SkillSet(models.Model):
    name = models.TextField(blank=False, verbose_name='Название набора навыков', max_length=30)
    data_table = models.TextField(blank=False, verbose_name='Таблица навыков')
    skill_graph = models.ImageField(blank=False, verbose_name='График навыков')

    class Meta:
        verbose_name = 'Набор навыков'
        verbose_name_plural = 'Наборы навыков'


class Statistics(models.Model):
    annual_salary_graph = models.ImageField(
        blank=False,
        verbose_name='График годовых зарплат'
    )
    annual_salary_table = models.TextField(
        blank=False,
        verbose_name='Таблица годовых зарплат'
    )

    annual_vacancy_graph = models.ImageField(
        blank=False,
        verbose_name='График годовых вакансий'
    )
    annual_vacancy_table = models.TextField(
        blank=False,
        verbose_name='Таблица годовых вакансий'
    )

    city_salary_graph = models.ImageField(
        blank=False,
        verbose_name='График зарплат по городам'
    )
    city_salary_table = models.TextField(
        blank=False,
        verbose_name='Таблица зарплат по городам'
    )

    city_vacancy_graph = models.ImageField(
        blank=False,
        verbose_name='График доли вакансий по городам'
    )
    city_vacancy_table = models.TextField(
        blank=False,
        verbose_name='Таблица доли вакансий по городам'
    )

    top_skills_graph = models.ImageField(
        blank=False,
        verbose_name='График топ-20 навыков'
    )
    top_skills_table = models.TextField(
        blank=False,
        verbose_name='Таблица топ-20 навыков'
    )
