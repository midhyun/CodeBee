from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:study_pk>/', views.detail, name='detail'),
    path('<int:study_pk>/userlist', views.userlist, name='userlist'),
    path('<int:study_pk>/update/', views.update, name='update'),
    path('<int:study_pk>/delete/', views.delete, name='delete'),
    path('<int:study_pk>/join/<int:user_pk>', views.join, name='join'),
    path('study_accepted/<int:study_id>/<int:users_id>', views.study_accepted, name='study_accepted'),
    path('study_kick/<int:study_id>/<int:users_id>', views.study_kick, name='study_kick'),
]