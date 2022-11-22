from django.urls import path
from articles import views

urlpatterns = [

    path('', views.ArticlesView, name ='articles_view' ),
]

