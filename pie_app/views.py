from django.shortcuts import render,redirect
from . import models
from django.contrib import messages
import bcrypt

# The main page of login and registration
def main(request):
    return render(request ,'main_page.html')


#Signup Method
def register(request):
    if request.method == 'POST':
        errors = models.User.objects.signup_validator(request.POST)
        if len(errors) > 0:
            for k , value in errors.items():
                messages.error(request , value)
            return redirect('/')
        else:
            new_user = models.create_user(first_name=request.POST['first_name'] , last_name=request.POST['last_name'] , email=request.POST['email'] , password=request.POST['password'] )
            request.session['email'] = request.POST['email']
            request.session['id'] = new_user.id
            return redirect('/dashboard')
    else:
        return redirect('/')


#Login Method
def validate_login(request):
    if request.method == 'POST':
        warnings = models.User.objects.login_validator(request.POST)
        if len(warnings) > 0:
            for k , value in warnings.items():
                messages.warning(request , value)
            return redirect('/')
        else:
            user = models.view_user(email=request.POST['email'])
            request.session['email'] = user.email
            request.session['id'] = user.id
        return redirect('/dashboard')
        
    else:
        return redirect('/')



# Dashboard Page Method
def pies(request):
    if 'email' not in request.session:
        return redirect('/')
    else:
        context = {
            'user' : models.view_user(email = request.session['email'])
        }
        return render(request , 'dashboard.html' , context)

#Create pie Method
def create_pie(request):
    if request.method == 'POST':
        infos = models.User.objects.pie_validator(request.POST)
        if len(infos)>0 : 
            for k ,value in infos.items():
                messages.info(request , value)
            return redirect('/dashboard')
        else:
            models.create_pie(name = request.POST['name'] , filling = request.POST['filling'] , crust = request.POST['crust'] , users = models.user_info(id = request.session['id']) )
            return redirect('/dashboard')

#edit pie info
def edit_pie(request , id):
    context = {
        'pie':models.view_pie(id = id)
    }
    return render(request , 'edit.html' , context)

#the method through which the update info will be passed 
def update_pie(request , id):
    if request.method == 'POST':
        infos = models.User.objects.pie_validator(request.POST)
        if len(infos)>0 : 
            for k ,value in infos.items():
                messages.info(request , value)
            return redirect('/pies/edit/'+str(id))
        else:
            models.update_pie(id = id , name = request.POST['name'] , filling= request.POST['filling'] , crust = request.POST['crust'])
            return redirect('/dashboard')



#Method that shows all pies in the database
def all_pies(request):
    context = {
        'pies':models.all_pies()
    }
    return render (request , "all_pies.html",context )


#a method to delete pie info
def delete_pie(request,id):
    pie = models.view_pie(id = id)
    if pie.users.id == request.session['id']:
        models.delete_pie(id=id)
        return redirect('/dashboard')
    else:
        return redirect('/dashboard')


#Method that renders the voting and the pie info page
def info(request , id):
    context = {
        "pie": models.view_pie(id = id)
    }
    return render(request , 'pie_info.html' , context )



#method that clears all sessions and return to login and registration page
def logout(request):
    request.session.clear()
    return redirect('/')


#methods for voting 
def voteplus(request , id):
    models.increase_vote(id=id)
    request.session['vote'] = 1
    return redirect('/voteminus/'+str(id))

def voteminus(request , id):
    context = {
        'pie' : models.view_pie(id = id)
    }
    return render(request , 'voteminus.html', context)

def remove_vote(request , id):
    models.decrease_vote(id = id)
    return redirect('/pies')
