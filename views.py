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
    user = find_employee(login, password)

    if user is None:
        return HttpResponse(status=401)

    return JsonResponse(user)


def get_data(request):
    login = request.GET.get('login')
    password = request.GET.get('password')
    user = check_user(login, password)

    if user is None:
        return HttpResponse(status=401)
    return get_data(user)


def find_company(id):
    for comp in db:
        if comp.get('id') == id:
            employees = list()
            for user in users:
                if user.get('company') == comp.get('id'):
                    employees.append(user)
            comp['employees'] = employees
            return comp
    return None


def get_company_data(user):
    company = find_company(user.get('company'))
    if user.get('access') == 0:
        array = [company]
        result = dict(organizations=array)
        return JsonResponse(result)


@csrf_exempt
def save_org(request):
    data = json.loads(request.body)
    login = data.get('login')
    password = data.get('password')
    user = check_user(login, password)

    if user is None:
        return HttpResponse(status=401)
    orgData = data.get('orgData')
    for i in range(len(db)):
        if db[i].get('id') == orgData.get('id'):
            try:
                del orgData["employees"]
            except KeyError:
                print("Key 'employees' not found")
            db[i] = orgData
    save_db()
    return HttpResponse(status=200)


@csrf_exempt
def register_org(request):
    data = json.loads(request.body)
    org_id = str(uuid.uuid4())
    user_id = str(uuid.uuid4())
    user = {
        "id": user_id,
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
        "head": user_id,
        "car_park": [],
        "employees": []
    }
    users.append(user)
    db.append(org)
    save_db()
    save_users()
    return HttpResponse(status=200)


def save_db():
    dbFile = open("db.json", "w", encoding="utf8")
    dbFile.write(json.dumps(db, ensure_ascii=False))
    dbFile.close()


def save_users():
    usersFile = open("users.json", "w", encoding="utf8")
    usersFile.write(json.dumps(users, ensure_ascii=False))
    usersFile.close()
