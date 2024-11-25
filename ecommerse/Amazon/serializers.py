from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Product, Wishlist,Rating,Cart


class ProductDetailSerializer(serializers.ModelSerializer):
    offer_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'
        
        
    def get_offer_price(self, obj):
        discount_amount = (obj.price * obj.discount) / 100
        offer_price = obj.price - discount_amount
        return round(offer_price, 2) 
  
    
  
class ProductSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(read_only=True)  # Read-only to ensure it's not modified through the API
    offer_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'offer_price', 'discount','likes_count']
        
        
    def get_offer_price(self, obj):
        discount_amount = (obj.price * obj.discount) / 100
        offer_price = obj.price - discount_amount
        return round(offer_price, 2) 
  
 
class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'user', 'product', 'rating', 'review', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value   


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


class CartSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name') 
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2) 
    product_image = serializers.ImageField(source='product.image')  
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)  

    class Meta:
        model = Cart
        fields = ['product_name', 'product_price', 'size', 'quantity', 'product_image', 'total_price']    