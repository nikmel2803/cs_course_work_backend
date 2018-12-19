from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import uuid

import json

dbFile = open("db.json", "r", encoding="utf8")
db = json.loads(dbFile.read())
dbFile.close()

usersFile = open("users.json", "r", encoding="utf8")
users = json.loads(usersFile.read())
usersFile.close()


def find_user(login):
    for user in users:
        if user.get('login') == login:
            return user
    return None


def get(request):
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


def get_data(user):
    company = find_company(user.get('company'))
    if user.get('access') == 0:
        array = [company]
        result = dict(organizations=array)
        return JsonResponse(result)


def post(request):
    return HttpResponse("Hello, world!")


def check_user(login, password):
    if not (login and password):
        return None
    user = find_user(login)
    if user is None or user.get('password') != password:
        return None
    return user


def sign_in(request):
    login = request.GET.get('login')
    password = request.GET.get('password')
    user = check_user(login, password)

    if user is None:
        return HttpResponse(status=401)

    return JsonResponse(user)


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
def sign_up(request):
    data = json.loads(request.body)
    orgId = str(uuid.uuid4())
    userId = str(uuid.uuid4())
    user = {
        "id": userId,
        "login": data.get('login'),
        "first_name": data.get('first_name'),
        "password": data.get('password'),
        "last_name": data.get('last_name'),
        "patronymic": data.get('patronymic'),
        "birthday": data.get('birthday'),
        "position": "Глава компании",
        "access": 0,
        "sex": data.get('sex'),
        "company": orgId
    }
    org_data = data.get('orgData')
    org = {
        "id": orgId,
        "name": org_data.get('name'),
        "description": org_data.get('description'),
        "founding_date": org_data.get('founding_date'),
        "address": org_data.get('address'),
        "head": userId,
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
