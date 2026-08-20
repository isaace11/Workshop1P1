import csv
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from movie.models import Movie


class Command(BaseCommand):
    help = "Load movies from movies_initial.csv into the database."

    def handle(self, *args, **options):
        csv_path = Path(__file__).with_name("movies_initial.csv")
        created_count = 0
        updated_count = 0

        try:
            with csv_path.open(newline="", encoding="utf-8") as csv_file:
                reader = csv.DictReader(csv_file)

                for index, row in enumerate(reader):
                    if index >= 100:
                        break

                    title = row.get("title", "").strip()
                    if not title:
                        continue

                    year_value = row.get("year", "").strip()
                    year = int(year_value) if year_value else None

                    _, created = Movie.objects.update_or_create(
                        title=title,
                        defaults={
                            "genre": row.get("genre", "").strip(),
                            "year": year,
                            "description": row.get("plot", "").strip(),
                            "image": "movie/images/default.jpg",
                        },
                    )

                    if created:
                        created_count += 1
                    else:
                        updated_count += 1

        except FileNotFoundError as exc:
            raise CommandError(f"CSV file not found: {csv_path}") from exc
        except Exception as exc:
            raise CommandError(f"Unexpected error loading movies: {exc}") from exc

        self.stdout.write(
            self.style.SUCCESS(
                f"Movies loaded. Created: {created_count}. Updated: {updated_count}."
            )
        )
