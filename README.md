# tutor-smith

Name still to be defined

````shell
Start the server:
~$ python3 manage.py runserver
````
---
## Setting up
### Packages
Requirements:
* python3 >= 3.8
* pip3
* packages from requirements.txt
* packages from requirements-dev.txt if you're a developer

````shell
~$ pip install -r requirements.txt
````
### Precommit Hooks
precommit hooks are important to guarantee merges with less conflicts.
**installation**
make sure you have installed the packages from requirements-dev.txt
````shell
~$ pre-commit install
pre-commit installed at .git/hooks/pre-commit

~$ pre-commit run --all-files
````
if one of the hooks fail, just add & commit again

---

## Adding new content
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
## The Database
**Important:** The *Name* Field is now seperated in *first_name* and *last_name*
### Basics
If you make changes to the Database please run
````shell
~$ python3 manage.py makemigrations
~$ python3 manage.py migrate
````
**Don't forget to inform the others of your changes**
</br>
### Read and write to / from the Database
```python
# Read
# SQL: SELECT * FROM User WHERE email = email
User.objects.filter(email=email) # -> Returns None on empty Querry

# SQL: SELECT * FROM User WHERE name LIKE '%a'
User.objects.filter(email__startswith="a")

# Selecting a single Object
User.objects.get(email=email) # -> Raises an DoesNotExist Exeption on empty Querry
````
[more infos here](https://docs.djangoproject.com/en/3.2/topics/db/queries/#retrieving-all-objects)
````python
# Write
# Create a new User with the email test@test
User.objects.create(email="test@test")

# Update an Object
u1.email = "test2@test" # u1 is an already existing User
u1.save()
````
---
## Additional Information
* The secret key has to be [generated](https://djecrety.ir/) or is given by an Administrator.
Store it in the base directory as **SECRET_KEY.txt**
