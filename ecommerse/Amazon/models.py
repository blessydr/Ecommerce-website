from django.db import models
from django.contrib.auth.models import User  



class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Mens Wear', 'Men\'s Wear'),
        ('Womens Wear', 'Women\'s Wear'),
        ('Kids Wear', 'Kids\' Wear'),
        ('Accessories', 'Accessories'),
        ('Footwear', 'Footwear'),
        ('Sportswear', 'Sportswear'),
        ('Home Decor', 'Home Decor'),
        ('Electronics', 'Electronics'),
    ]
    name = models.CharField(max_length=100)  
    description = models.TextField()  
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)  
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    image = models.ImageField(upload_to='products/') 
    sizes = models.CharField(max_length=50)  
    colors = models.CharField(max_length=50)  
    availability = models.BooleanField(default=True)  
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)  
    review = models.TextField(blank=True, null=True) 
    discount = models.CharField(max_length=20, blank=True, null=True) 
    date_added = models.DateTimeField(auto_now_add=True) 
    date_updated = models.DateTimeField(auto_now=True)  
    brand = models.CharField(max_length=50, blank=True, null=True)  
    review_count = models.IntegerField(default=0)  # Count of reviews
    ratings_count = models.IntegerField(default=0)  # Count of ratings
    rating = models.FloatField(default=0.0)
    likes_count = models.IntegerField(default=0)

    def update_rating_info(self):
        reviews = self.reviews.all()  
        if reviews.exists():
            total_reviews = reviews.count() 
            total_rating = sum(review.rating for review in reviews) 
            self.rating = total_rating / total_reviews  
            self.ratings_count = total_reviews  
            self.review_count = total_reviews  
        else:
            self.rating = 0.0
            self.ratings_count = 0
            self.review_count = 0
        self.save()
    def __str__(self):
        return self.name  


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlists') 
    created_at = models.DateTimeField(auto_now_add=True) 

    class Meta:
        unique_together = ('user', 'product')  



class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()  
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.name}"

    def save(self, *args, **kwargs):
        if self.rating < 1 or self.rating > 5:
            raise ValueError("Rating must be between 1 and 5.")
        super().save(*args, **kwargs)