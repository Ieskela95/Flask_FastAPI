from fastapi import FastAPI, Request
import logging
from typing import Optional
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

FORMAT = '{levelname:<8} - {asctime} - >>> {msg}'
logging.basicConfig(format=FORMAT, style='{', level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
templates = Jinja2Templates(directory="./home_work/home_work_5/templates")

# Для каждой конечной точки необходимо проводить валидацию данных запроса и ответа.
# Для этого использовать библиотеку Pydantic.


class Task(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[bool] = False
#     Для каждой задачи должна быть возможность указать статус (выполнена/не выполнена).
#     По умолчанию не выполнена!


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    logger.info('Отработал GET запрос(Главная страница).')
    return templates.TemplateResponse("item.html", {"request": request})


@app.get('/tasks/')
async def all_tasks():
    logger.info('Отработал GET запрос(прочитал БД и вывел все задачи).')
    return {'реализация с БД на FastAPI еще не проходили': 'создал конечные точки, согласно условиям задачи'}


@app.get('/tasks/{id_}')
async def returns_task(id_: int):
    logger.info(f'Отработал GET запрос(вернул задачу с id = {id_}).')
    return {f'реализация с БД еще не проходили': f'создал конечные точки, согласно условиям задачи. GET_task = {id_}'}


@app.post("/tasks/")
async def create_task(task: Task):
    logger.info('Отработал POST запрос(добавил новую задачу).')
    return {"POST_new_task": task}


@app.put("/tasks/{task_id}")
async def update_task(task_id: int, task: Task):
    logger.info(f'Отработал PUT запрос(обновил задачу с id = {task_id}).')
    return {"PUT_task_id": task_id, "task": task}


@app.delete('/tasks/{task_id}')
async def delete_item(task_id: int):
    logger.info(f'Отработал DELETE запрос (удалил задачу с id = {task_id}).')
    return {'DELETE_task_id': task_id}


# протестировал все конечные точки используя документацию: http://127.0.0.1:8000/docs
# для запуска приложения ввести команду:
# uvicorn lection.lection_5.lection.main:app --reload  (если стартовать из корня проекта)
# ОБРАТИТЕ ВНИМАНИЕ ТОЧЕЧНАЯ НАТАЦИЯ, не слеш ! отсутствие разрешения .py у файла 'main'
# либо из этой директории исполняемого файла, командой: uvicorn main:app --reload
# (main название файла app название переменной FastAPI)
