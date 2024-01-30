from django.shortcuts import render
from http import HTTPStatus

def csrf_failure(request, reason=''):
    return render(request, 'core/403.html')

def page_not_found(request, exeption):
    context = {
        'path' : request.path
    }
    return render(request, 'core/404.html', context, status=HTTPStatus.NOT_FOUND )