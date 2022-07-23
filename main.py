'''
парсер для анонсов мероприятий Свердловской области
'''

import requests
from bs4 import BeautifulSoup


url = 'https://www.све.рф'
response = requests.get(f'{url}/smi/announcement')

# Создаем суп для разбора html
soup = BeautifulSoup(response.text, 'html.parser')

anons_link_div = soup.find_all('a', class_='news_link')         # Найдем все ссылки с заголовками новостей

#print(anons_link_div)
#print(type(news_link_div))
#print(news_link_div.get('class'))


# ======Выведем все заголовки новстей и ссылки на страницы:========
i = 0
for record in anons_link_div:
    i += 1
    news = record.find('div', class_='news_link--title')
    news_link = record.get('href')
    print(f'\n{i}. {news.text}. ссылка: {news_link}')
    news_page = requests.get(f'{url}{news_link}')
    #print(f'   Статус странцы: {news_page.status_code}')

    soup_news = BeautifulSoup(news_page.text, 'html.parser')    # варим суп из страницы новости
    title_news = soup_news.find('h1')       # получим заголовок новости
    print(title_news.text)
    data_news = soup_news.find('div', class_='article--info')
    print(data_news.text)
    content_news = soup_news.find('div', class_='content')
    print(content_news.text)

# =================================================================

print('-*-*-*-*-*-*- Конец *-*-*-*--*--*-*-')
