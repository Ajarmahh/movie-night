from movie_app import MovieApp
from storage_json import StorageJson
from storage_csv import StorageCsv

API_KEY = '3c8176cb'


def main():
    storage_type = input("Select storage type (1 = JSON, 2 = CSV): ").strip()

    if storage_type == '1':
        storage = StorageJson('data/movies.json')
    elif storage_type == '2':
        storage = StorageCsv('data/movies.csv')
    else:
        print("Invalid storage type selected.")
        return

    app = MovieApp(storage, API_KEY)
    app.run()


if __name__ == "__main__":
    main()
