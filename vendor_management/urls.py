from django.urls import path
from . import views  # Import views from your pathfinding app

urlpatterns = [
    path('vendors/', views.VendorListCreateAPIView.as_view(), name='vendor-list-create'),
    path('vendors/<int:pk>/', views.VendorDetailAPIView.as_view(), name='vendor-detail'),
    path('vendors/<int:pk>/performance/', views.VendorPerformanceAPIView.as_view(), name='vendor-performance'),

    path('purchase_orders/', views.PurchaseOrderListCreateAPIView.as_view(), name='purchase-order-list-create'),
    path('purchase_orders/<int:pk>/', views.PurchaseOrderDetailAPIView.as_view(), name='purchase-order-detail'),
    path('purchase_orders/<int:pk>/acknowledge/', views.AcknowledgePurchaseOrderAPIView.as_view(), name='purchase-order-acknowledge'),
]