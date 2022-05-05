from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('post', views.post, name='post'),
    path('delete/<str:file_name>', views.delete, name='delete'),
    path('<str:file>/<str:table>', views.excel, name='excel')
]
