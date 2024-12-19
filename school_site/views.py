from django.shortcuts import render

def home(request):
    context = {'school_name' : "DevSkill",
               'user_name' : "Älice",
               'subjects': ['Benglai', 'Science', 'English'],
               'regestration_open': True
            }
    if request.method == 'POST':
        helper_method()
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        email = request.POST.get('email')
        context.update({'user_name' : f"{first_name} {last_name}",})
        context.update({'email' : email,})
        return render(request, 'homepage.html', context=context)
    return render(request, 'homepage.html', context=context)

def helper_method(pram, Param1: str = 'abcd'):
    print('helper method!')

def about(request):
    return render(request, 'about.html')
