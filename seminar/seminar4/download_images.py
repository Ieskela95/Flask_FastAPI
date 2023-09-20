import os.path
import time
import requests
import asyncio
import threading

url1 = 'https://w.forfun.com/fetch/25/25288deb7f076b5dd9d48ce41ad4f558.jpeg'
url2 = 'https://static.tildacdn.com/tild3936-3265-4837-b530-626633666435/_1__.png'
url3 = 'https://pythonturbo.ru/wp-content/uploads/2022/12/output-1024x544.png'
list_url = [url1, url2, url3]

start_time_all = time.time()


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


for url_ in list_url:
    download_image(url_)
print(f'(Итог)время работы программы(синхронный): {round(time.time() - start_time_all, 2)} сек.\n')


async def download_image_async(url_async):
    """Асинхронный подход"""
    start_time = time.time()
    name = url_async.split('/')[-1]
    resp = requests.get(url_async)
    if resp.status_code == 200:
        with open(f'images\\{name}', 'wb') as file:
            file.write(resp.content)
    print(f'(async)время скачивания изображения({name}): {time.time() - start_time:.2f} сек.')


async def main():
    """Функция, для асинхронной работы download_image_async"""
    tasks = []
    for url_tasks in list_url:
        tasks.append(asyncio.ensure_future(download_image_async(url_tasks)))
    await asyncio.gather(*tasks)


start_time_all = time.time()
asyncio.run(main())
print(f'(Итог)время работы программы(с async): {round(time.time() - start_time_all, 2)} сек.\n')

# многопоточный подход

threads = []
start_time_all = time.time()
for url in list_url:
    thread = threading.Thread(target=download_image, args=[url])
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
print(f'(Итог)время работы программы(многопоточный): {round(time.time() - start_time_all, 2)} сек.\n')
