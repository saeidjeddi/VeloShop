from django.urls import path

from .views import ProductsCategoryView, CategoryView


urlpatterns = [
    path('', CategoryView.as_view()),
    path("<int:category_id>/", ProductsCategoryView.as_view()),
]