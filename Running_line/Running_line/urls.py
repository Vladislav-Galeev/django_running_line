from main import views
from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('download/<str:running_line>/', views.download_file, name='download_file'),
    path('get_notes/', views.get_notes, name='get_notes'),
]
