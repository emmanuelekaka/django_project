from django.shortcuts import render, redirect
from . forms import *
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required




def home(request):
    return render(request, "home.html")


def login(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)

            if user.status == 'Student':
                if Student.objects.filter(user_id=user.id):
                    return redirect('student_profile')
                else:
                    return redirect('student_register')
            else:
                if Alumin.objects.filter(user_id=user.id):
                    return redirect('alumin_profile')
                else:
                    return redirect('alumin_register')
            
        else:
            messages.info(request, "The email and password donot match")
            return redirect('login')

    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return render(request, "register.html", {'form':form})
    else:
        return render(request, "register.html", {'form':form})




@login_required(login_url='login')
def alumin_register(request  ,*args, **kwargs):
    form = AluminForm()
    context={'form':form}
    if request.method=='POST':
        form = AluminForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user= request.user
            instance.save()
            return redirect('alumin_profile')
        else:
            messages.info(request, "The email and password donot match")
            return render(request,'alumin/register2.html', context)

    
    return render(request,'alumin/register2.html', context)




@login_required(login_url='login')
def alumin_profile(request):
    
    data = Alumin.objects.get(user_id=request.user.pk)
    data={'data':data}

    return render(request, 'alumin/profile.html',  data)

def alumin_update(request, pk):
    
    info = Alumin.objects.get(id=pk)
    form = AluminForm(instance=info)

    if request.method=='POST':
        form = AluminForm(request.POST, instance=info)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user= request.user
            instance.save()
            return redirect('alumin_profile')
    context={'form':form}
    return render(request,'alumin/update.html', context)






@login_required(login_url='login')
def student_profile(request):
    
    data = Student.objects.get(user_id=request.user.pk)
    data={'data':data}

    return render(request, 'student/profile.html',  data)


@login_required(login_url='login')
def student_register(request  ,*args, **kwargs):
    form = StudentForm()
    if request.method=='POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user= request.user
            instance.save()
            return redirect('student_profile')
    
    context={'form':form}
    return render(request,'student/register2.html', context)



def student_update(request, pk):
    
    info = Student.objects.get(id=pk)
    form = StudentForm(instance=info)

    if request.method=='POST':
        form = StudentForm(request.POST, instance=info)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user= request.user
            instance.save()
            return redirect('student_profile')
    context={'form':form}
    return render(request,'student/update.html', context)  
