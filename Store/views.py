from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CategorySerializer,BookSerializer,RatingSerializer
from .models import Category,Book,Rating
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.validators import ValidationError
# Create your views here.


class BookCategoryVV(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# class BookCategoryView(APIView):
#     def get(self,request):
#         category=Category.objects.all()
#         category_serializer= CategorySerializer(category,many=True,context={'request': request})
#         return Response(category_serializer.data)
    
#     def post(self,request):
#         category = CategorySerializer(data=request.data)
#         if category.is_valid():
#             category.save()
#             return Response(category.data)
#         else:
#             return Response(category.errors)
        
        
        
# class BookCategoryDetailView(APIView):
#     def get(self,request,pk):
#         try:
#             category_detail = Category.objects.get(pk=pk)
#         except Category.DoesNotExist:
#             return Response({"message":"Category doesnot found"}, status=status.HTTP_404_NOT_FOUND)
#         category_serializer = CategorySerializer(category_detail,context={'request': request})
#         return Response(category_serializer.data)
    
#     def put(self,request,pk):
#         category = Category.objects.get(pk=pk)
#         category_serializer = CategorySerializer(category,data = request.data)
#         if category_serializer.is_valid():
#             category_serializer.save()
#             return Response(category_serializer.data)
#         else:
#             category_serializer.errors()
            
#     def delete(self,request,pk):
#         category = Category.objects.get(pk=pk)
#         category.delete()
#         return Response({"message":"Category Deleted"})
    
class BookView(APIView):
    def get(self,request):
        book = Book.objects.all()
        book_serializer = BookSerializer(book, many=True)
        return Response(book_serializer.data)
    def post(self,request):
        book_detail_serializer  =  BookSerializer(data = request.data)
        if book_detail_serializer.is_valid():
            book_detail_serializer.save()
            return Response(book_detail_serializer.data)
        else:
            return Response(book_detail_serializer.errors)
        
        
class BookDetailView(APIView):
    def get(self, request, pk):
        try:
            book_detail = Book.objects.get(pk=pk)
            
        except Book.DoesNotExist:
            return Response({"message":"Book Detail doesnot exist."}, status=status.HTTP_404_NOT_FOUND)
        book_detail_serializer = BookSerializer(book_detail)
        return Response(book_detail_serializer.data)
    
    
    def put(self, request,pk):
        book_detail = Book.objects.get(pk=pk)
        book_detail_serializer = BookSerializer(book_detail, data=request.data)
        if book_detail_serializer.is_valid():
            book_detail_serializer.save()
            return Response(book_detail_serializer.data)
        else:
            return Response(book_detail_serializer.errors)
        
    def delete(self, request, pk):
        book_detail = Book.objects.get(pk=pk)
        book_detail.delete()
        return Response({"message":"Book Deleted"})
    
class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

class ReviewListView(generics.ListAPIView):
    serializer_class = RatingSerializer
    
    def get_queryset(self):
        pk=self.kwargs['pk']
        return Rating.objects.filter(book=pk)
    
class ReviewCreateView(generics.CreateAPIView):
    # def get_queryset(self):
    #     return Rating.objects.all()
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    
    def perform_create(self, serializer):
        pk=self.kwargs['pk']
        book = Book.objects.get(pk=pk)
        user = self.request.user
        rating_queryset = Rating.objects.filter(book=book, rate_user=user)
        if rating_queryset.exists():
            raise ValidationError(f'Rating already done for {book.title}')
        serializer.save(book=book,rate_user=user)
# @api_view(["GET","POST"])
# def category(request):
#     if request.method == 'GET':
#         category = Category.objects.all()
#         category_serializer = CategorySerializer(category, many=True)
#         return Response(category_serializer.data)
#     if request.method == 'POST':
#         category_data  =  CategorySerializer(data= request.data)
#         if category_data.is_valid():
#             category_data.save()
#             return Response(category_data.data,status=status.HTTP_201_CREATED)
#         else:
#             return Response(category_data.errors,status = status.HTTP_400_BAD_REQUEST)
        
# @api_view(['GET','PUT','DELETE'])
# def category_detail(request,pk):
#     if request.method == "GET":
#         try:
#             category_detail = Category.objects.get(pk=pk)
#         except Category.DoesNotExist:
#             return Response({'error':"Category Not Found"}, status=404)
#         category_serializer = CategorySerializer(category_detail)
#         return Response(category_serializer.data, status=status.HTTP_200_OK)
#     if request.method  == 'PUT':
#         category_detail = Category.objects.get(pk=pk)
#         category_serializer = CategorySerializer(category_detail, data=request.data)
#         if category_serializer.is_valid():
#             category_serializer.save()
#             return Response(category_serializer.data, status=status.HTTP_200_OK)
        
#         else:
#             return Response(category_serializer.error)
#     if request.method == "DELETE":
#         category_detail = Category.objects.get(pk=pk)
#         category_detail.delete()
#         return Response({'message':'Category Deleted'})
    
# @api_view(['GET', 'POST'])
# def books(request):
#     if request.method == "GET":
#         books = Book.objects.all()
#         book_serializer = Book_Serializer(books, many=True)
#         return Response(book_serializer.data)
    
    
#     if request.method ==  "POST":
#         book_serializer = Book_Serializer(data= request.data)
#         if book_serializer.is_valid():
#             book_serializer.save()
#             return Response(book_serializer.data)
#         else:
#             return Response(book_serializer.errors)
    
# @api_view(['GET',"PUT"]) 
# def book_detail(request,pk):
#     if request.method =="GET":
#         try:
#             book_detail = Book.objects.get(pk=pk)
#         except Book.DoesNotExist:
#             return Response({'error':"Book Not Found"}, status=404)
#         book_detail_serializer = Book_Serializer(book_detail)
#         return Response(book_detail_serializer.data)
#     if request.method == "PUT":
#         book_detail = Book.objects.get(pk=pk)
#         book_detail_serializer = Book_Serializer(book_detail, data=request.data)
#         if book_detail_serializer.is_valid():
#             book_detail_serializer.save()
#             return Response(book_detail_serializer.data)
        
#         else:
#             return Response(book_detail_serializer.errors)
        
#     if request.method == 'DELETE':
#         book_detail  = Book.objects.get(pk=pk)
#         book_detail.delete()
#         return Response({"success":"Book deleted successfully"})