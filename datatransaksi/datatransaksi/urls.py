
from django.contrib import admin
from django.urls import path
from transaksi import views



urlpatterns = [
    path('', views.home, name='home'),
    path('list_item/', views.list_item, name='list_item'),
    path('list_anggota/', views.list_anggota, name='list_anggota'),
    path('add_item/', views.add_item, name='add_item'),
    path('update_item/<int:pk>/', views.update_item, name='update_item'),
    path('delete_item/<str:pk>/', views.delete_item, name='delete_item'),
    path('admin/', admin.site.urls),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('download_pdf/<int:pk>/', views.download_pdf, name='download_pdf'),
    path('register/', views.register, name='register'),

    
]
