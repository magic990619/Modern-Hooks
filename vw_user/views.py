# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth.models import User
from vw_user.models import Profile


@login_required
@csrf_exempt
def index(request):
    request_type = request.POST.get('action')
    if request_type == 'delete':
        del_id = request.POST.get('del_id', None)
        User.objects.get(pk=del_id).delete()
    elif request_type == 'add':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        position = request.POST.get('position')
        new_user = User()
        User.objects.create_user(username=email, email=email, password=password)
    members = User.objects.all()
    return render(request, "vw_user/index.html", {
        'members': members,
    })


@login_required
@csrf_exempt
def edit_member(request):
    type = request.POST.get('type')
    content = request.POST.get('content')
    member_id = request.POST.get('member_id')
    member = Profile.objects.get(pk=member_id)
    member.type = type
    member.content = content
    member.save()
    return HttpResponse('success')


@login_required
@csrf_exempt
def del_member(request):
    del_id = request.POST.get('del_id')
    member = Profile.objects.get(pk=del_id)
    member.delete()
    return HttpResponse('success')
