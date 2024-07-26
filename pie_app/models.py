from django.db import models
import re
import bcrypt
from datetime import datetime

class UserManager(models.Manager):
    def signup_validator(self , postData):
        errors = {}
        if len(postData['first_name']) < 2 : 
            errors['first_name'] = 'First Name must be at least 2 characters '
        if len(postData['last_name']) < 2 : 
            errors['last_name'] = 'Last Name must be at least 2 characters '
        if len(postData['password']) < 8 : 
            errors['password'] = 'Password should be at least 8 characters'
        if postData['password'] != postData['confirmPassword'] :
            errors['cpw'] = 'Passwords do not match'
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):      
            errors['email'] = "Invalid email address!"
        if User.objects.filter(email = postData['email']).exists():
            errors['email'] = "Email already exists"
        return errors
    def login_validator(self , postData):
        warnings = {}
        if postData['email'] == '':
            warnings['email'] = 'Email field cant be empty'
        elif postData['password'] == '':
            warnings['password'] = 'Password field cant be empty'
        elif User.objects.filter(email = postData['email']).exists() == False : 
                warnings['email'] = "Email does not exist"
        else:
            if bcrypt.checkpw(postData['password'].encode(), view_user(email = postData['email']).password.encode()) == False :
                warnings['password'] = 'Incorrect Password'
        return warnings
    def pie_validator(self , postData):
        infos = {}
        if postData['name'] == '':
            infos['name'] = 'Please Fill the name field'
        elif postData['filling'] == '':
            infos['filling'] = 'Please fill the filling field'
        elif postData['crust'] == '':
            infos['crust'] = 'Please fill the Crust Field'
        else:
            if Pie.objects.filter(name = postData['name']).exists() == True:
                infos['name'] = 'Pie name already exists'
        return infos
    




class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length= 50)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Pie(models.Model):
    name = models.CharField(max_length=50)
    filling = models.CharField(max_length=255)
    crust = models.CharField(max_length=100)
    vote = models.IntegerField(null = True , default=int(0))
    users = models.ForeignKey(User , related_name='pies' , on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



def create_user(first_name , last_name , email , password ):
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    return User.objects.create(first_name = first_name , last_name = last_name , email = email , password = pw_hash)

def view_user(email):
    user = User.objects.get(email = email)
    return user

def user_info(id):
    user =User.objects.get(id=id)
    return user

def create_pie(name , filling , crust , users):
    return Pie.objects.create(name = name , filling = filling , crust = crust , users = users)

def view_pie(id):
    return Pie.objects.get(id = id)

def update_pie(id ,name , filling , crust):
    the_pie = view_pie(id=id)
    the_pie.name = name
    the_pie.filling = filling
    the_pie.crust = crust
    return the_pie.save()

def all_pies():
    return Pie.objects.all()

def delete_pie(id):
    the_pie =view_pie(id=id)
    return the_pie.delete()

def increase_vote(id):
    thepie = view_pie(id=id)
    thepie.vote = int(thepie.vote) +1
    return thepie.save()

def decrease_vote(id):
    thepie = view_pie(id=id)
    thepie.vote = int(thepie.vote) -1
    return thepie.save()