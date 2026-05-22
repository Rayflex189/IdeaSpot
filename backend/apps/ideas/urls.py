from django.urls import path
from . import views

urlpatterns = [
    path('', views.IdeaListCreateView.as_view(), name='idea-list'),
    path('<int:pk>/', views.IdeaDetailView.as_view(), name='idea-detail'),
]
