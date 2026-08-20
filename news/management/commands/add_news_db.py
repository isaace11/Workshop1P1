import csv
from datetime import datetime
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from news.models import News


class Command(BaseCommand):
    help = "Load five news records from Fake.csv into the database."

    def handle(self, *args, **options):
        csv_path = Path(__file__).with_name("Fake.csv")
        created_count = 0
        updated_count = 0

        try:
            with csv_path.open(newline="", encoding="utf-8") as csv_file:
                reader = csv.DictReader(csv_file)

                for index, news_item in enumerate(reader):
                    if index >= 5:
                        break

                    headline = news_item["title"].strip()
                    body = news_item["text"].strip()
                    date_value = datetime.strptime(
                        news_item["date"],
                        "%B %d, %Y",
                    ).date()

                    _, created = News.objects.update_or_create(
                        headline=headline,
                        defaults={
                            "body": body,
                            "date": date_value,
                        },
                    )

                    if created:
                        created_count += 1
                    else:
                        updated_count += 1

        except FileNotFoundError as exc:
            raise CommandError(f"CSV file not found: {csv_path}") from exc
        except Exception as exc:
            raise CommandError(f"Unexpected error loading news: {exc}") from exc

        self.stdout.write(
            self.style.SUCCESS(
                f"News loaded. Created: {created_count}. Updated: {updated_count}."
            )
        )
