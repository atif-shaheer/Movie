from django.conf.urls import url
from application.movie.views import UserRegistrationView
from application.movie.views import UserProfileView
from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    url('signup/', UserRegistrationView.as_view()),
    url('profile/', UserProfileView.as_view()),

    path("", views.movies, name="movies"),

    url('add/', views.add_to_cart, name='add_to_cart'),
    url('remove/', views.remove_from_cart, name='remove_from_cart'),
    url('cart/', views.cart, name='cart'),
    ]
