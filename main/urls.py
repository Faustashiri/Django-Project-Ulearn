from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

# URL-шаблоны для приложения
urlpatterns = [
    # Главная страница
    path('', views.home, name='home'),

    # Страница статистики
    path('statistics/', views.statistics, name='statistics'),

    # Страница данных о спросе
    path('demand/', views.demand, name='demand'),

    # Географическая статистика
    path('geography/', views.geography, name='geography'),

    # Страница навыков
    path('skills/', views.skills, name='skills'),

    # Последние вакансии
    path('latest-jobs/', views.latest_jobs, name='latest_jobs'),
]

# Настройки для отображения медиафайлов в режиме отладки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
