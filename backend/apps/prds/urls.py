from django.urls import path
from . import views

urlpatterns = [
    path('', views.PRDListCreateView.as_view(), name='prd-list'),
    path('<int:pk>/', views.PRDDetailView.as_view(), name='prd-detail'),
    path('generate/<int:idea_id>/', views.GeneratePRDView.as_view(), name='generate-prd'),
    path('<int:prd_id>/grant/', views.GrantPermissionView.as_view(), name='grant-permission'),
    path('<int:prd_id>/revoke/<int:user_id>/', views.RevokePermissionView.as_view(), name='revoke-permission'),
]
