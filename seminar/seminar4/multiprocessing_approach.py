import os
from multiprocessing import Process
import time
import requests

url1 = 'https://w.forfun.com/fetch/25/25288deb7f076b5dd9d48ce41ad4f558.jpeg'
url2 = 'https://static.tildacdn.com/tild3936-3265-4837-b530-626633666435/_1__.png'
url3 = 'https://pythonturbo.ru/wp-content/uploads/2022/12/output-1024x544.png'
list_url = [url1, url2, url3]


def download_image(url):
    """Функция, которая скачивает изображения с заданного URL-адреса(и выводит время работы в консоль)"""
    if not os.path.exists('images'):
        os.mkdir('images')
    start_time = time.time()
    name = url.split('/')[-1]
    resp = requests.get(url)
    if resp.status_code == 200:
        with open(f'images\\{name}', 'wb') as file:
            file.write(resp.content)
    print(f'время скачивания изображения({name}): {time.time() - start_time:.2f} сек.')


#  многопроцессорный подход (сделал отдельный файл, т.к он требует особого подхода)
processes = []
start_time_all = time.time()

if __name__ == '__main__':
    for url_processes in list_url:
        process = Process(target=download_image, args=(url_processes,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
    print(f'(Итог)время работы программы(многопроцессорный): {round(time.time() - start_time_all, 2)} сек.\n')
