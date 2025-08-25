from django.core.management.base import BaseCommand
from movie.models import Movie
import os
import json

# Se cambio la función con ayuda de Gemini ya que la anterior no funcionaba correctamente
class Command(BaseCommand):
    help = 'Load movies from movie_descriptions.json into the Movie model'

    def handle(self, *args, **kwargs):
        # Using forward slashes for cross-platform compatibility
        # Note: The path here should be relative to your project's manage.py
        json_file_path = 'movie/management/commands/movies.json'

        try:
            # Load data from the JSON file
            with open(json_file_path, 'r', encoding='utf-8') as file:
                movies = json.load(file)

            # Add products to the database
            for movie in movies:  # Iterate directly over the movie list
                # Use .get() with a default value to prevent KeyError and IntegrityError
                title = movie.get('title')
                genre = movie.get('genre')
                year = movie.get('year')
                description = movie.get('plot', '')  # Use '' as default for empty plot/description
                
                # Check for required fields before creating the object
                if title and description:
                    # Check if the movie already exists
                    if not Movie.objects.filter(title=title).exists():
                        Movie.objects.create(
                            title=title,
                            image='movie/images/default.jpg',
                            genre=genre,
                            year=year,
                            description=description
                        )
                    else:
                        self.stdout.write(self.style.WARNING(f'Movie "{title}" already exists, skipping.'))
                else:
                    self.stdout.write(self.style.ERROR(f'Skipping a movie due to missing title or description: {movie}'))
            
            self.stdout.write(self.style.SUCCESS('Successfully loaded movies into the database.'))
            
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Error: JSON file not found at {json_file_path}'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR(f'Error: Failed to decode JSON from {json_file_path}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An unexpected error occurred: {e}'))