from django.shortcuts import render

def index(request):
    print('index 화면 진입')
    return render(request , 'index.html')
    