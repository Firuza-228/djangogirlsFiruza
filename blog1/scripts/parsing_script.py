from django.core.management.base import BaseCommand
from blog.models import Post
import requests
from bs4 import BeautifulSoup
from datetime import datetime

URL = "https://ekaraganda.kz/"  # Сайт для парсинга

class Command(BaseCommand):
    help = 'Парсит статьи с ekaraganda.kz и сохраняет их в БД'

    def handle(self, *args, **kwargs):
        response = requests.get(URL)
        if response.status_code != 200:
            print("Ошибка при получении данных")
            return

        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.find_all("div", class_="news-item")  # Заменить на актуальный тег

        for article in articles:
            title = article.find("h2").text.strip()  # Заголовок
            link = article.find("a")["href"]  # Ссылка
            date_text = article.find("time").text.strip()  # Дата публикации
            image = article.find("img")["src"]  # Изображение

            published_date = datetime.strptime(date_text, "%d.%m.%Y")  # Пример формата

            # Проверяем, есть ли такая статья в БД
            if not Post.objects.filter(title=title).exists():
                Post.objects.create(
                    title=title,
                    text="Подробнее на сайте",
                    published_date=published_date,
                    image_url=image,
                    source_url=URL + link,
                )
                self.stdout.write(self.style.SUCCESS(f"Добавлена статья: {title}"))
