from django.urls import path

from . import views

urlpatterns = [
    path('entries/', views.EntryView.as_view()),
    path('entries/<int:pk>/', views.EntryRetrieveView.as_view()),
    path('likes/', views.LikeView.as_view()),
    path('likes/<int:pk>/', views.LikeRetrieveView.as_view()),
]
