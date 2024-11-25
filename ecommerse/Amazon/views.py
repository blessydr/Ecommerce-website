from django.shortcuts import render
from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login,logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Product
from .models import Product
from .serializers import ProductSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Wishlist
from .serializers import ProductSerializer

class WishlistView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can use wishlist
    serializer_class = ProductSerializer

    def get_queryset(self):
        # Get the wishlist products for the logged-in user
        user = self.request.user
        return Product.objects.filter(wishlists__user=user)

    def post(self, request, *args, **kwargs):
        user = request.user
        product_id = request.data.get('product_id')

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        # Add or remove from wishlist
        wishlist_item, created = Wishlist.objects.get_or_create(user=user, product=product)

        if not created:
            # If already exists, remove from wishlist
            wishlist_item.delete()
            product.likes_count = product.wishlists.count()  # Update likes count
            product.save()
            return Response({"message": "Removed from wishlist"}, status=status.HTTP_200_OK)
        
        # Update likes count if added
        product.likes_count = product.wishlists.count()
        product.save()
    
        return Response({"message": "Added to wishlist"}, status=status.HTTP_201_CREATED)


class LogoutView(APIView):
    def post(self, request):
        logout(request)  # This will end the user's session
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all() 
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'price', 'availability', 'name']

class LoginView(APIView):
    permission_classes = [AllowAny]  

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user) 
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)



class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  
