from django.urls import path
from .views import (
    loginview, login_action, logout_action, supplierlistview, addsupplier, searchsuppliers, productlistview,
    addproduct, confirmdeleteproduct, deleteproduct, edit_product_get, edit_product_post, products_filtered,
    # Added new views
    customerlistview, addcustomer, confirmdeletecustomer, deletecustomer, orderlistview, addorder,
    confirmdeleteorder, deleteorder
)

urlpatterns = [
    # Login & logout
    path('', loginview),
    path('login/', login_action),
    path('logout/', logout_action),

    # Supplier urls
    path('suppliers/', supplierlistview),
    path('add-supplier/', addsupplier),
    path('search-suppliers/', searchsuppliers),

    # Product urls
    path('products/', productlistview),
    path('add-product/', addproduct),
    path('delete-product/<int:id>/', deleteproduct),
    path('confirm-delete-product/<int:id>/', confirmdeleteproduct),
    path('edit-product-get/<int:id>/', edit_product_get),
    path('edit-product-post/<int:id>/', edit_product_post),
    path('products-by-supplier/<int:id>/', products_filtered),

    # ADDED URLS ====================

    # Customer urls
    path('customers/', customerlistview),
    path('add-customer/', addcustomer),
    path('confirm-delete-customer/<int:id>/', confirmdeletecustomer),
    path('delete-customer/<int:id>/', deletecustomer),

    # Order urls
    path('orders/', orderlistview),
    path('add-order/', addorder),
    path('confirm-delete-order/<int:id>/', confirmdeleteorder),
    path('delete-order/<int:id>/', deleteorder),
]