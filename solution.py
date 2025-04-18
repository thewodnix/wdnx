from flask import Flask, render_template, jsonify
import random
import requests
from deep_translator import GoogleTranslator

app = Flask(__name__)

# Используем YTS API для получения популярных фильмов
YTS_API_URL = 'https://yts.mx/api/v2/list_movies.json'
# Переводчик (английский → русский)
translator = GoogleTranslator(source='en', target='ru')


def get_random_movie():
    try:
        # Запрашиваем список популярных фильмов
        response = requests.get(YTS_API_URL, params={'limit': 50, 'page': random.randint(1, 5), 'sort_by': 'rating'}, timeout=5)
        data = response.json()
        movies = data.get('data', {}).get('movies', [])
        if not movies:
            raise ValueError('Нет доступных фильмов.')

        movie = random.choice(movies)
        title = movie.get('title') or 'Без названия'
        summary_en = movie.get('summary') or ''

        # Перевод описания
        try:
            description_ru = translator.translate(summary_en)
        except Exception:
            description_ru = summary_en or 'Описание отсутствует.'

        # Обрезка описания до ближайшей точки на 200 символе
        if len(description_ru) > 400:
            snippet = description_ru[:400]
            last_dot = snippet.rfind('.')
            if last_dot != -1:
                snippet = snippet[:last_dot+1]
            description_ru = snippet

        return {
            'title': title,
            'description': description_ru,
            'poster_url': movie.get('medium_cover_image')
        }
    except Exception as e:
        return {
            'title': 'Ошибка загрузки фильма',
            'description': str(e),
            'poster_url': None
        }


@app.route('/')
def index():
    movie = get_random_movie()
    return render_template('index.html', movie=movie)


@app.route('/random_movie')
def random_movie():
    movie = get_random_movie()
    return jsonify(movie)


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
