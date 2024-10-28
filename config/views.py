from django.shortcuts import render

def home(request):
    context = {
        'project_title': "Finance Manager Wep Application Team1",
        'github_url': "https://github.com/grace287/finance-wep-app ",
    }
    return render(request, 'home.html', context)
