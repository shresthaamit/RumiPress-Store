from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    
    class Meta:
        verbose_name_plural = 'Categories'
    def __str__(self):
        return self.name
    
    
class Book(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200)
    publication_date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books')
    distribution_expenses = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    isbn = models.CharField(max_length=13, unique=True, blank=True, null=True)
    
    class Meta:
        verbose_name_plural = 'Books'
    def __str__(self):
        return self.title
    
class Rating(models.Model):
    rate = models.PositiveIntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    review = models.CharField(max_length=100, blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='ratings')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        verbose_name_plural = 'Ratings'
    def __str__(self):
        return str(self.rate)+" for "+self.book.title