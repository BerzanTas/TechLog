from django.urls import path
from . import views

urlpatterns = [
    path('comments/', views.CommentListCreate.as_view(), name='comment-view-create'),
    path('comments/<int:pk>/', views.CommentDestroy.as_view(), name='comment-destroy'),
    path('solutions/', views.SolutionListCreate.as_view(), name='solution-view-create'),
    path("search/", views.SolutionListCreate.as_view(), name="solution-search"),
    path('solutions/<str:username>', views.UserSolutionsList.as_view(), name='user-solution-list'),
    path('solutions/<int:pk>/', views.SolutionRetrieveUpdateDestroy.as_view(), name='solution-update'),
]
