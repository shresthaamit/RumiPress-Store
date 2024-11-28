from django.db.models import Avg,Count
from .models import Book,Rating
import numpy as np
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def calculate_baseline_ratings():
    avg_rating = Book.objects.aggregate(Avg('average_rate'))['average_rate__avg']
    return avg_rating if avg_rating else 3.0 


def calculate_total_ratings_threshold():
    total_ratings = Book.objects.values_list('total_ratings', flat=True) 
    if total_ratings:
        return np.percentile(total_ratings,70)
    return 0


def calculate_average_weighted_mean(book,m,C):
    R= book.average_rate
    v=book.total_ratings
    
    if v + C > 0:
        weighted_mean = (R*v + C*m) /(v +C)
        return weighted_mean
    return 0

def recommend_books(user):
    recommend_books =[]
    m=calculate_baseline_ratings()
    C =  calculate_total_ratings_threshold()
    allbooks = Book.objects.annotate(avg_rating = Avg('ratings__rate'), rating_count=Count('ratings'))
    for book in allbooks:
        if book.total_ratings >= C:
            awm = calculate_average_weighted_mean(book,m,C)
            print(logger.info(f"Book: {book.title}, Total Ratings: {book.total_ratings}, AWM: {awm}"))
            recommend_books.append((book,awm))
         
        if  len(recommend_books)<4:
            remaining_books = [
                (book,calculate_average_weighted_mean(book,m,C))
                for book in allbooks if book not in [b for b, _ in recommend_books]
            ]
            recommend_books.extend(remaining_books[:4 - len(recommend_books)])
            
            
    recommend_books.sort(key=lambda x: x[1], reverse=True)
    return [book for book, _ in recommend_books[:4]]