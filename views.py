from django.http import HttpResponse
from django.http import JsonResponse

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
        print(comp)
        if comp.get('id') == id:
            return comp
    return None


def get_data(user):
    company = find_company(user.get('company'))
    if user.get('access') == 0:
        print(company)
        return JsonResponse(company)


def post(request):
    return HttpResponse("Hello, world!")


def check_user(login, password):
    if not (login and password):
        return None
    user = find_user(login)
    if user is None or user.get('password') != password:
        return None
    return user


def signIn(request):
    login = request.GET.get('login')
    password = request.GET.get('password')
    user = check_user(login, password)

    if user is None:
        return HttpResponse(status=401)

    return JsonResponse(user)
