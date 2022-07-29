

import requests
from bs4 import BeautifulSoup
import pprint

def del_spec_symbols(data_string):  # вырежем лишние символы
    #print(rf'{data_string}')
    data_string = list(data_string)
    #print(f'Длина строки:{len(data_string[0])}, {data_string[0]}')
    new_data = data_string[0][7:-6]
    #print(rf'Новая дата:{new_data}***')
    return(new_data)

url = 'https://www.све.рф'
response = requests.get(f'{url}/smi/announcement')

# Создаем суп для разбора html
soup = BeautifulSoup(response.text, 'html.parser')

anons_link_div = soup.find_all('a', class_='news_link')         # Найдем все ссылки с заголовками новостей

#print(anons_link_div)
#print(type(news_link_div))
#print(news_link_div.get('class'))

last_news = []
# ======Выведем все заголовки новстей и ссылки на страницы:========
i = 0
for record in anons_link_div:
    i += 1
    news = record.find('div', class_='news_link--title')
    news_link = record.get('href')
        #print(f'\n{i}. {news.text}. ссылка: {news_link}')
    news_page = requests.get(f'{url}{news_link}')
    #print(f'   Статус странцы: {news_page.status_code}')
    soup_news = BeautifulSoup(news_page.text, 'html.parser')    # варим суп из страницы новости
    title_news = soup_news.find('h1')       # получим заголовок новости
        #print(title_news.text)
    data_news = soup_news.find('div', class_='article--info')
    clear_data = del_spec_symbols(data_news)    # Избавим дату от корявых тегов
        #print(f'Дата: {type(clear_data)}: {clear_data}')
    content_news = soup_news.find('div', class_='content')
        #print(content_news.text)
    # соберем новость в словарь:
    dict_from_news = {'Number': i, 'Data': clear_data, 'heading': title_news.text, 'link': f'{url}{news_link}', 'text': content_news.text}
    pprint.pprint(dict_from_news)
    last_news.append(dict_from_news)
# =================================================================
for news in last_news:
    pprint.pprint(news)
print('-*-*-*-*-*-*- Конец *-*-*-*--*--*-*-')
