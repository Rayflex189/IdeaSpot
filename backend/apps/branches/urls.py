from django.urls import path
from . import views

urlpatterns = [
    path('<int:prd_id>/', views.BranchRetrieveUpdateView.as_view(), name='branch-detail'),
    path('<int:prd_id>/merge/', views.MergeBranchView.as_view(), name='branch-merge'),
    path('<int:prd_id>/discard/', views.DiscardBranchView.as_view(), name='branch-discard'),
]
