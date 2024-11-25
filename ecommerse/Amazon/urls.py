from django.urls import path
from .views import RegisterUserView,LoginView,LogoutView,ProductListView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('products/', ProductListView.as_view(), name='product-list'),
        path('wishlist/', WishlistView.as_view(), name='wishlist'),

]
