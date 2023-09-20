import argparse
import os
import time
import requests


def download_image(url_synchronous):
    """Функция, которая скачивает изображения с заданного URL-адреса(и выводит время работы в консоль)"""
    if not os.path.exists('images'):
        os.mkdir('images')
    start_time = time.time()
    name = url_synchronous.split('/')[-1]
    resp = requests.get(url_synchronous)
    if resp.status_code == 200:
        with open(f'images\\{name}', 'wb') as file:
            file.write(resp.content)
    print(f'время скачивания изображения({name}): {time.time() - start_time:.2f} сек.')


#  С помощью этого кода можно задавать список URL-адресов, через аргументы командной строки
start_time_all = time.time()

parser = argparse.ArgumentParser(description='Parser to start download_image')
parser.add_argument('-list', metavar='url', action='append', type=str, nargs='*', help='download_image sending URL')

args = parser.parse_args()

for url in args.list[0]:
    download_image(url)

print(f'Общее времени выполнения программы: {time.time() - start_time_all:.2f}')
# итак инструкция :)
# python .\ArgumentParser.py -list 'тут (в кавычках) вводим адрес, с которого требуется скачать изображение!'
# через запятую можем передавать список адресов для скачивания изображений 'первый URL', 'второй URL', 'третий URL'
# пример ввода: python .\ArgumentParser.py -list 'https://w.forfun.com/fetch/25/25288deb7f076b5dd9d48ce41ad4f558.j
# peg', 'https://static.tildacdn.com/tild3936-3265-4837-b530-626633666435/_1__.png', и т.д
# Копируем команду в консоль, жмем Enter и парсер стартует !
# Флаг -list это и есть(список) URL адресов до изображения, так-же можно передать один адрес.
