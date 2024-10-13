import json

FILENAME = 'data.json'


def get_movies():
    with open(FILENAME, 'r') as file:
        movies = json.load(file)
    return movies


def save_movies(movies):
    with open(FILENAME, 'w') as file:
        json.dump(movies, file, indent=4)


def add_movie(title, year, rating):
    movies = get_movies()
    movies[title] = {"year": year, "rating": rating}
    save_movies(movies)


def delete_movie(title):
    movies = get_movies()
    if title in movies:
        del movies[title]
    save_movies(movies)


def update_movie(title, rating):
    movies = get_movies()
    if title in movies:
        movies[title]["rating"] = rating
    save_movies(movies)
