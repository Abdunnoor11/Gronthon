from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    
    path('mybooks/', views.mybooks, name='mybooks'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('profile/', views.profile, name='profile'),
    path('publish/<int:id>', views.publish, name='publish'),
    path('allebook/', views.allebook, name='allebook'),    

    path('edit/<int:id>/<int:page>', views.edit, name='edit'),
    path('download/', views.download, name='download'),
    
    path('epudownload/<int:id>', views.epudownload, name='epudownload'),
    
    

]

