from django.urls import path

from .views import CartProductItemView, CartProductItemRemoveAddView


urlpatterns = [
    path('', CartProductItemView.as_view()),
    path('<int:pk>', CartProductItemRemoveAddView.as_view()),
]