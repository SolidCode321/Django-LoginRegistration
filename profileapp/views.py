from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth import get_user_model

from .forms import CreateUserForm, ProfileForm

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user

from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

User = get_user_model()

@login_required(login_url='login')
def index(request):
    return render(request, 'profileapp/home.html')

@login_required(login_url='login')
def profile(request):
    if request.method =='POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            username = request.user.username
            messages.success(request, f'{username}, Your profile is updated')
            return redirect('/')
    else:
        form = ProfileForm(instance=request.user.profile)
    context = {'form': form}
    return render(request, 'profileapp/profile.html', context)


def login_user(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is  not None:
            login(request, user)
            messages.info(request, f'{username}, you are logged in.')
            return redirect('/')
        else:
            messages.info(request, 'Invalid username or password.')
            return redirect('login')
    return render(request, 'profileapp/login_page.html')


def register_user(request):
    form = CreateUserForm()


    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.info(request, 'Account is created.')
            return redirect('login')
        else:
            context={'form': form}
            messages.info(request, 'Invalid credentials.')
            return render(request, 'profileapp/register_page.html', context)


    context = {'form': form}
    return render(request, 'profileapp/register_page.html', context)

@login_required(login_url='login')
def logout_user(request):
    logout(request)
    messages.info(request, 'You logged out successfully')
    return redirect('login')

def graph(request):
    return render(request, 'profileapp/graph.html')

class GraphData(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        qs_users = User.objects.all().count()
        labels=['Customers', 'Sales', 'Users']
        default = [19, 12, qs_users]
        data = {
            "labels":labels,
            "default":default,
        }
        return Response(data)

class PasswordContextMixin:
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {"title": self.title, "subtitle": None, **(self.extra_context or {})}
        )
        return context

