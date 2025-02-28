from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login',views.loginUser,name='login'),
    path('logout',views.logoutUser,name='logout'),
    path('register',views.registerUser,name='register'),
    path('editProfile',views.editUserProfile,name='editProfile'),
    path('room/<str:pk>/',views.room,name='room'),
    path('userProfile/<str:pk>/',views.userProfile,name='userProfile'),
    path('createRoom',views.createRoom,name='createRoom' ),
    path('updateRoom/<str:pk>/',views.updateRoom,name='updateRoom' ),
    path('deleteRoom/<str:pk>/',views.deleteRoom,name='deleteRoom'),
    path('deleteMessage/<str:pk>/',views.deleteMessage,name='deleteMessage'),

]
