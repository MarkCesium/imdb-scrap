from bs4 import BeautifulSoup
import requests


def get_data():
    id = 0
    for card in range(1, 1000, 50):
        url = f'https://www.imdb.com/search/title/?title_type=feature&genres=adventure&start={card}&explore=genres'
        response = requests.get(url)

        if response:
            soup = BeautifulSoup(response.text, 'html.parser')
            all_films = soup.findAll('div', class_='lister-item')
            for film in all_films:
                film_header = str(film.find('h3').find('a').contents[0])
                film_genre = film.find('p', class_='text-muted').find('span',
                                                                      class_='genre').contents[0][1:-12].split(', ')
                try:
                    film_runtime = int(film.find('p', class_='text-muted').find('span',
                                                                                class_='runtime').contents[0].split()[
                                           0])
                    film_rate = float(film.find('div', class_='ratings-bar').find('strong').contents[0])
                    film_state = 'Done'
                except AttributeError:
                    film_runtime = 'None'
                    film_rate = 'None'
                    film_state = 'Processed'
                film_desc = film.findAll('p', class_='text-muted')[1].contents[0][1:]
                id += 1
                yield {
                    'Name': film_header,
                    'Genre': film_genre,
                    'Description': film_desc,
                    'State': film_state,
                    'Runtime': film_runtime,
                    'Rate': film_rate,
                    'id': id
                }
        else:
            yield 'Something went wrong'


films = get_data()
for i in range(1000):
    print(next(films))
    print('---')
