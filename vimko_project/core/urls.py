
from rest_framework.routers import DefaultRouter


from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductListCreateView.as_view()),
    path('products/<int:pk>/', views.ProductRetrieveUpdateDeleteView.as_view()),

    path('dealers/', views.DealerListCreateView.as_view()),
    path('dealers/<int:pk>/', views.DealerRetrieveUpdateView.as_view()),

    path('inventory/', views.InventoryListView.as_view()),
    path('inventory/<int:product_id>/', views.InventoryUpdateView.as_view()),
    path('inventory/add/', views.InventoryCreateView.as_view()),   # POST create
    path('orders/', views.OrderListCreateView.as_view()),
    path('orders/<int:pk>/', views.OrderRetrieveUpdateView.as_view()),
    path('orders/<int:pk>/confirm/', views.OrderConfirmView.as_view()),
    path('orders/<int:pk>/deliver/', views.OrderDeliverView.as_view()),
]