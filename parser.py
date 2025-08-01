import requests
from bs4 import BeautifulSoup
import json
import os

def parse_program(url, program_name):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        program_info = {
            'name': program_name,
            'description': soup.find('div', class_='program-page__desc').get_text(strip=True) 
                          if soup.find('div', class_='program-page__desc') else '',
            'subjects': []
        }
        
        # Более гибкий поиск раздела с дисциплинами
        subjects_section = None
        possible_sections = [
            soup.find('div', {'id': 'disciplines'}),
            soup.find('h2', string='Дисциплины'),
            soup.find('h2', string='Учебные дисциплины'),
            soup.find('h3', string='Дисциплины')
        ]
        
        for section in possible_sections:
            if section:
                subjects_section = section.find_next('div')
                break
        
        if subjects_section:
            subjects = subjects_section.find_all('div', class_='discipline-item') or \
                      subjects_section.find_all('div', class_='subject-item') or \
                      subjects_section.find_all('li')
            
            for subject in subjects:
                subject_name = subject.find('h3').get_text(strip=True) if subject.find('h3') else \
                              subject.find('span', class_='discipline-name').get_text(strip=True) if subject.find('span', class_='discipline-name') else \
                              'Неизвестно'
                subject_desc = subject.find('p').get_text(strip=True) if subject.find('p') else \
                               subject.find('div', class_='discipline-desc').get_text(strip=True) if subject.find('div', class_='discipline-desc') else \
                               ''
                program_info['subjects'].append({
                    'name': subject_name,
                    'description': subject_desc
                })
        
        os.makedirs('data', exist_ok=True)
        with open(f'data/{program_name.lower().replace(" ", "_")}_plan.json', 'w', encoding='utf-8') as f:
            json.dump(program_info, f, ensure_ascii=False, indent=2)
        
        return program_info
    
    except Exception as e:
        print(f"Ошибка при парсинге {program_name}: {str(e)}")
        return None

# Парсим данные
ai_url = "https://abit.itmo.ru/program/master/ai"
ai_product_url = "https://abit.itmo.ru/program/master/ai_product"

parse_program(ai_url, "Artificial Intelligence")
parse_program(ai_product_url, "AI Products")

print("Данные успешно сохранены!")