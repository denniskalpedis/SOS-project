# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from ..login_and_registration.models import Users
from django.http import HttpResponseForbidden
from .models import *
from .forms import *
import hashlib

from django.shortcuts import render, HttpResponse, redirect, reverse

# Create your views here.
def index(request):
    if 'login' not in request.session:
        return redirect('/')
    current_user = Users.objects.get(id=request.session["login"])
    if 'group' not in request.session and current_user.user_groups_joined.all().count()<1:
        return redirect('/sos/join')
    elif 'group' not in request.session:
        logged_in = Users.objects.filter(id=request.session['login'])
        current_group = logged_in[0].user_groups_joined.all()
        request.session["group"] = current_group[0].id
    current_group = BuyGroup.objects.get(id=request.session["group"])
    context = {
        "buygroup": current_group,
        "user": current_user,
        "items": current_group.items.all()
    }

    if current_user == current_group.admin or current_user in current_group.tas.all():
        context = {
            "buygroup": current_group,
            "user": current_user,
            "snacks": current_group.items.all()
        }
        return render(request, "sos/index_admin.html", context) 
    return render(request, "sos/index.html", context)

# def new(request):
#     if "login" not in request.session:
#         redirect("/")
#     return render(request, "sos/create.html")

def create(request):
    print 'errors'
    if 'login' not in request.session:
        return redirect('/')
    errors = BuyGroup.objects.validate(request.POST)
    if len(errors):
        for error in errors:
            messages.error(request, error)
        return redirect('sos/join')
    current_user = Users.objects.get(id=request.session["login"])
    name = request.POST['name']
    password = request.POST['password']
    new = BuyGroup.objects.create(name=name, password=password, admin=current_user)
    new.users.add(current_user)
    return redirect('/sos')

# def join(request, id = "None"):
#     current_user = Users.objects.get(id=request.session["login"])
#     group_buy = BuyGroup.objects.all().filter(name=id)
#     if "login" not in request.session:
#         redirect("/")
#     if request.method=="POST":
#         if request.POST["password"] == group_buy[0].password:
#             group_buy[0].users.add(current_user)
#             request.session['group'] = group_buy[0].id
#             return redirect('/')
#         return render(request, "sos/join.html")
#     else:
#         if id is None:
#             return redirect('/sos')
#         else:
#             if group_buy.count() < 1:
#                 messages.error(request, "No Group Named {}!".format(id))
#                 return redirect('/sos')
#             # if current_user in group_buy[0].users:
#             #     print "already a member"
#             #     return redirect('/sos')
#         context = {
#             "group":group_buy[0].name
#         }
#         return render(request, "sos/join.html", context)

#     return redirect('/sos')

def group(request, id):
    if 'login' not in request.session:
        return redirect('/')
    current_user = Users.objects.get(id=request.session["login"])
    group_buy = BuyGroup.objects.all().filter(id=id)
    if "login" not in request.session:
        redirect("/")
    if group_buy.count() < 1:
        messages.error(request, "No Group Named {}!".format(id))
        return redirect('/sos/group.html')
    if group_buy[0].admin == current_user:
        userlevel = "admin"
    elif BuyGroup.objects.all().filter(tas=current_user).count() > 0:
        userlevel = "ta"
    else:
        userlevel = "user"

    context = {
        "userlevel":userlevel,
        "group":group_buy[0]
    }
    return render(request, "sos/group.html", context)

def upgrade_user(request, user_id, group_id):
    if 'login' not in request.session:
        return redirect('/')
    current_user = Users.objects.get(id=request.session["login"])
    if 'group' not in request.session and current_user.user_groups_joined.all().count()<1:
        return redirect('/sos/join')
    group_buy = BuyGroup.objects.get(id=group_id)
    if current_user != group_buy.admin and current_user not in group_buy.tas.all():
        return redirect('/sos')
    current_user = Users.objects.get(id=request.session["login"])
    if "login" not in request.session:
        redirect("/")
    # if current_user == group_buy[0].admin:
    group_buy.tas.add(Users.objects.get(id=user_id))
    return redirect('/sos/admin/users')

def md5encode(key, group):
    return hashlib.sha256(key.encode()+group.encode()).hexdigest()

