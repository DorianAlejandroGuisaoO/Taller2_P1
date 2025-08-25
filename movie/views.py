from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie
import matplotlib
matplotlib.use('Agg')   # <- Esto primero
import matplotlib.pyplot as plt
import io, base64
from django.shortcuts import render
from .models import Movie


# Create your views here.

def home(request):
    #return HttpResponse('<h1>Welcome to home page</h1>')
    #return render(request, 'home.html')
    #return render(request, 'home.html', {'name': ' Dorian Alejandro Guisao Ospina'})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm': searchTerm, 'movies': movies})


def about(request):
    #return HttpResponse('<h1>Welcome to about</h1>')
    return render(request, 'about.html')
    
def statistics_view(request):
    all_movies = Movie.objects.all()

    # ========= Gráfica 1: Películas por año =========
    movie_counts_by_year = {}
    for movie in all_movies:
        year = str(movie.year) if movie.year else "None"   # 👈 convertir a str
        movie_counts_by_year[year] = movie_counts_by_year.get(year, 0) + 1

    plt.figure(figsize=(12, 6))
    plt.bar(movie_counts_by_year.keys(), movie_counts_by_year.values(), width=0.5)
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(rotation=90)
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    graphic_year = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    plt.close()

    # ========= Gráfica 2: Películas por género =========
    movie_counts_by_genre = {}
    for movie in all_movies:
        if movie.genre:
            first_genre = movie.genre.split(',')[0].strip()
            movie_counts_by_genre[first_genre] = movie_counts_by_genre.get(first_genre, 0) + 1
        else:
            movie_counts_by_genre["Unknown"] = movie_counts_by_genre.get("Unknown", 0) + 1

    plt.figure(figsize=(10, 6))
    plt.bar(movie_counts_by_genre.keys(), movie_counts_by_genre.values(), width=0.6, color="skyblue")
    plt.title('Movies per genre (first genre only)')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    graphic_genre = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    plt.close()

    # ========= Render =========
    return render(request, 'statistics.html', {
        'graphic_year': graphic_year,
        'graphic_genre': graphic_genre
    })


def signup(request):
    email = request.GET.get('email')  # obtener email del formulario
    return render(request, 'signup.html', {'email': email})