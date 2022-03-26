import requests
import string
import os

from bs4 import BeautifulSoup


translator = str.maketrans('', '', string.punctuation + '—’')
working_directory = os.getcwd()

number_of_pages = int(input())
article_type = input()

for i in range(1, number_of_pages + 1):
    r = requests.get('https://www.nature.com/nature/articles?sort=PubDate&year=2020&page=' + str(i))
    soup = BeautifulSoup(r.content, 'html.parser')

    os.mkdir(working_directory + '\\Page_' + str(i))
    os.chdir('Page_' + str(i))

    for j in soup.find_all('article'):
        if j.find('span', {'data-test': 'article.type'}).text.strip() == article_type:
            article = j.find('a', {'data-track-action': 'view article'})
            article_title = article.text.translate(translator).replace(' ', '_').replace('__', '_') + '.txt'
            article_link = article.get('href')

            r_2 = requests.get('https://www.nature.com' + article_link)
            soup_2 = BeautifulSoup(r_2.content, 'html.parser')

            with open(article_title, 'w', encoding='utf-8') as f:
                f.write(soup_2.find('div', {'class': 'c-article-body u-clearfix'}).text.strip())

    os.chdir(working_directory)

print('Saved all articles.')
