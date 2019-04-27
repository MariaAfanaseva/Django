from django.shortcuts import render, HttpResponseRedirect
from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm
from django.contrib import auth
from django.urls import reverse


def register(request):
    title = 'register'

    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            new_user = register_form.save()
            auth.login(request, new_user)
            return HttpResponseRedirect(reverse('index'))
    else:
        register_form = ShopUserRegisterForm()

    context = {'title': title, 'register_form': register_form}
    return render(request, 'authapp/register.html', context)


def edit(request):
    title = 'editing'

    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)

    context = {'title': title, 'edit_form': edit_form}

    return render(request, 'authapp/edit.html', context)


def login(request):
    title = 'login'
    next = request.GET['next'] if 'next' in request.GET.keys() else ''

    login_from = ShopUserLoginForm(data=request.POST)
    if request.method == 'POST' and login_from.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse('index'))

    context = {
        'title': title,
        'login_form': login_from,
        'next': next
    }
    return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
