from django.shortcuts import render

def online(request):
    return render(request, 'all.html')

def main(request):
    return render(request, 'main.html')