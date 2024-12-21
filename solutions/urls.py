from django.urls import path
from . import views

app_name = 'solutions'

urlpatterns = [
    path('', views.solution_list, name='solution-list'),
    path('tags/', views.tag_list, name='tag-list'),
    path('solution/create/', views.solution_create, name='create'),
    path('<str:username>/<slug:slug>/', views.solution_detail, name='detail'),
]
