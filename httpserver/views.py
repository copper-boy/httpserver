import os
import shutil

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpRequest, FileResponse, HttpResponseNotFound
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

from sql_manager import SqlConnectionManager


# главная страница
def index(request: HttpRequest):
    if request.method == 'GET':
        file = request.GET.get('file')
        table = request.GET.get('table')
        if file:
            if table:
                return HttpResponse(';'.join(os.listdir(f'excel/{file.split(".")[0]}')))
            return HttpResponse(';'.join(os.listdir('sql')))
    return render(request, 'index.html')


# удаление db и xlsx файла
@csrf_exempt
def delete(request: HttpRequest, file_name):
    os.remove(os.path.join('sql', file_name))
    shutil.rmtree(os.path.join('excel', file_name.split('.')[0]))
    return index(request)


# добавление db файла и создание excel файлов методом из sql_manager.py
@csrf_exempt
def post(request: HttpRequest):
    database_file = request.FILES['database']
    if database_file:
        FileSystemStorage(location='sql').save(database_file.name, database_file)
        SqlConnectionManager(database_file.name)
    return index(request)


# возвращаем файл, чтобы пользователь мог скачать его
def excel(request: HttpRequest, file: str, table: str):
    if os.path.exists(f'excel/{file.split(".")[0]}/{table}'):
        return FileResponse(open(f'excel/{file.split(".")[0]}/{table}', 'rb'))
    else:
        return HttpResponseNotFound('File doesnt exists')
