from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CategorySerializer,BookSerializer,RatingSerializer,FavouriteSerializer
from .models import Category,Book,Rating,Favourite
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.validators import ValidationError
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly, IsAdminUser
from .permission import IsAdminOrReadOnlyPermission,IsStaffOrReadOnlyPermission,IsStaffOrIsAdminPermission,ReviewUserOrReadOnly
from django.http import HttpResponse
import pandas as pd
from rest_framework.decorators import api_view, permission_classes
import qrcode
from io import BytesIO
from django.core.files import File
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
# Create your views here.


class BookCategoryVV(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnlyPermission]
    


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
@permission_classes([IsAuthenticated])
def generate_qr_code(book):
    qr_data = f"Title: {book.title}, Author: {book.author}, ISBN: {book.isbn}, Category: {book.category.name}"
    qr_img = qrcode.make(qr_data)
    img_io = BytesIO()
    qr_img.save(img_io, 'PNG')
    img_io.seek(0)
    filename = f'{book.title}_qr.png'
    book.qr_code.save(filename, File(img_io), save=False)
    book.save()
class BookView(APIView):
    permission_classes = [IsStaffOrReadOnlyPermission]
    def get(self,request):
        book = Book.objects.all()
        book_serializer = BookSerializer(book, many=True)
        return Response(book_serializer.data)
    
    def post(self,request):
        book_detail_serializer  =  BookSerializer(data = request.data)
        if book_detail_serializer.is_valid():
            book =book_detail_serializer.save()
            generate_qr_code(book) 
            return Response(book_detail_serializer.data)
        else:
            return Response(book_detail_serializer.errors)
        
        
class BookDetailView(APIView):
    permission_classes =[IsStaffOrReadOnlyPermission]
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
            book =book_detail_serializer.save()
            generate_qr_code(book)
            
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
    permission_classes = [IsAuthenticatedOrReadOnly,ReviewUserOrReadOnly]

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
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        pk=self.kwargs['pk']
        book = Book.objects.get(pk=pk)
        user = self.request.user
        rating_queryset = Rating.objects.filter(book=book, rate_user=user)
        if rating_queryset.exists():
            raise ValidationError(f'Rating already done for {book.title}')
        
        if book.total_ratings == 0:
            book.average_rate =serializer.validated_data['rate']
        else:
            book.average_rate = (book.average_rate + serializer.validated_data['rate']) / 2
        book.total_ratings +=1
        book.save()   
        serializer.save(book=book,rate_user=user)
        

def download_excel(request):
    permission= IsStaffOrIsAdminPermission()
    if not permission.has_permission(request, None):
         return HttpResponse("You do not have permission to access this resource.", status=403)
    # if permission_classes. 
    books = Book.objects.all()
    all_books = []
    for book in books:
        all_books.append({
            'Title':book.title,
            'SubTitle':book.subtitle,
            'Author':book.author,
            'Publisher':book.publisher,
            'Publication_date':book.publication_date,
            'Category':book.category,
            'Distribution Expenses':book.distribution_expenses,
            'Isbn':book.isbn
        }  
        )
    # print(all_books)
    df = pd.DataFrame(all_books)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=books.xlsx'
    df.to_excel(response,index=False,engine='openpyxl')
    return response

class count_book(APIView):
    def get(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({"message": "Category does not exist"}, status=404)
        book_count = Book.objects.filter(category_id=category)
        if book_count.exists():
            total = book_count.count()
            return Response({"count": total})
        else:
            return Response({"message": "No books found in this category"}, status=404)
        
        
class BookPDFView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,pk):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response({"message": "Book not found"},status=404)
        response=HttpResponse(content_type="application/pdf")
        response['Content-Disposition'] = f'attachment; filename="{book.title}.pdf"'
        p = canvas.Canvas(response, pagesize=letter)
        p.setFont("Times-Roman", 12)
        p.drawString(100, 750, f"Title: {book.title}")
        p.drawString(100, 730, f"Subtitle: {book.subtitle}")
        p.drawString(100, 710, f"Author: {book.author}")
        p.drawString(100, 690, f"Publisher: {book.publisher}")
        p.drawString(100, 670, f"Publication Date: {book.publication_date.strftime('%Y-%m-%d')}")
        p.drawString(100, 650, f"ISBN: {book.isbn if book.isbn else 'N/A'}")
        p.drawString(100, 630, f"Category: {book.category.name}")
        p.showPage()
        p.save()
        return response
    
    
class AddToFavorite(generics.CreateAPIView):
    serializer_class = FavouriteSerializer
    permission_classes = [IsAuthenticated]
    def  post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        user = request.user
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response({'error':"Book Not Found"}, status=404)
        if Favourite.objects.filter(user=user, book=book).exists():
            return Response({'message': 'This book is already in your favorites!'}, status=400)
        serializers = self.get_serializer(data={'user': user.id, 'book': book.id})
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response({'message': 'Book added to favorites!'}, status=201)
    
    
class ShowFavorite(generics.ListAPIView):
    serializer_class = FavouriteSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Favourite.objects.filter(user=user)
    
    
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