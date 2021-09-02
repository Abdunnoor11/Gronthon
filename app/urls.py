from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),

    path('mybooks/', views.mybooks, name='mybooks'),
    path('profile/', views.profile, name='profile'),

    path('edit/<int:id>/<int:page>', views.edit, name='edit'),

]
