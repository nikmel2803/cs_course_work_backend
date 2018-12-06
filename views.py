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
        print(user)
        if user.get('login') == login:
            return user
    return None


def get(request):
    return HttpResponse("Hello, world!")


def post(request):
    return HttpResponse("Hello, world!")


def signIn(request):
    login = request.GET.get('login')
    password = request.GET.get('password')

    if not (login and password):
        return HttpResponse(status=400)
    user = find_user(login)

    if user is None:
        return HttpResponse(status=400)

    if user.get('password') == password:
        return JsonResponse(user)
    return HttpResponse(status=400)
