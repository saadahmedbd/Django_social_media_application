from django.urls import path
from . import views


urlpatterns = [
    path('',views.home,name='home'),
    path('room/<str:pk>/',views.room, name='room'),
    path('user-profile/<str:pk>', views.profile, name='user-profile'),


    path('create-room',views.createRoom,name="room-form"),
    path('update-room/<str:pk>/',views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/',views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/',views.deleteMessage, name="delete-message"),

    path('update-user/',views.updateUser, name="update-user"),

    path('topic/',views.topicPage, name='topic'),
    path('activity/',views.activityPage, name='activity'),




    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('register/', views.registerPage , name="register"),
    
    
]

