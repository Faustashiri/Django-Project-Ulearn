from django.contrib import admin
from .models import (
    MainPage,
    MainPageImage,
    Demand,
    Geography,
    SkillsSet,
    StatisticSet,
)

# Inline для изображений на главной странице
class MainPageImageInline(admin.TabularInline):
    model = MainPageImage
    extra = 1


# Админка для главной страницы
@admin.register(MainPage)
class MainPageAdmin(admin.ModelAdmin):
    inlines = [MainPageImageInline]


# Регистрация моделей в админке
admin.site.register(Demand)
admin.site.register(Geography)
admin.site.register(SkillsSet)
admin.site.register(StatisticSet)
