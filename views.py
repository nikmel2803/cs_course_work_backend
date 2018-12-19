from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import uuid

import json

dbFile = open("db.json", "r", encoding="utf8")
db = json.loads(dbFile.read())
dbFile.close()


def find_employee(login, password):
    if not (login and password):
        return None
    for org in db:
        for employee in org['employees']:
            if employee.get('login') == login and employee.get('password') == password:
                return employee
    return None


def sign_in(request):
    login = request.GET.get('login')
    password = request.GET.get('password')
    if login == 'admin' and password == 'adminqwerty':
        admin = {
            "login": 'admin',
            "first_name": '',
            "password": 'adminqwerty',
            "last_name": '',
            "patronymic": '',
            "birthday": '',
            "position": '',
            "access": 0,
            "sex": 1,
            "org_id": ''
        }
        return JsonResponse(admin)
    user = find_employee(login, password)

    if user is None:
        return HttpResponse(status=401)

    return JsonResponse(user)


def get_data(request):
    login = request.GET.get('login')
    password = request.GET.get('password')
    if login == 'admin' and password == 'adminqwerty':
        org_id = request.GET.get('orgId')
        for org in db:
            if org.get('id') == org_id:
                return JsonResponse(org)
    org = find_org_by_employee(login, password)

    if org is None:
        return HttpResponse(status=401)
    return JsonResponse(org)


def find_org_by_employee(login, password):
    if not (login and password):
        return None
    for org in db:
        for employee in org['employees']:
            if employee.get('login') == login and employee.get('password') == password:
                return org
    return None


@csrf_exempt
def save_org(request):
    data = json.loads(request.body)
    login = data.get('login')
    password = data.get('password')
    user = find_employee(login, password)

    if user is None and login != 'admin' and password != 'adminqwerty':
        return HttpResponse(status=401)
    orgData = data.get('orgData')
    for i in range(len(db)):
        if db[i].get('id') == orgData.get('id'):
            db[i] = orgData
    save_db()
    return HttpResponse(status=200)


@csrf_exempt
def register_org(request):
    data = json.loads(request.body)
    org_id = str(uuid.uuid4())
    user = {
        "login": data.get('login'),
        "first_name": data.get('first_name'),
        "password": data.get('password'),
        "last_name": data.get('last_name'),
        "patronymic": data.get('patronymic'),
        "birthday": data.get('birthday'),
        "position": "Глава компании",
        "access": 0,
        "sex": data.get('sex'),
        "org_id": org_id
    }
    org_data = data.get('orgData')
    org = {
        "id": org_id,
        "name": org_data.get('name'),
        "description": org_data.get('description'),
        "founding_date": org_data.get('founding_date'),
        "address": org_data.get('address'),
        "head": data.get('login'),
        "car_park": [],
        "employees": [user]
    }
    db.append(org)
    save_db()
    return HttpResponse(status=200)


def save_db():
    dbFile = open("db.json", "w", encoding="utf8")
    dbFile.write(json.dumps(db, ensure_ascii=False))
    dbFile.close()