import requests


class MovieApp:
    def __init__(self, storage, api_key):
        self._storage = storage
        self._api_key = api_key

    def _command_list_movies(self):
        movies = self._storage.list_movies()
        if not movies:
            print("No movies found.")
        else:
            for title, details in movies.items():
                print(
                    f'{title} - Year: {details["year"]}, Rating: {details["rating"]},'
                    f' Poster: {details.get("poster", "N/A")}')

    def _command_add_movie(self):
        title = input("Enter movie title: ").strip()
        if title == "":
            print("Movie title cannot be empty.")
            return
        try:
            response = requests.get(
                f"http://www.omdbapi.com/?t={title}&apikey={self._api_key}"
            )
            data = response.json()

            if data['Response'] == 'False':
                print(f"Movie '{title}' not found in OMDb API.")
                return

            # Extracting the necessary information from the API response
            movie_title = data['Title']
            year = int(data['Year'])
            rating = float(data.get('imdbRating', 0))
            poster = data.get('Poster', 'N/A')

            # Adding the movie to storage
            self._storage.add_movie(movie_title, year, rating, poster)
            print(f"Movie '{movie_title}' added successfully.")

        except requests.exceptions.RequestException:
            print("Error: Unable to connect to OMDb API. Please check your connection.")
        except ValueError:
            print("Error: Received invalid data from the API.")

    def _command_delete_movie(self):
        title = input("Enter movie title to delete: ").strip()
        if title == "":
            print("Movie title cannot be empty.")
            return
        self._storage.delete_movie(title)
        print(f"Movie '{title}' deleted successfully.")

    def _command_update_movie(self):
        title = input("Enter movie title to update: ").strip()
        if title == "":
            print("Movie title cannot be empty.")
            return
        try:
            new_rating = float(input("Enter new rating: "))
            self._storage.update_movie(title, new_rating)
            print(f"Movie '{title}' updated successfully.")
        except ValueError:
            print("Invalid input. Rating should be a float.")

    def _command_movie_stats(self):
        movies = self._storage.list_movies()
        if not movies:
            print("No movies available to show statistics.")
            return

        ratings = [details["rating"] for details in movies.values()]
        average_rating = sum(ratings) / len(ratings)
        best_movie = max(movies.items(), key=lambda item: item[1]["rating"])
        worst_movie = min(movies.items(), key=lambda item: item[1]["rating"])

        print(f"Average rating: {average_rating:.2f}")
        print(f"Best movie: {best_movie[0]} - Rating: {best_movie[1]['rating']}")
        print(f"Worst movie: {worst_movie[0]} - Rating: {worst_movie[1]['rating']}")

    def _generate_website(self):
        with open('_static/index_template.html', 'r') as file:
            template_html = file.read()

        template_html = template_html.replace('__TEMPLATE_TITLE__', 'My Movie App')

        # Generate the movie grid HTML
        movies = self._storage.list_movies()
        movie_grid_html = ''
        for title, details in movies.items():
            movie_html = f'''
             <li>
                 <div class="movie">
                     <h2>{title}</h2>
                     <img src="{details.get('poster', '')}" alt="{title} poster" class="movie-poster" />
                     <p>Year: {details['year']}</p>
                     <p>Rating: {details['rating']}/10</p>
                 </div>
             </li>
             '''
            movie_grid_html += movie_html

        template_html = template_html.replace('__TEMPLATE_MOVIE_GRID__', movie_grid_html)

        with open('index.html', 'w') as file:
            file.write(template_html)

        print("Website was generated successfully.")

    def run(self):
        while True:
            print("\nMenu:")
            print("0. Exit")
            print("1. List movies")
            print("2. Add movie")
            print("3. Delete movie")
            print("4. Update movie")
            print("5. Stats")
            print("6. Generate website")

            choice = input("Enter your choice: ").strip()
            if choice == '0':
                print("Bye!")
                break
            elif choice == '1':
                self._command_list_movies()
            elif choice == '2':
                self._command_add_movie()
            elif choice == '3':
                self._command_delete_movie()
            elif choice == '4':
                self._command_update_movie()
            elif choice == '5':
                self._command_movie_stats()
            elif choice == '6':
                self._generate_website()

            else:
                print("Invalid choice. Please try again.")
