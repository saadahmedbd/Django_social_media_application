from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from . models import Room , Topic, Message
from . forms import RoomForm
from django.contrib.auth.models import User
from django.contrib import messages # type: ignore
from django.contrib.auth import authenticate, login, logout # type: ignore
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm # for register page form

#object render korbo views and template ar maddome
# rooms =[
#     {'id':1,"name":"let's learn python"},
#     {'id':2,"name":"let's learn java"},
#     {"id":3,"name":"let's learn javaScript"},
# ]
def loginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect ('home')
    if request.method == "POST":
        username=request.POST.get('username')
        password =request.POST.get('username')

        try:
            user=User.objects.get(username=username).lower()
        except:
            messages.error(request,"user invalid")
        
        user= authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect ('home')
        else:
            messages.error(request,"useranme or password is invalid")

    context={'page':page}
    return render(request, 'base/login_register.html', context)

def  logoutPage(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form =UserCreationForm()

    if request.method =="POST":
        form =UserCreationForm(request.POST)
        if form.is_valid():
           user=form.save(commit=False)
           user.username=user.username.lower()
           user.save()
           login(request,user)
           return redirect('home') 
        else:
            messages.error(request, 'an error occured during registration')
    return render (request, 'base/login_register.html', {'form':form})

def home(request):
    q=request.GET.get('q') if request.GET.get('q') != None else '' # always home page have data

    rooms =Room.objects.filter(
    Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q))# data filter kora holo and icontains through if you write half word django give you data
    # you are import data from admin panel and admin panel data from import models
    
    topics= Topic.objects.all()
    room_count =rooms.count()
    room_messages =Message.objects.filter(Q(room__topic__name__icontains=q)) # filter room message by room topic
    context={'rooms':rooms , 'topics':topics, "room_count":room_count, 'room_messages':room_messages}
    return render(request, 'base/home.html', context)



def room (request,pk):
    #render data home to room
    # room=None
    # for i in rooms:
    #     if i['id'] ==int (pk):
    #         room=i
    

    room =Room.objects.get(id=pk)
    room_messages=room.message_set.all()
    participants=room.participants.all()
    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id) 
    context ={'room':room, 'room_messages':room_messages , 
              'participants':participants}
    return render(request,"base/room.html", context)

def profile (request, pk):
    
    user =User.objects.get(id=pk)
    rooms =user.room_set.all() # only show which user profile you want to check that user room contain you can see
    topics= Topic.objects.all()
    room_messages =user.message_set.all() # only show which user profile you want to check that user message you can see

    context={'user':user, 'rooms':rooms ,'topics':topics, 'room_messages':room_messages}
    return render (request, 'base/profile.html', context)

@login_required(login_url='login')
def createRoom(request):
    form =RoomForm()
    if request.method == "POST":
        form =RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render (request, "base/room_form.html", context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room =Room.objects.get(id=pk)
    form=RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("you are not a user")

    if request.method == "POST":
        form =RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect ('home')
    context={'form':form}
    return render (request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room =Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("you are not a user")


    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render (request, "base/delete.html", {'obj':room})

@login_required(login_url='login')
def deleteMessage(request, pk):
    message =Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse("your are not allowed here")


    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render (request, "base/delete.html", {'obj':message})