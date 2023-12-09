from django.shortcuts import render

def me(request):
    template = 'about/me.html'
    title = 'Об авторе'
    context = {
        'title': title
    }
    return render(request, template, context)

def tech(request):
    template = 'about/tech.html'
    title = 'О проекте'
    context = {
        'title': title
    }
    return render(request, template, context)