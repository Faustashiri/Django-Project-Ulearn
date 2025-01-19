from django.shortcuts import render
import requests
from datetime import datetime

from .context_processors import fetch_main_page, fetch_skills_data
from .models import ProfessionPage, DemandData, CityStatistics, SkillSet, Statistics
from . import utils

def home(request):
    return render(request, 'home.html', {
        'context': fetch_main_page(request)
    })

def statistics(request):
    stat_set = Statistics.objects.first()

    context = {
        'salary_plot': stat_set.annual_salary_graph.url,
        'salary_table': stat_set.annual_salary_table,
        'vacancies_plot': stat_set.annual_vacancy_graph.url,
        'vacancies_table': stat_set.annual_vacancy_table,
        'city_salary_plot': stat_set.city_salary_graph.url,
        'city_salary_table': stat_set.city_salary_table,
        'city_vacancies_plot': stat_set.city_vacancy_graph.url,
        'city_vacancies_table': stat_set.city_vacancy_table,
        'skills_plot': stat_set.top_skills_graph.url,
        'skills_table': stat_set.top_skills_table,
    }

    return render(request, 'statistics.html', context)

def demand(request):
    demand = DemandData.objects.first()

    return render(request, 'demand.html', {
        'graph_salary_level': demand.salary_trend_graph.url,
        'graph_num_vacancy': demand.vacancy_trend_graph.url,
        'salary_table': demand.salary_statistics_table,
        'vacancy_table': demand.vacancy_statistics_table,
    })

def geography(request):
    geo = CityStatistics.objects.first()

    return render(request, 'geography.html', {
        'graph_salary_level_by_city': geo.salary_by_city_graph.url,
        'graph_vacancy_fraction_by_city': geo.vacancy_distribution_graph.url,
        'level_by_city_table': geo.salary_by_city_table,
        'fraction_by_city_table': geo.vacancy_distribution_table
    })

def skills(request):
    skills_set = fetch_skills_data(request).first()
    skills_table = skills_set.data_table
    skills_plot = skills_set.skill_graph.url

    return render(request, 'skills.html', {
        'skills_plot': skills_plot,
        'skills_table': skills_table
    })

def latest_jobs(request):
    job_title_keywords = ['C# программист', 'c#', 'c sharp', 'шарп', 'с#']

    url = 'https://api.hh.ru/vacancies/'

    search_query = ' OR '.join(job_title_keywords)

    params = {
        'period': 1,
        'page': 0,
        'per_page': 10,
        'text': search_query
    }

    response = requests.get(url, params=params)
    vacancies = response.json().get('items', [])

    detailed_vacancies = []
    for vacancy in vacancies:
        vacancy_details = requests.get(f"https://api.hh.ru/vacancies/{vacancy['id']}").json()

        skills = ', '.join([skill['name'] for skill in vacancy_details.get('key_skills', [])])
        description = vacancy_details.get('description', 'Отсутствует')

        salary = vacancy_details['salary']
        salary_str = ''

        if salary is not None:
            salary = utils.convert_salary(salary)
            if salary['from'] is not None and salary['to'] is not None:
                salary_str = f"{salary['from']} - {salary['to']}"
            elif salary['from'] is not None:
                salary_str = f"{salary['from']}"
            elif salary['to'] is not None:
                salary_str = f"{salary['to']}"
        else:
            salary_str = None

        detailed_vacancies.append({
            'name': vacancy_details['name'],
            'description': utils.clean_html_tags(description),
            'skills': skills,
            'company': vacancy_details['employer']['name'],
            'salary': salary_str,
            'region': vacancy_details['area']['name'],
            'published_at': vacancy_details['published_at'],
        })

        detailed_vacancies.sort(key=lambda x: datetime.strptime(x['published_at'], "%Y-%m-%dT%H:%M:%S%z"), reverse=True)

    for vacancy in detailed_vacancies:
        vacancy['published_at'] = utils.format_publication_date(vacancy['published_at'])

    return render(request, 'latest_jobs.html', {
        'vacancies': detailed_vacancies
    })
