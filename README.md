#tutor-smith

Name still to be defined

````console
Start the server:
~$ python3 manage.py runserver
````
---
###Setting up
Requirements:  
* python3 >= 3.8
* pip3
* packages from requirements.txt

````console
~$ pip install -r requirements.txt
````
---

###Adding new content
1. add the new site to the *app_name*/views.py
````python
def view_name(request):
    #Do something with data
    return render('template.html', context={"foo": "bar"})
````
2. register the url in tutor_smith/urls.py
````python
urlpatterns = [
    ...,
    path('url', app_name.view_name),
]
````
---
###Additional Information
* A simple "Hello World" view can be found under *localhost:8000/hello/*  
A "Hello World" view with templates can be found at *localhost:8000/hello-template/*
* The secret key has to be generated or is given by an Administrator.  
Store it in the base directory as **SECRET_KEY.txt**