def joining(request):
    if 'login' not in request.session:
        return redirect('/')
    if request.method == "GET":
        return render(request, "sos/landing_page.html")
    elif request.method == "POST":
        if BuyGroup.objects.filter(name=request.POST['name']) < 1:
            return redirect('/sos/join')
        current_user = Users.objects.get(id=request.session["login"])
        group_name = request.POST["name"]
        group_buy = BuyGroup.objects.get(name=group_name)
        if request.POST["password"] == group_buy.password:
            group_buy.users.add(current_user)
            request.session["group"] = group_buy.id
            return redirect('/sos')
    current_user = Users.objects.get(id=request.session["login"])

def users(request):
    if 'login' not in request.session:
        return redirect('/')
    current_user = Users.objects.get(id=request.session["login"])
    if 'group' not in request.session and current_user.user_groups_joined.all().count()<1:
        return redirect('/sos/join')
    group = BuyGroup.objects.get(id=request.session['group'])
    if current_user != group.admin and current_user not in group.tas.all():
        return redirect('/sos')
    group_buy = BuyGroup.objects.all().filter(id=request.session['group'])
    context = {
        "user": current_user,
        "group":group_buy[0]
    }
    return render(request,'sos/users.html', context)

def downgrade_user(request, user_id, group_id):
    if 'login' not in request.session:
        return redirect('/')
    current_user = Users.objects.get(id=request.session["login"])
    if 'group' not in request.session and current_user.user_groups_joined.all().count()<1:
        return redirect('/sos/join')
    group_buy = BuyGroup.objects.get(id=group_id)
    if current_user != group_buy.admin and current_user not in group_buy.tas.all():
        return redirect('/sos')
    if "login" not in request.session:
        redirect("/")
    # if current_user == group_buy[0].admin:
    group_buy.tas.remove(Users.objects.get(id=user_id))
    #group_buy[0].tas.del(Users.objects.get(id=user_id))
    return redirect('/sos/admin/users')

def remove_user(request, user_id, group_id):
    if 'login' not in request.session:
        return redirect('/')
    current_user = Users.objects.get(id=request.session["login"])
    if 'group' not in request.session and current_user.user_groups_joined.all().count()<1:
        return redirect('/sos/join')
    group_buy = BuyGroup.objects.get(id=group_id)
    if current_user != group_buy.admin and current_user not in group_buy.tas.all():
        return redirect('/sos')
    user = Users.objects.get(id=user_id)
    if "login" not in request.session:
        redirect("/")
    # if current_user == group_buy[0].admin:
    if user in group_buy.tas.all():
        group_buy.tas.remove(Users.objects.get(id=user_id))
    group_buy.users.remove(Users.objects.get(id=user_id))
    #group_buy[0].tas.del(Users.objects.get(id=user_id))
    return redirect('/sos/admin/users')

def inventory(request):
    if 'login' not in request.session:
        return redirect('/')
    current_user = Users.objects.get(id=request.session["login"])
    if 'group' not in request.session and current_user.user_groups_joined.all().count()<1:
        return redirect('/sos/join')
    user = Users.objects.get(id=request.session['login'])
    group = BuyGroup.objects.get(id=request.session['group'])
    if user != group.admin and user not in group.tas.all():
        return redirect('/sos')
    context = {
        'snacks': group.items.all(),
        'inventory': group.inventory.all(),
        'user': Users.objects.get(id=request.session['login'])
    }
    return render(request, 'sos/inventory.html', context)

def inventory_add(request):
    if 'login' not in request.session:
        return redirect('/')
    current_user = Users.objects.get(id=request.session["login"])
    if 'group' not in request.session and current_user.user_groups_joined.all().count()<1:
        return redirect('/sos/join')
    user = Users.objects.get(id=request.session['login'])
    group = BuyGroup.objects.get(id=request.session['group'])
    if user is not group.admin and user not in group.tas.all():
        return redirect('/sos')
    errors = Inventory.objects.validate(request.POST)
    if len(errors):
        for error in errors:
            messages.error(request, error)
        return redirect('/sos/inventory')
    item = Items.objects.get(buy_group=group,item_name=request.POST['item'])
    maximum = int(request.POST['max'])
    minimum = int(request.POST['min'])
    count = int(request.POST['count'])
    unit = request.POST['measurment']
    Inventory.objects.create(item=item,buy_group=group,count=count,unit=unit,max_inventory=maximum,min_inventory=minimum)
    return redirect('/sos/inventory')

