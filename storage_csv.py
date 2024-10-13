import csv
from istorage import IStorage


class StorageCsv(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path

    def _load_data(self):
        movies = {}
        try:
            with open(self.file_path, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    title = row['title']
                    movies[title] = {
                        'rating': float(row['rating']),
                        'year': int(row['year']),
                        'poster': row.get('poster', '')
                    }
        except FileNotFoundError:
            pass  # File not found means we start with an empty dictionary
        return movies

    def _save_data(self, movies):
        with open(self.file_path, mode='w', newline='') as file:
            fieldnames = ['title', 'rating', 'year', 'poster']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for title, details in movies.items():
                writer.writerow({
                    'title': title,
                    'rating': details['rating'],
                    'year': details['year'],
                    'poster': details.get('poster', '')
                })
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
        movie_to_delete = None
        for movie_title in movies:
            if movie_title.lower() == title_lower:
                movie_to_delete = movie_title
                break

        if movie_to_delete:
            del movies[movie_to_delete]  # Delete movie using the correct title
            self._save_data(movies)
        else:
            print(f"Movie '{title}' not found in the movie list.")

    def update_movie(self, title, rating):
        movies = self._load_data()
        if title in movies:
            movies[title]['rating'] = rating
            self._save_data(movies)
