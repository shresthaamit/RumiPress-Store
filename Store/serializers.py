from .models import Category,Book,Rating,Favourite
from rest_framework import serializers
class RatingSerializer(serializers.ModelSerializer):
    rate_user = serializers.StringRelatedField()
    class Meta:
        model = Rating
        exclude = ('book',)
        
        
class BookSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')
    qr_code_url = serializers.SerializerMethodField()
    ratings  = RatingSerializer(many=True,read_only=True)
    class Meta:
        model = Book
        fields = "__all__"
        
    def get_qr_code_url(self, obj):
        if obj.qr_code:
            return obj.qr_code.url
        return None 
class CategorySerializer(serializers.ModelSerializer):
    books =  BookSerializer(many=True, read_only =True)
    class Meta:
        model = Category
        fields ="__all__"
        extra_kwargs = {
            'url': {'view_name': 'platform-detail', 'lookup_field': 'pk'}
        }
        
        
class BookDetailForFavouriteSerializer(serializers.ModelSerializer):
    qr_code_url = serializers.SerializerMethodField()

    class Meta:
        model = Book
     
        fields = ['id', 'title', 'subtitle', 'author', 'publisher', 'publication_date', 'category', 'isbn', 'qr_code_url']

    def get_qr_code_url(self, obj):
        if obj.qr_code:
            return obj.qr_code.url
        return None
class FavouriteSerializer(serializers.ModelSerializer):
    book = BookDetailForFavouriteSerializer(read_only=True)
    class Meta:
        model = Favourite
        fields =['id', 'user', 'book']
        
    def create(self, validated_data):
        user =  validated_data.get('user')
        book = validated_data.get('book')
        favourite, created = Favourite.objects.get_or_create(user=user, book=book)
        if not created:
            raise serializers.ValidationError("The book has already been created in  favourites.")
        
        return favourite
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
    
    
        
    