from django.shortcuts import render,redirect
from django.contrib import messages 
from django.db.models import Q
from django.http import HttpResponse
from .models import Room,Topic,Message,User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .form import RoomForm,UserFrom,MyUserCreationForm

def loginUser(request):
    page='login'
    statusLogin=False
    messageLogin=''
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        email=request.POST.get('email','').strip().lower()
        password=request.POST.get('password','')

        try:
            user=User.objects.get(email=email)
        except:
            messageLogin='invlaid user!'
            statusLogin=True
        
        user=authenticate(request,email=email,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messageLogin=('Username OR password does not exit')
            statusLogin=True
    context={'page':page,'statusLogin':statusLogin,'messageLogin':messageLogin}
    return render(request,'login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    page='register'
    statusRegister=False
    messageRegister=""
    form=MyUserCreationForm()
    
    if request.method == 'POST':
        print(request.POST)  # Print the entire POST data in the terminal
        print("Username:", request.POST.get("username"))  # Print a specific field
        print("Email:", request.POST.get("email"))
        print("Password:", request.POST.get("password1"))
        form=MyUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.strip().lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            statusRegister=True
            messageRegister=('An error occurred during registration')
    context={'form':form,'page':page,'statusRegister':statusRegister,'messageRegister':messageRegister}
    return render(request,'login.html',context)

def home(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ''
    rooms=Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    room_count=rooms.count()
    topics=Topic.objects.all()
    room_messages=Message.objects.filter(Q(room__topic__name__icontains=q))
    context={'rooms':rooms,'topics':topics,'room_count':room_count,'room_messages':room_messages}
    return render(request,'home.html',context)

def room(request,pk):
    room=Room.objects.get(id=pk)
    room_messages=room.message_set.all()
    participants=room.participants.all()
    if request.method == 'POST':
        message=Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)
    context={'room':room,'room_messages':room_messages,'participants':participants}
    return render(request,'room.html',context)

def userProfile(request,pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()
    room_messages=user.message_set.all()
    topics=Topic.objects.all()
    context={'user':user,'rooms':rooms,'room_messages':room_messages,'topics':topics}
    return render(request,'profile.html',context)

@login_required(login_url='login')
def editUserProfile(request):
    user=request.user
    form=UserFrom(instance=user)
    if request.method == 'POST':
        form=UserFrom(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect('userProfile',pk=user.id)
    context={'form':form}
    return render(request,'user_profile.html',context)

@login_required(login_url='login')
def createRoom(request):
    form=RoomForm()
    topics=Topic.objects.all()
    header='Create Room'
    if request.method == "POST":
        topic_name=request.POST.get('topic')
        topic, created=Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')
    context={'form':form,'topics':topics,'header':header}
    return render(request,'room_form.html',context)

@login_required(login_url='login')
def updateRoom(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)
    topics=Topic.objects.all()
    header='Update Room'
    if request.user != room.host:
        return HttpResponse('Your not the host of this room!!')
    if request.method=="POST":
        topic_name=request.POST.get('topic')
        topic, created=Topic.objects.get_or_create(name=topic_name)
        room.name=request.POST.get('name')
        room.topic=topic
        room.description=request.POST.get('description')
        room.save()
        return redirect('home')
    context={'form':form,'topics':topics,'room':room,'header':header}
    return render(request,'room_form.html',context)

@login_required(login_url='login')
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request,'delete.html',{'obj':room}) 

@login_required(login_url='login')
def deleteMessage(request,pk):
    message=Message.objects.get(id=pk)
    
    if request.user != message.user:
        return HttpResponse('Your are not allowed to here')
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request,'delete.html',{'obj':message}) 
