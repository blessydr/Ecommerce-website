from rest_framework import serializers
from django.contrib.auth.models import Usefrom rest_framework import serializers
from .models import Product, Wishlist

class ProductSerializer(serializers.ModelSerializer):
    is_in_wishlist = serializers.SerializerMethodField()  # To check if a product is in the user's wishlist

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'price', 'brand', 'image', 'offer', 
            'rating', 'ratings_count', 'review_count', 
            'likes_count', 'is_in_wishlist'
        ]

    # Method to determine if the product is in the user's wishlist
    def get_is_in_wishlist(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return Wishlist.objects.filter(user=user, product=obj).exists()
        return False

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
