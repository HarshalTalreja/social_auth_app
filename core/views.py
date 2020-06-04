from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UpdatePhoneNoForm
from django.contrib import messages
from .models import CustomUser
from .check_number import check_no
from django.views.generic import ListView, DetailView
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q

# Create your views here.
def login(request):
    return render(request, 'core/login.html')

@login_required
def home(request):
    if not check_no(str(request.user.phone)):
        print(type(request.user.phone))
        if request.method == 'POST':
            form = UpdatePhoneNoForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, f'Your phone number is updated!')
                return redirect('home')
            else:
                CustomUser.objects.filter(id=request.user.pk).delete()
        else:
            form = UpdatePhoneNoForm()
        return render(request, 'core/phone.html', {'form': form})
    else:
        print("Hello")
        return render(request, 'core/home.html')

class UserListView(ListView):
    model = CustomUser
    context_object_name = 'users'
    template_name= 'core/user_list.html'

class UserDetailView(DetailView):
    model = CustomUser
    context_object_name = 'user'

@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'core/password.html', {'form': form})

def get_user_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        users = CustomUser.objects.filter(
            Q(phone__icontains=q)|
            Q(name__icontains=q)
        ).distinct()

    for user in users:
        queryset.append(user)
    return list(set(queryset))

def SearchScreenView(request):
    context = {}

    query = ""
    if request.GET:
        query = request.GET['q']
        context['query'] = str(query)

    users = CustomUser.objects.all()
    context['users'] = users
    
    users = get_user_queryset(query)
    context['users'] = users



    return render(request, 'core/search_screen.html', context)
