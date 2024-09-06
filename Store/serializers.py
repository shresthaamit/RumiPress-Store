from .models import Category,Book,Rating
from rest_framework import serializers
class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        exclude = ('book',)
        
        
class BookSerializer(serializers.ModelSerializer):
    ratings  = RatingSerializer(many=True,read_only=True)
    class Meta:
        model = Book
        fields = "__all__"
class CategorySerializer(serializers.ModelSerializer):
    books =  BookSerializer(many=True, read_only =True)
    class Meta:
        model = Category
        fields ="__all__"
        extra_kwargs = {
            'url': {'view_name': 'platform-detail', 'lookup_field': 'pk'}
        }
    # id = serializers.IntegerField(read_only=True)
    # name = serializers.CharField(max_length=200)
    
    
    # def create(self,validate_data):
    #     return Category.objects.create(**validate_data)
    # def update(self, instance, validate_data):
    #     instance.name = validate_data.get('name', instance.name)
    #     instance.save()
    #     return instance
    

    # # category = CategorySerializer()
    # id = serializers.IntegerField(read_only=True)
    # title = serializers.CharField(max_length=200)
    # subtitle = serializers.CharField(max_length=200)
    # author = serializers.CharField(max_length=200)
    # publication_date=serializers.DateField()
    # publisher = serializers.CharField(max_length=200)
    # category = serializers.CharField(source='category.name')
    # distribution_expenses =serializers.DecimalField(max_digits=10, decimal_places=2)
    # isbn = serializers.CharField(max_length=13)
    # def create(self, validated_data):
    #         category = validated_data.pop('category')['name']
    #         cat = Category.objects.filter(name=category).first()
    #         return Book.objects.create(**validated_data,category=cat)
        
    # def update(self,instance,validated_data):
    #     instance.title = validated_data.get('title',instance.title)
    #     instance.subtitle = validated_data.get('subtitle',instance.subtitle)
    #     instance.author = validated_data.get('author', instance.author)
    #     instance.publication_date = validated_data.get('publication_date', instance.publication_date)
    #     instance.publisher = validated_data.get('publisher', instance.publisher)
    #     instance.category =  validated_data.get(Category,instance.category)
    #     instance.distribution_expenses = validated_data.get('distribution_expenses', instance.distribution_expenses)
    #     instance.isbn = validated_data.get('distribution_expenses', instance.distribution_expenses)
    #     instance.save()
    #     return instance
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     # Customize the representation to only include the category name
    #     representation['category'] = instance.category.name
    #     return representation
    
    
        
    