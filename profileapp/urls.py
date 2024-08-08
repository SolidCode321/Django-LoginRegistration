from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='home'),
    path('profile/', views.profile, name='profile'),
    path('accounts/login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('graph/', views.graph, name='graph'),
    path('graph/data/', views.GraphData.as_view()),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='profileapp/password_reset_email.html'),name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='profileapp/password_reset_sent.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='profileapp/password_reset_form.html'),name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='profileapp/password_reset_complete.html'),name='password_reset_complete'),

]