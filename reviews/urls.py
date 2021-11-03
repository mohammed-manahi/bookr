from django.contrib import admin
from django.urls import path
from reviews import views

urlpatterns = [path('welcome', views.welcome, name='welcome'),
               # url mapper for views.index method
               path('', views.index),
               #path('book-search', views.search),
               path('books/', views.book_list, name='book-list'),
               path('books/<int:pk>', views.book_detail, name='book_detail'),
               path('book-search', views.book_search, name = 'book_search'),
               path('order', views.order_book, name='order_book')
               ]
