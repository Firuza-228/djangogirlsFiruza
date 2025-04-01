from django.core.management.base import BaseCommand
from blog.models import Post
import requests
from bs4 import BeautifulSoup
from datetime import datetime

class Command(BaseCommand):
    help = 'Парсит статьи с сайта Forbes.kz'

    def handle(self, *args, **kwargs):
        url = "https://www.forbes.kz/"

        response = requests.get(url)

        if response.status_code == 200:
            # Создаем объект BeautifulSoup для парсинга
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Ищем все новости на странице
            news_items = soup.find_all('div', class_='container')

            # Проходим по всем найденным новостям и извлекаем заголовки и даты
            for item in news_items:
                # Заголовок новости
                title_tag = item.find('div', class_='card__title')
                title = title_tag.text.strip() if title_tag else 'Без заголовка'
                
                # Для даты используем тег div с классом "card__time"
                date_tag = item.find_next('div', class_='card__time')
                date = date_tag.text.strip() if date_tag else 'Дата не найдена'

                # Сохраняем статью в базе данных, если она еще не существует
                if not Post.objects.filter(title=title).exists():
                    published_date = None
                    try:
                        published_date = datetime.strptime(date, "%d %B %Y, %H:%M")
                    except ValueError:
                        pass  # Если дата не удается преобразовать, оставляем None

                    Post.objects.create(
                        title=title,
                        text="Подробнее на сайте",
                        published_date=published_date,
                        image_url="",
                        source_url=url,
                    )
                    self.stdout.write(self.style.SUCCESS(f"Добавлена статья: {title}"))
                else:
                    self.stdout.write(self.style.SUCCESS(f"Статья уже существует: {title}"))
        else:
            self.stdout.write(self.style.ERROR(f"Ошибка при загрузке страницы: {response.status_code}"))
