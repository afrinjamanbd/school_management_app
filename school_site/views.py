from django.shortcuts import render

def home(request):
    context = {'school_name' : "DevSkill",
               'user_name' : "Älice",
               'subjects': ['Bengla', 'Science', 'English'],
               'registration_open': True,
               
            }
    
    return render(request, 'homepage.html', context=context)

def about(request):
    return render(request, 'about.html')
