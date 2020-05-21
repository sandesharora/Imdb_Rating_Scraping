from requests import get
import pandas as pd
from bs4 import BeautifulSoup

url = 'http://www.imdb.com/search/title?release_date=2018&sort=num_votes,desc&page=1'
res = get(url)
html_soup = BeautifulSoup(res.text, 'html.parser')
movie_names = []
movie_years = []
movie_ratings = []
movie_metascores = []
movie_votes = []
# print(html_soup)
movie_container = html_soup.findAll('div', class_='lister-item mode-advanced')
print(len(movie_container))
# first_movie = BeautifulSoup(movie_container,'html.parser')
for movie in movie_container:
    if movie.find('div', {"class": "inline-block ratings-metascore"}) is not None:
        movie_name = movie.find('h3', {"class": "lister-item-header"}).find('a').get_text()
        movie_names.append(movie_name)

        movie_year = movie.find('h3', {"class": "lister-item-header"}).find('span', {
            "class": "lister-item-year text-muted unbold"}).get_text()
        movie_years.append(movie_year)

        movie_rating = movie.find('div', {"class": "inline-block ratings-imdb-rating"}).find('strong').get_text()
        movie_ratings.append(movie_rating)

        movie_metascore = movie.find('div', {"class": "inline-block ratings-metascore"}).find('span').get_text()
        movie_metascores.append(movie_metascore)

        movie_vote = movie.find('span', {"name": "nv"})['data-value']
        movie_votes.append(int(movie_vote))
        # print(movie_vote)

df = pd.DataFrame({'movie_name': movie_names, 'movie_year': movie_years, 'movie_rating': movie_ratings,
                   'movie_metascore': movie_metascores, 'votes': movie_votes})
df.loc[:, 'movie_year'] = df['movie_year'].str[-5:-1].astype(int)
df.to_csv("imdb_rating.csv")
print(df)



