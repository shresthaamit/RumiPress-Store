
from django.urls import path, include
from . import views
from .views import *
from rest_framework import routers
router = routers.DefaultRouter()
router.register('category', BookCategoryVV, basename='category')
urlpatterns = [
    # path('', views.category, name="category"),
    # path('<int:pk>/', views.category_detail, name='category_detail'),
    # path('', BookCategoryView.as_view(),name="BookCategory"),
    # path('<int:pk>/', BookCategoryDetailView.as_view(), name="category-detail"),
    path('books/',BookView.as_view(), name='books'),
    path('books/<int:pk>/', BookDetailView.as_view(), name="book-detail"),
    path('books/<int:pk>/review-create/', ReviewCreateView.as_view(), name="review-create"),
    path('books/<int:pk>/review/', ReviewListView.as_view(), name="book-detail"),
    path('books/review/<int:pk>/', ReviewDetailView.as_view(),name="review-detail"),
    path('', include(router.urls))
    
]
