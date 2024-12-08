from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('reset_password/', views.login_view, name='reset_password'),
    path('gusest_browse/', views.login_view, name='guest_browse'),
    path('logout/', views.logout_view, name="logout"),
    path('<str:username>/', views.user_profile, name='user_profile'),
]
