import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.shortcuts import render
from .forms import UserForm, UserProfileInfoForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import request
from django.conf import settings
from .models import UserProfileInfo
userss = User.objects.filter(is_superuser = False)
user_list = []
for i in userss:
    user_list.append(i.username)

# uuser = User.objects.get(username=request.user.username)
# print(user)


def index(request):
    # username = request.POST.get('username')
    #print(username,"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    return render(request, 'users/index.html', {"All_users": user_list})


@login_required
def special(request):
    return HttpResponse("You are logged in !")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                print('found it')
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request, 'users/registration.html',
                  {'user_form': user_form,
                           'profile_form': profile_form,
                           'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                print(username)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(
                username, password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'users/login.html', {})


def c_index(request):
    return render(request, 'chat/index.html', {})

@login_required
def mainroom(request, usr_id):

    img_url="https://felixora-dev.herokuapp.com"
    user_obj = UserProfileInfo.objects.get(user_id=usr_id)
    if(user_obj.profile_pic):
        usr_p_url = img_url + user_obj.profile_pic.url
    else:
        usr_p_url = img_url+'/media/profile_pics/user.png'
    usr_status = user_obj.about

    userss = User.objects.filter(is_superuser = False)
    list_of_contact=[]
    for i in userss:
        user_obj = UserProfileInfo.objects.get(user_id=i.id)
        if int(i.id) != int(usr_id):
            name = i.username
            if(user_obj.profile_pic):
                contact_p_url = img_url + user_obj.profile_pic.url
            else:
                contact_p_url = img_url+'/media/profile_pics/user.png'
            contact_about = user_obj.about
            contact_detail = {
                'name':name,
                'profile_pic':contact_p_url,
                'status':contact_about,
            }
            list_of_contact.append(contact_detail)
    return render(request, 'chat/room.html', {
        'username': mark_safe(json.dumps(request.user.username)),
        'usr_img': usr_p_url,
        'usr_status':usr_status,
        'contact_list':list_of_contact,
    })





@login_required
def room(request, room_name, usr_id):
    img_url=settings.SITE_URL
   
    reciver_id_obj = User.objects.get(username=room_name)
    reciever_id = reciver_id_obj.id
    ar = []
    ar.append(str(reciever_id))
    ar.append(str(usr_id))
    ar.sort()    
    room_id = "^".join(ar)
    
    user_obj = UserProfileInfo.objects.get(user_id=usr_id)
    if(user_obj.profile_pic):
        usr_p_url = img_url + user_obj.profile_pic.url
    else:
        usr_p_url = img_url+'/media/profile_pics/user.png'
    usr_status = user_obj.about
    
    rec_obj = UserProfileInfo.objects.get(user_id=reciever_id)
    if(rec_obj.profile_pic):
        rec_p_url = img_url + rec_obj.profile_pic.url
    else:
        rec_p_url = img_url+'/media/profile_pics/user.png'
    rec_status =rec_obj.about
    userss = User.objects.filter(is_superuser = False)
    list_of_contact=[]
    for i in userss:
        user_obj = UserProfileInfo.objects.get(user_id=i.id)
        if int(i.id) != int(usr_id):
            name = i.username
            print(name)
            if(user_obj.profile_pic):
                contact_p_url = img_url + user_obj.profile_pic.url
            else:
                contact_p_url = img_url+'/media/profile_pics/user.png'
            contact_about = user_obj.about
            contact_detail = {
                'name':name,
                'profile_pic':contact_p_url,
                'status':contact_about,
            }
            list_of_contact.append(contact_detail)
    print(list_of_contact)
    return render(request, 'chat/roomContent.html', {
        'room_name_json': room_id,
        'room_id': room_id,
        'username': mark_safe(json.dumps(request.user.username)),
        'usr_img': usr_p_url,
        'usr_status':usr_status,
        'rec_img': rec_p_url,
        'rec_status':rec_status,
        'rec_name': room_name,
        'contact_list':list_of_contact,
    })
# from django.utils.crypto import get_random_string
# chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
# SECRET_KEY = get_random_string(50, chars)
# print (SECRET_KEY)