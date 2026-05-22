from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('apps.accounts.urls')),
    path('api/ideas/', include('apps.ideas.urls')),
    path('api/prds/', include('apps.prds.urls')),
    path('api/branches/', include('apps.branches.urls')),
]
