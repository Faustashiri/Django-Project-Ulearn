from . import core_constants
from .models import MainPage, SkillsSet

# Контекстные процессоры для шаблонов
def get_funding_centers(request):
    """Добавляет список центров финансирования в контекст."""
    return {'funding_centers': core_constants.FCs}


def get_academic_group(request):
    """Добавляет список академических групп в контекст."""
    return {'academic_group': core_constants.ACADEMIC_GROUP}


# Функции для получения данных из моделей
def fetch_main_page(request):
    """
    Получает данные главной страницы с предзагрузкой дополнительных изображений.
    """
    return MainPage.objects.prefetch_related('additional_images').all()


def fetch_skills_data(request):
    """
    Получает информацию о доступных наборах навыков.
    """
    return SkillsSet.objects.all()


# Дополнительные переменные для контекста
def get_profession_title(request):
    """Добавляет название профессии в контекст."""
    return {'profession_title': core_constants.PROFESSION_NAME}


def get_website_name(request):
    """Добавляет название веб-сайта в контекст."""
    return {'website_name': core_constants.SITE_NAME}
