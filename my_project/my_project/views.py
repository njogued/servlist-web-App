from django.http import HttpResponse

# @app.route('/')


def index(request):
    return HttpResponse("this is the home page")
