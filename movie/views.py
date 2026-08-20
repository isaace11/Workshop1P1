import base64
import io
from collections import Counter

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from django.shortcuts import render

from .models import Movie
# Create your views here.


def home(request):
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()

    return render(request, 'home.html', {
        'name': 'Isabel Acevedo',
        'searchTerm': searchTerm,
        'movies': movies
    })


def about(request):
    return render(request, 'about.html', {'name': 'Isabel Acevedo'})


def _build_bar_graph(labels, values, title, xlabel, ylabel):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(labels, values)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(axis='x', labelrotation=90)
    fig.tight_layout()

    buffer = io.BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    graphic = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close(fig)

    return graphic


def statistics_view(request):
    years_counter = Counter()
    genres_counter = Counter()

    for movie in Movie.objects.all():
        year = movie.year if movie.year is not None else 'None'
        years_counter[str(year)] += 1

        genre = movie.genre or ''
        first_genre = genre.split(',')[0].strip() if genre.strip() else 'None'
        genres_counter[first_genre] += 1

    years = sorted(years_counter.keys(), key=lambda value: (value == 'None', value))
    genres = sorted(genres_counter.keys())

    graphic_year = _build_bar_graph(
        years,
        [years_counter[year] for year in years],
        'Movies per year',
        'Year',
        'Number of movies',
    )
    graphic_genre = _build_bar_graph(
        genres,
        [genres_counter[genre] for genre in genres],
        'Movies per genre',
        'Genre',
        'Number of movies',
    )

    return render(request, 'statistics.html', {
        'graphic_year': graphic_year,
        'graphic_genre': graphic_genre,
    })