def vote(request, id):
    if 'login' not in request.session:
        return redirect('/')
    current_user = Users.objects.get(id=request.session["login"])
    if 'group' not in request.session and current_user.user_groups_joined.all().count()<1:
        return redirect('/sos/join')
    user = Users.objects.get(id=request.session['login'])
    group = BuyGroup.objects.get(id=request.session['group'])
    item = Items.objects.get(id=id)
    item.voters.add(user)
    print 'in votes'
    return redirect('/sos/inventory')

def devote(request, id):
    if 'login' not in request.session:
        return redirect('/')
    current_user = Users.objects.get(id=request.session["login"])
    if 'group' not in request.session and current_user.user_groups_joined.all().count()<1:
        return redirect('/sos/join')
    user = Users.objects.get(id=request.session['login'])
    group = BuyGroup.objects.get(id=request.session['group'])
    item = Items.objects.get(id=id)
    item.voters.remove(user)
    print user
    print item
    return redirect('/sos/inventory')


def inventory_edit(request):
    if 'login' not in request.session:
        return redirect('/')
    current_user = Users.objects.get(id=request.session["login"])
    if 'group' not in request.session and current_user.user_groups_joined.all().count()<1:
        return redirect('/sos/join')
    user = Users.objects.get(id=request.session['login'])
    group = BuyGroup.objects.get(id=request.session['group'])
    if user != group.admin and user not in group.tas.all():
        return redirect('/sos')
    errors = Inventory.objects.validate(request.POST)
    if len(errors):
        for error in errors:
            messages.error(request, error)
        return redirect('/sos/inventory')
    item = group.items.get(item_name=request.POST['item'])
    inventory = group.inventory.get(item=item)
    inventory.count = int(request.POST['count'])
    inventory.unit = request.POST['measurment']
    inventory.max_inventory = int(request.POST['max'])
    inventory.min_inventory = int(request.POST['min'])
    inventory.save()
    return redirect('/sos/inventory')

def inventory_delete(request, id):
    if 'login' not in request.session:
        return redirect('/')
    current_user = Users.objects.get(id=request.session["login"])
    if 'group' not in request.session and current_user.user_groups_joined.all().count()<1:
        return redirect('/sos/join')
    user = Users.objects.get(id=request.session['login'])
    group = BuyGroup.objects.get(id=request.session['group'])
    if user != group.admin and user not in group.tas.all():
        return redirect('/sos')
    inventory = Inventory.objects.get(id=id)
    inventory.delete()
    return redirect('/sos/inventory')

    
def upload_pic(request):
    if 'login' not in request.session:
        return redirect('/')
    current_user = Users.objects.get(id=request.session["login"])
    if 'group' not in request.session and current_user.user_groups_joined.all().count()<1:
        return redirect('/sos/join')
    print "uploading pic"
    print request.method
    if request.method == 'POST':
        print "is POST"
        form = ImageUploadForm(request.POST, request.FILES)
        print form
        if form.is_valid():
            print "Form Valid!"
            print request.POST["name"]
            name = request.POST["name"]
            group = BuyGroup.objects.get(id=request.session['group'])
            m = Items.objects.create(item_name=name, buy_group=group)
            m.picture = form.cleaned_data['image']
            m.save()
            return redirect('/sos')
    return HttpResponseForbidden('allowed only via POST')

def new_item(request):
    return render(request, "sos/new_item.html")

def switch(request):
    user = Users.objects.get(id=request.session['login'])
    group = BuyGroup.objects.get(id=request.session['group'])
    newGroup = BuyGroup.objects.get(name=request.POST['name'])
    if user in newGroup.users.all():
        request.session['group'] = newGroup.id
    return redirect('/sos')


def item_delete(request, id):
    if 'login' not in request.session:
        return redirect('/')
    if 'group' not in request.session and current_user.user_groups_joined.all().count()<1:
        return redirect('/sos/join')
    user = Users.objects.get(id=request.session['login'])
    group = BuyGroup.objects.get(id=request.session['group'])
    if user != group.admin and user not in group.tas.all():
        return redirect('/sos')
    item = Items.objects.get(id=id)
    item.delete()
    return redirect('/sos')
