from django.urls import path
from .views import ProductListView, ProductDetailView

urlpatterns = [

    path('', ProductListView.as_view()),
    path('<int:pk>/<slug:slug>/', ProductDetailView.as_view()),

]