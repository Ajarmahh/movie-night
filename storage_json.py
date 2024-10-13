from istorage import IStorage
import json


class StorageJson(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path

    def _load_data(self):
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_data(self, data):
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=4)
            print(f"Movies saved to {self.file_path}.")

    def list_movies(self):
        return self._load_data()

    def add_movie(self, title, year, rating, poster):
        movies = self.list_movies()
        movies[title] = {
            'year': year,
            'rating': rating,
            'poster': poster
        }
        self._save_data(movies)

    def delete_movie(self, title):
        movies = self._load_data()
        title_lower = title.lower()
        # Find movie by matching lowercase title
        movie_to_delete = None
        for movie_title in movies:
            if movie_title.lower() == title_lower:
                movie_to_delete = movie_title
                break

        if movie_to_delete:
            del movies[movie_to_delete]
            self._save_data(movies)
        else:
            print(f"Movie '{title}' not found in the movie list.")

    def update_movie(self, title, rating):
        movies = self._load_data()
        if title in movies:
            movies[title]["rating"] = rating
            self._save_data(movies)
